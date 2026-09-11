#!/usr/bin/env python3
"""Generate website/dataset-{id}.html pages from datasets/*.json records.

Records use the flat issue-field structure written by issue_to_json.py.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATASETS_DIR = ROOT / "datasets"
PAGES_DIR = ROOT / "website"

HTML_TEMPLATE = """<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{title} | Multiphase Data Hub</title>
    <link rel="stylesheet" href="styles.css" />
  </head>
  <body>
    <header class="page-header">
      <div class="site-nav"><nav class="nav" aria-label="Primary navigation">
        <a class="brand" href="index.html">Multiphase Data Hub</a>
        <div class="nav-links">
          <a href="datasets.html">Datasets</a>
          <a href="standard.html">Standard</a>
          <a href="contribute.html">Contribute</a>
          <a href="hosting.html">Hosting</a>
          <a href="governance.html">Governance</a>
          <a href="about.html">About</a>
        </div>
      </nav></div>
      <div class="page-title">
        <p class="eyebrow">{status_label}</p>
        <h1>{title}</h1>
        <p>{subtitle}</p>
      </div>
    </header>

    <main>
      <section class="section detail-hero">
        {detail_images_inline}
        <div>
          <p class="eyebrow">Description</p>
          <p class="section-copy">{description}</p>
          <div class="download-actions">
            {open_button}
          </div>
        </div>
      </section>
{cases_section}

      <section class="section band">
        <h2 id="quick-info">Quick Info</h2>
        <ul class="quick-info-list">
          {quick_info_items}
        </ul>
      </section>
    </main>

    <footer class="footer">
      <span>Multiphase Data Hub</span>
      <span>{title}</span>
    </footer>
  </body>
</html>
"""


def _short_status(status: str) -> str:
    for suffix in ("_dataset", " dataset"):
        if status.endswith(suffix):
            return status[: -len(suffix)]
    return status


def build_page(record: dict) -> str | None:
    dataset_id = record.get("id", "")
    if not dataset_id:
        print("Skipping record without id")
        return None

    title = (record.get("title") or "Untitled").strip()
    subtitle = (record.get("subtitle") or "").strip()
    description = (record.get("description") or "").strip()
    status = _short_status(record.get("status", "seed"))
    status_label = status.capitalize() + " dataset"

    image = (record.get("preview") or "").strip()
    if image.startswith("website/"):
        image = image[len("website/"):]
    if not image:
        image = "assets/placeholder.png"

    access_links = [
        s.strip() for s in (record.get("access_link") or "").split(";") if s.strip()
    ]
    metadata_links = [
        s.strip() for s in (record.get("metadata_link") or "").split(";") if s.strip()
    ]

    try:
        case_count = int(record.get("case_count") or 1)
    except (TypeError, ValueError):
        case_count = 1
    if case_count < 1:
        case_count = 1

    if case_count <= 1 and access_links:
        host = record.get("hosting_platform", "ModelScope")
        open_button = (
            f'<a class="button primary" href="{access_links[0]}">Open on {host}</a>'
        )
    else:
        open_button = ""

    cases_section = ""
    if case_count > 1:
        rows: list[str] = []
        total = max(len(access_links), len(metadata_links))
        for i in range(total):
            acc = access_links[i] if i < len(access_links) else ""
            meta = metadata_links[i] if i < len(metadata_links) else ""
            acc_td = f'<a class="text-link" href="{acc}">{acc}</a>' if acc else "-"
            meta_td = f'<a class="text-link" href="{meta}">info.json</a>' if meta else "-"
            rows.append(f"<tr><td>{acc_td}</td><td>{meta_td}</td></tr>")
        cases_section = (
            '<section class="section">'
            '<p class="eyebrow">Cases</p>'
            '<h2>Dataset and metadata links</h2>'
            '<table class="data-table"><thead><tr>'
            "<th>Dataset link</th><th>info.json</th>"
            "</tr></thead><tbody>"
            + "".join(rows)
            + "</tbody></table></section>"
        )

    detail_images = record.get("detail_images", [])
    if isinstance(detail_images, str):
        detail_images = [detail_images]
    detail_imgs = []
    for d_img in detail_images:
        d_img = (d_img or "").strip()
        if not d_img:
            continue
        if d_img.startswith("website/"):
            d_img = d_img[len("website/"):]
        detail_imgs.append(f'<img src="{d_img}" alt="{title}" />')
    if detail_imgs:
        detail_images_inline = "".join(detail_imgs)
    else:
        detail_images_inline = ""

    items: list[str] = []
    if case_count <= 1:
        if access_links:
            items.append(f'<li><a class="text-link" href="{access_links[0]}">Dataset link</a></li>')
        if metadata_links:
            items.append(f'<li><a class="text-link" href="{metadata_links[0]}">info.json</a></li>')
    contributors = (record.get("contributors") or "").strip()
    if contributors:
        items.append(f"<li>Contributors: {contributors}</li>")
    contact = (record.get("contact") or "").strip()
    if contact:
        items.append(f"<li>Contact: {contact}</li>")
    doi = (record.get("doi") or "").strip()
    if doi:
        items.append(f'<li><a class="text-link" href="https://doi.org/{doi}">DOI</a></li>')
    license_str = (record.get("license") or "").strip()
    if license_str:
        items.append(f"<li>License: {license_str}</li>")
    grid = (record.get("grid") or "").strip()
    if grid:
        items.append(f"<li>Grid: {grid}</li>")
    field_location = (record.get("field_location") or "").strip()
    if field_location:
        items.append(f"<li>Field location: {field_location}</li>")
    samples = (record.get("samples") or "").strip()
    if samples:
        items.append(f"<li>Samples / snapshots: {samples}</li>")
    format_str = (record.get("format") or "").strip()
    if format_str:
        items.append(f"<li>Format: {format_str}</li>")
    size = (record.get("size") or "").strip()
    if size:
        items.append(f"<li>Size: {size}</li>")
    case_condition = (record.get("case_condition") or "").strip()
    if case_condition:
        items.append(f"<li>Case conditions: {case_condition}</li>")
    file_format = (record.get("file_format") or "").strip()
    if file_format:
        items.append(f"<li>Loading instructions: {file_format}</li>")

    quick_info_items = "\n          ".join(items)

    return HTML_TEMPLATE.format(
        title=title,
        subtitle=subtitle,
        description=description,
        status_label=status_label,
        open_button=open_button,
        cases_section=cases_section,
        detail_images_inline=detail_images_inline,
        quick_info_items=quick_info_items,
    )


def main() -> int:
    if not DATASETS_DIR.exists():
        print("datasets/ directory not found")
        return 1

    json_files = sorted(DATASETS_DIR.glob("*.json"))
    if not json_files:
        print("No dataset JSON files found; cleaning orphan pages")

    generated = 0
    records = []
    for path in json_files:
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            print(f"Skipping {path.name}: invalid JSON ({exc})")
            continue

        page = build_page(record)
        if page is None:
            continue

        records.append(record)
        dataset_id = record.get("id", "")
        output_path = PAGES_DIR / f"dataset-{dataset_id}.html"
        output_path.write_text(page, encoding="utf-8")
        print(f"Generated {output_path.name}")
        generated += 1

    # Remove orphaned detail pages for deleted dataset JSONs
    existing_pages = set(PAGES_DIR.glob("dataset-*.html"))
    expected_ids = {r.get("id", "") for r in records}
    for page_path in sorted(existing_pages):
        page_id = page_path.stem.replace("dataset-", "")
        if page_id not in expected_ids:
            page_path.unlink()
            print(f"Removed orphan page: {page_path.name}")

    print(f"Generated {generated} dataset detail page(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
