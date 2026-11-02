#!/usr/bin/env python3
"""Import the dual-mode LaTeX CV into the website's plain-text data file.

Usage: python scripts/import_cv.py /path/to/curriculum_vitae_seongju_lee
Only Python's standard library is required. The CV remains the source of truth.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from urllib.parse import urlsplit


def uncomment(text: str) -> str:
    return "\n".join(re.split(r"(?<!\\)%", line, maxsplit=1)[0] for line in text.splitlines())


def group(text: str, position: int) -> tuple[str, int]:
    while position < len(text) and text[position].isspace():
        position += 1
    if position >= len(text) or text[position] != "{":
        raise ValueError(f"Expected a TeX argument near {text[position:position + 60]!r}")
    start = position + 1
    depth = 1
    position += 1
    while position < len(text):
        char = text[position]
        if char == "\\" and position + 1 < len(text) and text[position + 1] in "{}\\":
            position += 2
            continue
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if not depth:
                return text[start:position], position + 1
        position += 1
    raise ValueError("Unclosed TeX argument")


def arguments(text: str, position: int, count: int) -> tuple[list[str], int]:
    values = []
    for _ in range(count):
        value, position = group(text, position)
        values.append(value)
    return values, position


def definitions(text: str) -> tuple[dict[str, str], str]:
    records = {}
    spans = []
    pattern = r"\\newcommand\s*\{\\([A-Za-z]+)\}(?:\s*\[\d+\])?"
    for match in re.finditer(pattern, text):
        value, end = group(text, match.end())
        records[match.group(1)] = value
        spans.append((match.start(), end))
    for start, end in reversed(spans):
        text = text[:start] + text[end:]
    return records, text


def mode(text: str, selected: bool) -> str:
    """Evaluate the CV's single boolean, including nested occurrences."""
    token = re.compile(r"\\(ifselectedcv|else|fi)\b")
    while (start := re.search(r"\\ifselectedcv\b", text)) is not None:
        depth, middle, end = 1, None, None
        for match in token.finditer(text, start.end()):
            if match.group(1) == "ifselectedcv":
                depth += 1
            elif match.group(1) == "fi":
                depth -= 1
                if depth == 0:
                    end = match
                    break
            elif depth == 1:
                middle = match
        if end is None:
            raise ValueError("Unclosed ifselectedcv")
        yes = text[start.end():middle.start() if middle else end.start()]
        no = text[middle.end():end.start()] if middle else ""
        text = text[:start.start()] + mode(yes if selected else no, selected) + text[end.end():]
    return text


def plain(text: str, selected: bool = False) -> str:
    text = mode(text, selected)
    result = []
    position = 0
    wrappers = {"textbf", "textit", "textrm", "texttt", "underline", "krbf", "emph", "MakeUppercase"}
    declarations = {"ttfamily", "bfseries", "footnotesize", "small", "normalsize", "raggedright", "selectfont"}
    while position < len(text):
        char = text[position]
        if char == "{":
            value, position = group(text, position)
            result.append(plain(value, selected))
        elif char == "\\":
            if position + 1 >= len(text):
                break
            if not text[position + 1].isalpha():
                escape = text[position + 1]
                result.append(escape if escape in "&%_#$" else " ")
                position += 2
                continue
            match = re.match(r"\\([A-Za-z]+)", text[position:])
            assert match is not None
            command = match.group(1)
            position += match.end()
            if command in wrappers:
                value, position = group(text, position)
                result.append(plain(value, selected))
            elif command in {"textcolor", "href"}:
                values, position = arguments(text, position, 2)
                result.append(plain(values[1], selected))
            elif command in {"includegraphics", "cvpublicationrole"}:
                if command == "includegraphics":
                    while position < len(text) and text[position].isspace():
                        position += 1
                    if position < len(text) and text[position] == "[":
                        position = text.index("]", position) + 1
                _, position = group(text, position)
            elif command == "space":
                result.append(" ")
            elif command in declarations or command.endswith("icon"):
                pass
            else:
                raise ValueError(f"Unhandled content command: {command}")
        else:
            result.append(char)
            position += 1
    return re.sub(r"\s+", " ", "".join(result).replace("---", "\u2014").replace("--", "\u2013")).strip()


def entries(text: str, selected: bool = False) -> list[list[str]]:
    text = mode(text, selected)
    return [arguments(text, match.end(), 4)[0] for match in re.finditer(r"\\entry\b", text)]


def link_records(text: str) -> list[dict[str, str]]:
    links = []
    for match in re.finditer(r"\\href\b", text):
        (url, label), _ = arguments(text, match.end(), 2)
        links.append({"label": plain(label).strip("[]"), "url": url.strip().replace(r"\&", "&")})
    return links


def colored_group(text: str, color: str) -> tuple[str, tuple[int, int]] | None:
    for match in re.finditer(r"\\textcolor\b", text):
        values, end = arguments(text, match.end(), 2)
        if values[0] == color:
            return values[1], (match.start(), end)
    return None


def summary(text: str, selected: bool = False) -> str:
    red = colored_group(text, "red")
    return re.sub(r"^TL;DR:\s*", "", plain(red[0], selected)) if red else ""


def selected_calls(text: str, prefix: str) -> list[str]:
    return re.findall(r"\\(" + prefix + r"[A-Za-z]+)\b", mode(text, True))


def publication_selection_groups(rendering: str) -> dict[str, str]:
    """Read selected groups from their CV subsection, without naming papers."""
    groups = {}
    current = "main"
    pattern = r"\\cvsubsect\b(?:\s*\[[^\]]*\])?|\\(cvpub[A-Za-z]+)\b"
    selected = mode(rendering, True)
    for match in re.finditer(pattern, selected):
        if match.group(1):
            groups[match.group(1)] = current
        else:
            values, _ = arguments(selected, match.end(), 2)
            heading = plain(values[1]).casefold()
            current = "additional" if heading.startswith("additional ") and "author" in heading else "main"
    return groups


def publication_records(source: str) -> list[dict]:
    macros, rendering = definitions(source)
    selected = selected_calls(rendering, "cvpub")
    selection_groups = publication_selection_groups(rendering)
    full = selected_calls(mode(rendering, False), "cvpub")
    records = []
    for identifier in full:
        kind, title, venue, body = entries(macros[identifier])[0]
        kind = plain(kind).lower().replace("top ", "").replace(" ", "-")
        if kind == "in-submission":
            kind = "submission"
        category = "domestic" if identifier.startswith("cvpubDomestic") else "international"
        if kind in {"submission", "wip"}:
            category = kind
        red = colored_group(body, "red")
        authors_tex = body[:red[1][0]] + body[red[1][1]:] if red else body
        blue = colored_group(authors_tex, "blue")
        if blue:
            authors_tex = authors_tex[:blue[1][0]] + authors_tex[blue[1][1]:]
        authors = plain(authors_tex)
        author_role = ""
        if "Seongju Lee*" in authors:
            author_role = "Co-first author"
        elif authors.startswith(("Seongju Lee", "\uc774\uc131\uc8fc")):
            author_role = "First author"
        venue_text = plain(venue)
        notes = []
        if kind == "submission":
            target = colored_group(venue, "gray")
            if target:
                venue_text = plain(target[0])
                note = plain(venue[:target[1][0]] + venue[target[1][1]:])
                if note:
                    notes.append(note)
            venue_text = "In Submission. " + venue_text
        metrics = []
        if blue:
            for metric in re.finditer(r"\\(?:rankicon|citeicon)\s*(.*?)(?=\\(?:rankicon|citeicon)|$)", blue[0], re.S):
                metrics.append(plain(metric.group(1)))
        years = re.findall(r"\b(?:19|20)\d{2}\b", venue_text)
        records.append({
            "id": identifier, "title": plain(title), "authors": authors,
            "venue": venue_text, "year": int(years[0]) if years else None,
            "category": category, "type": kind, "selected": identifier in selected,
            "selectedOrder": selected.index(identifier) + 1 if identifier in selected else None,
            "authorRole": author_role, "summary": summary(body),
            "links": link_records(body), "metrics": metrics, "notes": notes,
            **({"selectionGroup": "additional"}
               if selection_groups.get(identifier) == "additional" else {}),
        })
    return records


def project_records(source: str) -> list[dict]:
    macros, rendering = definitions(source)
    selected = [name for name in selected_calls(rendering, "cvproject") if name in macros]
    full = [name for name in selected_calls(mode(rendering, False), "cvproject") if name in macros]
    records = []
    for identifier in full:
        period_role, title, organization, body = entries(macros[identifier], identifier in selected)[0]
        period, _, role = period_role.partition(r"\\")
        records.append({
            "id": identifier, "title": plain(title), "period": plain(period),
            "role": plain(role.replace(r"\\", " \u00b7 ")), "organization": plain(organization),
            "summary": summary(body, identifier in selected),
            "selected": identifier in selected,
            "selectedOrder": selected.index(identifier) + 1 if identifier in selected else None,
            "links": link_records(body),
        })
    return records


def experience_records(source: str) -> list[dict]:
    records = []
    for period, title, organization, body in entries(source):
        period, _, role = period.partition(r"\\")
        description = ". ".join(part for part in [plain(role), plain(body)] if part)
        records.append({"period": plain(period), "title": plain(title), "organization": plain(organization), "description": description})
    return records


def education_records(source: str) -> list[dict]:
    selected = {(plain(row[0]), plain(row[1])) for row in entries(source, True)}
    records = []
    for period, institution, advisor, body in entries(source):
        degree, _, detail = body.partition(r"\\")
        key = (plain(period), plain(institution))
        records.append({"period": key[0], "institution": key[1], "degree": plain(degree),
                        "details": " ".join(part for part in [plain(detail), plain(advisor)] if part),
                        "selected": key in selected})
    return records


def award_records(source: str) -> list[dict]:
    # Selected mode may shorten titles and venues; date and result identify the award.
    full = entries(source)
    full_keys = [(plain(row[0]), plain(row[3])) for row in full]
    assert len(full_keys) == len(set(full_keys)), "Award selection keys (date, result) must be unique"
    selected = {(plain(row[0]), plain(row[3])) for row in entries(source, True)}
    assert selected <= set(full_keys), "Selected awards must match a full-CV date and result"
    return [{"date": plain(date), "title": plain(title), "organization": plain(organization),
             "result": plain(result), "selected": (plain(date), plain(result)) in selected}
            for date, title, organization, result in full]


def patent_records(source: str) -> list[dict]:
    records = []
    for period_status, title, number, inventors in entries(source):
        year, _, status = period_status.partition(r"\\")
        records.append({"year": plain(year), "title": plain(title), "status": plain(status),
                        "number": plain(number), "inventors": plain(inventors)})
    return records


def validate(data: dict) -> None:
    for collection in ["publications", "projects", "education", "awards", "experience", "academicExperience", "patents"]:
        records = data[collection]
        assert records, f"Empty collection: {collection}"
        if collection not in {"publications", "projects", "education", "awards"}:
            continue
        assert all(isinstance(record["selected"], bool) for record in records), collection
        chosen = [record for record in records if record["selected"]]
        if collection in {"publications", "projects"}:
            assert all(isinstance(record["selectedOrder"], int) for record in chosen), collection
            assert sorted(record["selectedOrder"] for record in chosen) == list(range(1, len(chosen) + 1)), collection
            assert all(record["selectedOrder"] is None for record in records if not record["selected"]), collection
            assert all(isinstance(record["id"], str) and record["id"] for record in records), collection
            assert len({record["id"] for record in records}) == len(records)
    assert not any(item["metrics"] for item in data["publications"] if item["category"] == "domestic")
    for item in data["publications"]:
        assert item.get("selectionGroup", "main") in {"main", "additional"}, item["id"]
        if item.get("selectionGroup") == "additional":
            assert item["selected"] and item["category"] not in {"submission", "wip"}, item["id"]
            assert item["authorRole"] in {"First author", "Co-first author"}, item["id"]

    def visit(value):
        if isinstance(value, dict):
            for key, content in value.items():
                if key in {"url", "sourceUrl"}:
                    parsed = urlsplit(content)
                    assert parsed.scheme in {"https", "http"} and parsed.netloc, content
                visit(content)
        elif isinstance(value, list):
            for content in value:
                visit(content)
        elif isinstance(value, str):
            assert "\\" not in value, value
            assert not re.search(r"<[^>]+>", value), value
    visit(data)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cv_dir", type=Path, help="Directory containing main.tex and the dual-mode CV sections")
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parents[1] / "src/data/profile.json")
    parser.add_argument("--as-of", default="2026-11-02", help="Date when the CV facts and metrics were checked")
    args = parser.parse_args()

    def read(name):
        return uncomment((args.cv_dir / name).read_text(encoding="utf-8-sig"))

    experience = experience_records(read("02_research_experience.tex"))
    profile = {
        "name": "Seongju Lee", "title": experience[0]["title"],
        "affiliation": experience[0]["organization"], "location": "South Korea",
        "email": "sungjulee96@gmail.com", "github": "https://github.com/SeongjuLee",
        "scholar": "https://scholar.google.com/citations?user=Q0LR04AAAAAJ",
        "photo": "assets/images/profile/seongju_lee.jpg",
        "cv": "assets/docs/Seongju_Lee_CV_Full.pdf",
        "selectedCv": "assets/docs/Seongju_Lee_CV_Robotics_Perception.pdf",
        "bio": [
            "I am a Senior Researcher at HD Hyundai Robotics, working on humanoid and dual-arm robot learning and multimodal data pipelines.",
            "My research spans object detection, semantic segmentation, domain generalization, and multi-agent trajectory prediction. I have experience leading perception software development and building multi-view datasets for autonomous systems.",
            "I received my Ph.D. in AI Convergence from Gwangju Institute of Science and Technology (GIST) in February 2026, advised by Prof. Kyoobin Lee.",
        ],
        "researchInterests": ["Robust visual perception", "Domain generalization and knowledge distillation", "Multi-agent trajectory prediction", "Multimodal robot learning"],
    }
    data = {
        "asOf": args.as_of, "profile": profile,
        "publications": publication_records(read("03_publications.tex")),
        "projects": project_records(read("04_projects.tex")),
        "experience": experience,
        "academicExperience": experience_records(read("08_academic_experience_service.tex")),
        "education": education_records(read("05_education.tex")),
        "awards": award_records(read("06_awards.tex")),
        "patents": patent_records(read("07_patents.tex")),
    }
    # Media is curated separately from the CV; retain its mapping when importing updates.
    if args.output.exists():
        previous = json.loads(args.output.read_text(encoding="utf-8-sig"))
        for collection in ("publications", "projects"):
            media_by_id = {item["id"]: item["media"] for item in previous.get(collection, [])
                           if item.get("media")}
            for item in data[collection]:
                if item["id"] in media_by_id:
                    item["media"] = media_by_id[item["id"]]
    validate(data)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Imported {len(data['publications'])} publications and {len(data['projects'])} projects into {args.output}")


if __name__ == "__main__":
    main()
