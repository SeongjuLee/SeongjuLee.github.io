"""Check the static site's research records, structure, and local destinations."""
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.ids = []
        self.links = []
        self.assets = []
        self.headings = []
        self.content = []
        self.domestic_content = []
        self.sections = []
        self.main_focusable = False
        self.lang = None
        self.image_alts = []
        self.feed(path.read_text(encoding="utf-8"))

    def handle_starttag(self, tag, attrs):
        attr = dict(attrs)
        if attr.get("id"):
            self.ids.append(attr["id"])
        if tag == "html":
            self.lang = attr.get("lang")
        if tag == "a" and attr.get("href"):
            self.links.append(attr["href"])
        if tag == "link" and "canonical" not in attr.get("rel", ""):
            if attr.get("href"):
                self.assets.append(attr["href"])
        if tag in {"img", "script"} and attr.get("src"):
            self.assets.append(attr["src"])
        if tag == "img":
            self.image_alts.append(attr.get("alt"))
        if tag == "main" and attr.get("id") == "main":
            self.main_focusable = attr.get("tabindex") == "-1"
        if tag == "section":
            self.sections.append(attr.get("id"))
        if re.fullmatch("h[1-6]", tag):
            self.headings.append(int(tag[1]))

    def handle_endtag(self, tag):
        if tag == "section" and self.sections:
            self.sections.pop()

    def handle_data(self, data):
        self.content.append(data)
        if "domestic" in self.sections:
            self.domestic_content.append(data)


def check():
    errors = []

    def require(condition, message):
        if not condition:
            errors.append(message)

    pages = {path.resolve(): Page(path) for path in
             [ROOT / "index.html", *sorted((ROOT / "src/pages").glob("*.html"))]}
    require(len(pages) == 6, "Expected the homepage and five preserved archive routes")
    for path, page in pages.items():
        label = str(path.relative_to(ROOT))
        require(page.lang == "en", f"{label}: missing document language")
        require(page.headings.count(1) == 1, f"{label}: expected one H1")
        require(len(page.ids) == len(set(page.ids)), f"{label}: duplicate IDs")
        require(page.main_focusable, f"{label}: skip destination must accept focus")
        require("#main" in page.links, f"{label}: missing skip link")
        require(all(alt for alt in page.image_alts), f"{label}: missing image description")
        for previous, current in zip(page.headings, page.headings[1:]):
            require(current <= previous + 1, f"{label}: heading level jumps H{previous} to H{current}")
        for href in page.links + page.assets:
            parts = urlsplit(href)
            if parts.scheme or parts.netloc:
                require(parts.scheme in {"https", "http", "mailto"}, f"{label}: unsupported URL {href}")
                continue
            target = (ROOT / unquote(parts.path).lstrip("/") if parts.path.startswith("/")
                      else path.parent / unquote(parts.path)) if parts.path else path
            target = target.resolve()
            if target.is_dir():
                target = target / "index.html"
            require(target.is_relative_to(ROOT), f"{label}: link escapes repository {href}")
            require(target.is_file(), f"{label}: missing local destination {href}")
            if parts.fragment and target in pages:
                require(unquote(parts.fragment) in pages[target].ids, f"{label}: missing anchor {href}")
        require("Cited by" not in " ".join(page.domestic_content), f"{label}: domestic citation count displayed")

    data = json.loads((ROOT / "src/data/profile.json").read_text(encoding="utf-8"))
    home = pages[(ROOT / "index.html").resolve()]
    publication_page = pages[(ROOT / "src/pages/publications.html").resolve()]
    project_page = pages[(ROOT / "src/pages/projects.html").resolve()]
    for collection, archive in [("publications", publication_page), ("projects", project_page)]:
        records = data[collection]
        selected = sorted((item for item in records if item["selected"]), key=lambda item: item["selectedOrder"])
        all_ids = {item["id"] for item in records}
        actual_home = [item_id for item_id in home.ids if item_id in all_ids]
        require(actual_home == [item["id"] for item in selected], f"{collection}: selected order/content mismatch")
        require(all_ids <= set(archive.ids), f"{collection}: archive omits records")
    body = " ".join(home.content)
    require("Senior Researcher" in body and "HD Hyundai Robotics" in body, "Outdated current affiliation")
    require("Ph.D. Candidate" not in body, "Outdated doctoral candidate status")
    require("In submission" in body, "Submission must be identified separately")
    for key in ("cv", "selectedCv"):
        pdf = ROOT / data["profile"][key]
        require(pdf.is_file() and pdf.read_bytes().startswith(b"%PDF-"), f"Invalid {key} PDF")

    if errors:
        for message in errors:
            print(message, file=sys.stderr)
        return 1
    print(f"Checked {len(pages)} pages: research records, headings, anchors, local assets, and CV PDFs.")
    return 0


if __name__ == "__main__":
    raise SystemExit(check())
