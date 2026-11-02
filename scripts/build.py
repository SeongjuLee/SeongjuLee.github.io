#!/usr/bin/env python3
"""Render the committed, JavaScript-independent site from profile.json.

Run `python scripts/build.py` to rebuild, or add `--check` to check that the
generated pages match their source. Only the Python standard library is used.
"""

from __future__ import annotations

import argparse
import hashlib
from html import escape
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "src/data/profile.json"
CSS_VERSION = hashlib.sha256((ROOT / "assets/css/site.css").read_bytes()).hexdigest()[:12]
BASE_URL = "https://seongjulee.github.io/"
PAGES = {
    "home": ("index.html", "Home"),
    "publications": ("src/pages/publications.html", "Publications"),
    "projects": ("src/pages/projects.html", "Projects"),
    "experiences": ("src/pages/experiences.html", "Experience"),
    "awards": ("src/pages/awards.html", "Awards"),
    "patents": ("src/pages/patents.html", "Patents"),
}


def text(value: object) -> str:
    return escape(str(value or ""), quote=True)


def url(value: str, prefix: str = "") -> str:
    """Keep local asset URLs relative to each generated page."""
    value = str(value or "")
    parsed = urlsplit(value)
    if parsed.scheme:
        if parsed.scheme not in {"http", "https", "mailto"}:
            raise ValueError(f"Unsupported link scheme: {parsed.scheme}")
        return text(value)
    if value.startswith("#"):
        return text(value)
    if parsed.path.endswith(".pdf") and not parsed.query and not parsed.fragment:
        revision = hashlib.sha256((ROOT / parsed.path.lstrip("/")).read_bytes()).hexdigest()[:12]
        value += f"?v={revision}"
    return text(prefix + value.lstrip("/"))


def anchor(label: str, target: str, prefix: str = "", css: str = "") -> str:
    class_attr = f' class="{text(css)}"' if css else ""
    return f'<a href="{url(target, prefix)}"{class_attr}>{text(label)}</a>'


def links(items: list[dict], prefix: str = "") -> str:
    if not items:
        return ""
    return '<p class="item-links">' + " · ".join(
        anchor(item["label"], item["url"], prefix) for item in items
    ) + "</p>"


def authors(value: str | list[str], name: str) -> str:
    if isinstance(value, list):
        value = ", ".join(value)
    parts = re.split(f"({re.escape(name)})", str(value), flags=re.IGNORECASE)
    return "".join(
        f"<strong>{text(part)}</strong>" if part.casefold() == name.casefold()
        else text(part) for part in parts
    )


def research_media(item: dict, prefix: str) -> str:
    """Render a real research asset, or reserve its place without inventing one."""
    media = item.get("media") or {}
    src = media.get("src")
    if not src:
        return '<div class="research-media media-placeholder" aria-hidden="true"></div>'
    kind = media.get("kind", "gif")
    if kind not in {"gif", "image", "video"}:
        raise ValueError(f"Unsupported media kind for {item['id']}: {kind}")
    alt = media.get("alt") or item["title"]
    poster = media.get("poster")
    if kind == "video":
        poster_attr = f' poster="{url(poster, prefix)}"' if poster else ""
        return f'''<div class="research-media">
      <video controls preload="none" width="320" height="200" aria-label="{text(alt)}"{poster_attr}>
        <source src="{url(src, prefix)}">
        {anchor('Open research video', src, prefix)}
      </video>
    </div>'''
    motion_class = " media-animated-no-poster" if kind == "gif" and not poster else ""
    reduced_source = (f'<source media="(prefers-reduced-motion: reduce)" srcset="{url(poster, prefix)}">'
                      if kind == "gif" and poster else "")
    return f'''<a class="research-media{motion_class}" href="{url(src, prefix)}" aria-label="{text('Open original preview: ' + alt)}">
      <picture>
        {reduced_source}
        <img src="{url(src, prefix)}" alt="{text(alt)}" loading="lazy" decoding="async" width="320" height="200">
      </picture>
    </a>'''


def publication(item: dict, profile: dict, prefix: str, metrics: bool = False) -> str:
    role = item.get("authorRole")
    role_html = f'<span class="author-role">{text(role)}</span>' if role else ""
    summary = item.get("summary")
    summary_html = f'<p class="item-summary">{text(summary)}</p>' if summary else ""
    notes_html = "".join(f'<p class="item-summary">{text(note)}</p>' for note in item.get("notes", []))
    metric_html = ""
    if metrics and item.get("category") != "domestic" and item.get("metrics"):
        metric_html = '<p class="item-metrics">' + " · ".join(
            text(value) for value in item["metrics"]
        ) + "</p>"
    with_media = bool(item.get("media") or (item.get("selected") and item.get("selectionGroup") != "additional"))
    media_html = research_media(item, prefix) if with_media else ""
    article_class = ' class="research-row"' if with_media else ""
    return f'''<li class="publication" id="{text(item['id'])}">
  <article{article_class}>
    {media_html}
    <div class="research-copy">
    <h3>{text(item['title'])}</h3>
    <p class="authors">{authors(item.get('authors', ''), profile['name'])}{role_html}</p>
    <p class="venue">{text(item.get('venue', ''))}</p>
    {notes_html}
    {summary_html}
    {links(item.get('links', []), prefix)}
    {metric_html}
    </div>
  </article>
</li>'''


def publication_list(items: list[dict], profile: dict, prefix: str,
                     metrics: bool = False) -> str:
    return '<ol class="publication-list">\n' + "\n".join(
        publication(item, profile, prefix, metrics) for item in items
    ) + "\n</ol>"


def project_media(item: dict, prefix: str) -> str:
    """Optionally pair a platform view with the existing perception preview."""
    media = item.get("media") or {}
    platform = media.get("platform")
    if not platform:
        return research_media(item, prefix)
    if platform.get("kind", "gif") not in {"image", "gif"}:
        raise ValueError(f"Unsupported platform media kind for {item['id']}")
    platform_item = {**item, "media": platform}
    return f'''<div class="project-media-stack">
    <figure>
      {research_media(platform_item, prefix)}
      <figcaption>Platform</figcaption>
    </figure>
    <figure>
      {research_media(item, prefix)}
      <figcaption>Perception</figcaption>
    </figure>
  </div>'''


def project_list(items: list[dict], prefix: str, heading_level: int = 3) -> str:
    rows = []
    for item in items:
        date_html = f'<p class="item-date">{text(item["period"])}</p>'
        media = item.get("media") or {}
        credit_parts = []
        if media.get("credit"):
            credit_parts.append(text(media["credit"]))
        if media.get("sourceUrl"):
            credit_parts.append(anchor("Video source", media["sourceUrl"], prefix))
        credit_html = ('<p class="media-credit">' + " · ".join(credit_parts) + '</p>') if credit_parts else ""
        project_links = [link for link in item.get("links", []) if link["url"] != media.get("sourceUrl")]
        content = f'''
    <h{heading_level}>{text(item['title'])}</h{heading_level}>
    <p class="organization">{text(item['organization'])}</p>
    <p class="item-role">{text(item['role'])}</p>
    <p class="item-summary">{text(item['summary'])}</p>
    {links(project_links, prefix)}
    {credit_html}'''
        if item.get("selected") or item.get("media"):
            rows.append(f'''<li class="dated-item project-with-media" id="{text(item['id'])}">
  <article class="research-row">
    {project_media(item, prefix)}
    <div class="research-copy">
      {date_html}
      {content}
    </div>
  </article>
</li>''')
        else:
            rows.append(f'''<li class="dated-item" id="{text(item['id'])}">
  {date_html}
  <article>{content}
  </article>
</li>''')
    return '<ul class="dated-list projects-list">\n' + "\n".join(rows) + "\n</ul>"


def experience_list(items: list[dict]) -> str:
    rows = []
    for item in items:
        description = item.get("description")
        if isinstance(description, list):
            description = " ".join(description)
        detail = f'<p class="item-summary">{text(description)}</p>' if description else ""
        rows.append(f'''<li class="dated-item">
  <p class="item-date">{text(item['period'])}</p>
  <div>
    <h3>{text(item['title'])}</h3>
    <p class="organization">{text(item['organization'])}</p>
    {detail}
  </div>
</li>''')
    return '<ul class="dated-list">\n' + "\n".join(rows) + "\n</ul>"


def education_list(items: list[dict]) -> str:
    rows = []
    for item in items:
        details = item.get("details", [])
        if isinstance(details, str):
            details = [details]
        detail = "".join(f'<p class="item-summary">{text(value)}</p>' for value in details)
        rows.append(f'''<li class="dated-item">
  <p class="item-date">{text(item['period'])}</p>
  <div>
    <h3>{text(item['degree'])}</h3>
    <p class="organization">{text(item['institution'])}</p>
    {detail}
  </div>
</li>''')
    return '<ul class="dated-list">\n' + "\n".join(rows) + "\n</ul>"


def award_list(items: list[dict], heading_level: int = 3) -> str:
    rows = []
    for item in items:
        rows.append(f'''<li class="dated-item">
  <p class="item-date">{text(item['date'])}</p>
  <div>
    <h{heading_level}>{text(item['title'])}</h{heading_level}>
    <p class="award-result">{text(item['result'])}</p>
    <p class="organization">{text(item['organization'])}</p>
  </div>
</li>''')
    return '<ul class="dated-list awards-list">\n' + "\n".join(rows) + "\n</ul>"


def patent_list(items: list[dict], profile: dict) -> str:
    rows = []
    for index, item in enumerate(items, 1):
        number = item.get("number")
        number_html = f' · {text(number)}' if number else ""
        rows.append(f'''<li class="publication" id="patent-{index}">
  <article>
    <h2>{text(item['title'])}</h2>
    <p class="authors">{authors(item.get('inventors', ''), profile['name'])}</p>
    <p class="venue">{text(item.get('status', ''))}{number_html} · {text(item.get('year', ''))}</p>
  </article>
</li>''')
    return '<ol class="publication-list patent-list">\n' + "\n".join(rows) + "\n</ol>"


def section(title: str, section_id: str, body: str,
            more_label: str = "", more_url: str = "", prefix: str = "") -> str:
    more = anchor(more_label, more_url, prefix, "section-more") if more_label else ""
    return f'''<section class="content-section" aria-labelledby="{section_id}-heading" id="{section_id}">
  <div class="section-heading">
    <h2 id="{section_id}-heading">{text(title)}</h2>
    {more}
  </div>
  {body}
</section>'''


def shell(page: str, data: dict, content: str, description: str) -> str:
    profile = data["profile"]
    path, label = PAGES[page]
    prefix = "" if page == "home" else "../../"
    title = f"{profile['name']} — Robotics & Perception" if page == "home" else f"{label} | {profile['name']}"
    nav = []
    for key, (target, nav_label) in PAGES.items():
        active = ' aria-current="page"' if key == page else ""
        target_url = text(prefix or "./") if key == "home" else url(target, prefix)
        nav.append(f'<a href="{target_url}"{active}>{text(nav_label)}</a>')
    photo = str(profile["photo"]).lstrip("/")
    return f'''<!DOCTYPE html>
<!-- Generated by scripts/build.py from src/data/profile.json. -->
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{text(title)}</title>
  <meta name="description" content="{text(description)}">
  <link rel="canonical" href="{BASE_URL}{path if page != 'home' else ''}">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{text(title)}">
  <meta property="og:description" content="{text(description)}">
  <meta property="og:url" content="{BASE_URL}{path if page != 'home' else ''}">
  <meta property="og:image" content="{BASE_URL}{text(photo)}">
  <meta property="og:image:alt" content="Portrait of {text(profile['name'])}">
  <meta name="theme-color" content="#ffffff">
  <link rel="icon" type="image/svg+xml" href="{prefix}assets/favicon.svg">
  <link rel="stylesheet" href="{prefix}assets/css/site.css?v={CSS_VERSION}">
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  <header class="site-header wrapper">
    <a class="site-name" href="{text(prefix or './')}">{text(profile['name'])}</a>
    <nav class="site-nav" aria-label="Main navigation">
      {' '.join(nav)}
    </nav>
  </header>
  <main class="wrapper" id="main" tabindex="-1">
    {content}
  </main>
  <footer class="site-footer wrapper">
    <p>{text(profile['name'])} · {anchor('Email', 'mailto:' + profile['email'])} · {anchor('GitHub', profile['github'])}</p>
    <p>Updated <time datetime="{text(data['asOf'])}">{text(data['asOf'])}</time> · {anchor('Full CV', profile['cv'], prefix)}</p>
  </footer>
</body>
</html>
'''


def home(data: dict) -> str:
    profile = data["profile"]
    bio = "\n".join(f'<p>{text(value)}</p>' for value in profile["bio"])
    contact = [
        anchor("Full CV", profile["cv"]),
        anchor("Selected CV", profile["selectedCv"]),
        anchor("Email", "mailto:" + profile["email"]),
        anchor("Google Scholar", profile["scholar"]),
        anchor("GitHub", profile["github"]),
    ]
    intro = f'''<section class="profile" aria-labelledby="profile-name">
  <div class="profile-text">
    <h1 id="profile-name">{text(profile['name'])}</h1>
    <p class="profile-affiliation">{text(profile['title'])}, {text(profile['affiliation'])}</p>
    <p class="profile-links">{' · '.join(contact)}</p>
    <div class="bio">{bio}</div>
    <p class="research-interests"><strong>Research interests:</strong> {text('; '.join(profile['researchInterests']))}.</p>
  </div>
  <img class="portrait" src="{url(profile['photo'])}" alt="{text(profile['name'])}" width="160" height="192" fetchpriority="high">
</section>'''
    selected = sorted((item for item in data["publications"] if item.get("selected")),
                      key=lambda item: item.get("selectedOrder", 999))
    published = [item for item in selected if item["category"] not in {"submission", "wip"}]
    primary = [item for item in published if item.get("selectionGroup") != "additional"]
    additional = [item for item in published if item.get("selectionGroup") == "additional"]
    submitted = [item for item in selected if item["category"] == "submission"]
    publications_html = publication_list(primary, profile, "")
    if additional:
        publications_html += '<h3 class="subsection-heading" id="additional-publications-heading">Additional First-/Co-first-Author Publications</h3>\n'
        publications_html += publication_list(additional, profile, "")
    publications_html += '<p class="section-note">* Equal contribution.</p>'
    if submitted:
        publications_html += '<h3 class="subsection-heading">In submission</h3>\n'
        publications_html += publication_list(submitted, profile, "")
    projects = sorted((item for item in data["projects"] if item.get("selected")),
                      key=lambda item: item.get("selectedOrder", 999))
    body = intro + section("Selected publications", "publications", publications_html,
                           "All publications →", PAGES["publications"][0])
    body += section("Selected projects", "projects", project_list(projects, ""),
                    "All projects →", PAGES["projects"][0])
    body += section("Professional experience", "experience", experience_list(data["experience"]),
                    "All experience →", PAGES["experiences"][0])
    body += section("Education", "education", education_list(
        [item for item in data["education"] if item.get("selected")]))
    body += section("Selected awards", "awards", award_list(
        [item for item in data["awards"] if item.get("selected")]),
        "All awards →", PAGES["awards"][0])
    return shell("home", data, body,
                 f"{profile['name']}, {profile['title']} at {profile['affiliation']}. Research in robust perception, maritime vision, and robotics.")


def page_heading(title: str, description: str, extras: str = "") -> str:
    return f'''<header class="page-heading">
  <h1>{text(title)}</h1>
  <p>{text(description)}</p>
  {extras}
</header>'''


def publications_page(data: dict) -> str:
    groups = [
        ("international", "International publications"),
        ("domestic", "Domestic publications"),
        ("submission", "In submission"),
        ("wip", "Work in progress"),
    ]
    available = [(key, label) for key, label in groups
                 if any(item["category"] == key for item in data["publications"])]
    jump_links = '<nav class="page-index" aria-label="Publication categories">' + " · ".join(
        anchor(label, "#" + key) for key, label in available
    ) + "</nav>"
    body = page_heading("Publications", "Complete publication list, with submitted and ongoing work listed separately.", jump_links)
    body += f'<p class="archive-note">Citation and venue metrics, where included, reflect the CV snapshot of <time datetime="{text(data["asOf"])}">{text(data["asOf"])}</time>. Journal impact factors and JCR quartiles use the years explicitly shown. Domestic publications omit citation counts.</p>'
    for key, label in available:
        items = [item for item in data["publications"] if item["category"] == key]
        publications_html = publication_list(items, data["profile"], "../../", metrics=True)
        if key == "international":
            publications_html += '<p class="section-note">* Equal contribution.</p>'
        body += section(label, key, publications_html)
    return shell("publications", data, body, f"Publications by {data['profile']['name']}: robust perception, computer vision, and robotics.")


def archive(page: str, data: dict) -> str:
    if page == "projects":
        body = page_heading("Projects", "Research and development projects across robotics, perception, and machine learning.")
        body += project_list(data["projects"], "../../", heading_level=2)
        description = f"Research and development projects by {data['profile']['name']}."
    elif page == "experiences":
        body = page_heading("Experience & education", "Professional appointments, education, and earlier academic experience.")
        body += section("Professional experience", "professional", experience_list(data["experience"]))
        body += section("Education", "education", education_list(data["education"]))
        body += section("Academic experience & service", "academic", experience_list(data["academicExperience"]))
        description = f"Professional experience, education, and academic service of {data['profile']['name']}."
    elif page == "awards":
        body = page_heading("Awards & honors", "Research competition results, scholarships, and academic honors.")
        body += award_list(data["awards"], heading_level=2)
        description = f"Awards and honors received by {data['profile']['name']}."
    elif page == "patents":
        body = page_heading("Patents", "Patent applications and registrations recorded in the full CV.")
        body += patent_list(data["patents"], data["profile"])
        description = f"Patent applications and registrations by {data['profile']['name']}."
    else:
        raise ValueError(f"Unknown archive: {page}")
    return shell(page, data, body, description)


def render(data: dict) -> dict[Path, str]:
    required = {"asOf", "profile", "publications", "projects", "experience", "academicExperience", "education", "awards", "patents"}
    missing = required - data.keys()
    if missing:
        raise ValueError(f"Missing data keys: {', '.join(sorted(missing))}")
    outputs = {ROOT / "index.html": home(data)}
    outputs[ROOT / PAGES["publications"][0]] = publications_page(data)
    for page in ("projects", "experiences", "awards", "patents"):
        outputs[ROOT / PAGES[page][0]] = archive(page, data)
    return {path: "\n".join(line.rstrip() for line in content.splitlines()) + "\n"
            for path, content in outputs.items()}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Report stale generated pages without changing files.")
    args = parser.parse_args()
    data = json.loads(SOURCE.read_text(encoding="utf-8-sig"))
    outputs = render(data)
    stale = []
    for path, content in outputs.items():
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                stale.append(str(path.relative_to(ROOT)))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8", newline="\n")
    if stale:
        print("Generated pages are out of date: " + ", ".join(stale), file=sys.stderr)
        return 1
    print(("Checked" if args.check else "Rendered") + f" {len(outputs)} static pages from src/data/profile.json.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
