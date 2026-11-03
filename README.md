# Seongju Lee — research homepage

An academic homepage for Seongju Lee, Senior Researcher at HD Hyundai Robotics.
The homepage presents selected work; the archive pages and downloadable full CV
provide the complete record.

Live site: [seongjulee.github.io](https://seongjulee.github.io/).

## Content and build

`src/data/profile.json` is the website's content source. Edit this file, then
regenerate the committed HTML:

```sh
python scripts/build.py
python scripts/build.py --check
python tests/check_site.py
```

On Windows, `py` can be used in place of `python`. Python 3.10 or newer is
sufficient; no third-party Python packages, JavaScript framework, or build
service is required. All navigation and research content work without JavaScript.

Start a local preview from the repository root:

```sh
python -m http.server 8000 --bind 127.0.0.1
```

Open `http://127.0.0.1:8000/`.

## Updating the research record

- Publication and project `selected` flags control what appears on the homepage.
  `selectedOrder` sets their homepage order; the archive retains all records.
  Selected papers with `selectionGroup: "additional"` appear in the separate
  first-/co-first-author subsection.
- Keep accepted papers, manuscripts in submission, and work in progress in their
  respective categories. `authorRole` describes the recorded author position.
- Citation and journal metrics are a dated snapshot. Update `asOf` only when the
  displayed facts and metrics have been checked. Domestic publications omit
  citation metrics.
- Replace the two PDF snapshots under `assets/docs/` when the CV changes. These
  files are independent of the website build.
- Update biography, contact details, and research interests in `profile`.

Research previews are optional `media` objects on publication or project records:

```json
"media": {
  "src": "assets/media/research/example.gif",
  "poster": "assets/media/research/example-poster.jpg",
  "kind": "gif",
  "alt": "A factual description of the research visualization"
}
```

Most previews are extracted from the author's research presentations; the original
presentations and source videos are not published. The HD Hyundai dual-arm preview
is a company demonstration at FIX 2026, provided by HD Hyundai Robotics through
[NEWSIS](https://nwww.newsis.com/view/NISX20261021_0003835579)
([source GIF](https://img1.newsis.com/2026/10/21/NISI20261021_0002269867_web.gif?rnd=20261021150735)).
It retains the full nine-second scene and original 600?338 resolution.
Optional `media.credit` and `media.sourceUrl` fields display project attribution.

The MART preview (`mart-relations-concept.gif`) is a user-supplied conceptual
animation of pair-wise and overlapping group-wise relations. Its blank lead-in
and fade-out are trimmed; short phase labels and a final hold make it readable
as a homepage thumbnail. It is 640x400, 6.1 seconds, and approximately 641 KB.
The reduced-motion poster shows the complete relation/trajectory illustration.
The original basketball demonstration assets remain available in the repository.

The two maritime project previews each use one edited GIF that connects the
physical platform with real perception footage, using brief crossfades. The
source shots are separate recordings rather than synchronized views.

- `maritime-platform-perception.gif`: the platform photograph from the author's
  interview presentation (slide 4, "Appearance of Platform"), followed by daytime
  and rainy-condition detection recordings (`media12.mp4` and `media13.mp4`).
- `swarm-platform-perception.gif`: platform close-up (01:05-01:07.2), perception
  recording from the same presentation (`media10.mp4`, 00:00.5-00:06.1), then a
  platform group shot (01:07.8-01:10). The platform excerpts are from the
  October 10, 2024 [SBS News report](https://news.sbs.co.kr/news/endPage.do?news_id=N1007828633),
  also linked by the project's [news video](https://www.youtube.com/watch?v=AyBg_Y-ayZ4).
  Full frames and broadcaster marks are retained.

The original standalone perception and platform assets are retained as sources.

The formerly empty main research previews use these original research sources:

| Preview | Source and edit |
| --- | --- |
| CD-FKD | [GIST AI Lab demo](https://www.youtube.com/watch?v=3VRU82IuZ4g), 02:58-03:01 and 03:12-03:15; the CD-FKD result panel in daytime and nighttime scenes. |
| Robust Maritime / JSL | [Official presentation](https://www.youtube.com/watch?v=nJdHN2xWhJM), method diagram from slide 5; the separate Demo clip uses Cam1 then Cam2 at 01:18-01:24. |
| Block Selection | [Original CVPR paper](https://openaccess.thecvf.com/content/CVPR2023/papers/Yu_Block_Selection_Method_for_Using_Feature_Norm_in_Out-of-Distribution_Detection_CVPR_2023_paper.pdf), Figure 2(a), PDF page 2. |
| Active Annotation | [Publisher Figure 1](https://ars.els-cdn.com/content/image/1-s2.0-S266730532600075X-gr1_lrg.jpg), the complete five-phase workflow. |
| Tactile project | [Official project video](https://www.youtube.com/watch?v=ACXip1F-Fh0), 01:44-01:52; simulated grasping and tactile forces, credited as a project simulation. |
| Drone project | [Official project overview](https://sites.google.com/view/gistailab/project/%EB%93%9C%EB%A1%A0), the RGB/IR/LiDAR multi-view diagram. |
| Ceiling project | [Official project example](https://sites.google.com/view/gistailab/project/lg), the input/segmentation image pair; empty black bottom padding removed. |

Optional `media.demo` links to a local demonstration clip alongside a still
preview. Source figures preserve their meaningful panels and annotations.

Keep a poster for every GIF so reduced-motion preferences use a still frame.
Entries without media retain an empty preview area, except additional first-author
papers, which use a text-only layout. Nothing is fabricated to fill a preview.
The optional CV importer preserves existing media mappings by record ID.

The initial content was imported from the CV's full/selected LaTeX sources. The
optional importer supports that specific template:

```sh
python scripts/import_cv.py /path/to/curriculum_vitae_seongju_lee --as-of YYYY-MM-DD
python scripts/build.py
python tests/check_site.py
```

Importing regenerates `profile.json`, including its biography defaults. Review
the diff and the verification date before committing an imported snapshot.

## Files and publishing

- `index.html`: selected publications, projects, experience, education, and awards.
- `src/pages/`: complete publications, projects, experience, awards, and patents;
  existing page URLs are preserved.
- `assets/css/site.css`: responsive layout and typography.
- `assets/images/profile/`: the existing profile photograph.
- `assets/media/research/`: optimized research GIFs and still posters.
- `assets/docs/`: full and selected CV PDFs.
- `scripts/build.py`: static page renderer and freshness check.
- `tests/check_site.py`: generated content, links, assets, and HTML structure checks.

GitHub Pages serves the committed static files from the repository's configured
publishing branch. Commit regenerated HTML together with source changes; Pages
does not need to run Python. `.nojekyll` keeps the deployment static.
