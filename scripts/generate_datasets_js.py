#!/usr/bin/env python3
"""Generate website/datasets.js from datasets/*.json catalogue records.

Records use the flat issue-field structure written by issue_to_json.py.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATASETS_DIR = ROOT / "datasets"
OUTPUT = ROOT / "website" / "datasets.js"


def _short_status(status: str) -> str:
    for suffix in ("_dataset", " dataset"):
        if status.endswith(suffix):
            return status[: -len(suffix)]
    return status


def build_entry(record: dict) -> dict:
    title = (record.get("title") or "").strip()
    subtitle = (record.get("subtitle") or "").strip()
    keywords = (record.get("keywords") or "").strip()
    tags = [k.strip() for k in keywords.split(",") if k.strip()]

    preview = (record.get("preview") or "").strip()
    if preview.startswith("website/"):
        preview = preview[len("website/"):]

    access_links = [
        s.strip() for s in (record.get("access_link") or "").split(";") if s.strip()
    ]
    data_url = access_links[0] if access_links else ""

    try:
        case_count = int(record.get("case_count") or 1)
    except (TypeError, ValueError):
        case_count = 1
    if case_count < 1:
        case_count = 1

    return {
        "id": record.get("id", ""),
        "title": title,
        "subtitle": subtitle,
        "status": _short_status(record.get("status", "seed")).lower(),
        "tags": tags,
        "samples": (record.get("samples") or "").strip(),
        "grid": (record.get("grid") or "").strip(),
        "fieldLocation": (record.get("field_location") or "").strip(),
        "format": (record.get("format") or "").strip(),
        "license": (record.get("license") or "").strip(),
        "size": (record.get("size") or "").strip(),
        "imageUrl": preview,
        "dataUrl": data_url,
        "detailUrl": f"dataset-{record.get('id', 'unknown')}.html",
        "caseCount": case_count,
    }


def main() -> int:
    if not DATASETS_DIR.exists():
        print("datasets/ directory not found, skipping")
        return 1

    json_files = sorted(DATASETS_DIR.glob("*.json"))
    if not json_files:
        print("No dataset JSON files found; writing empty list")

    entries = []
    for path in json_files:
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
            entries.append(build_entry(record))
        except (json.JSONDecodeError, KeyError) as exc:
            print(f"Warning: skipping {path.name}: {exc}")

    header = "// Auto-generated from datasets/*.json -- do not edit manually.\n"
    data_block = f"const datasets = {json.dumps(entries, indent=2, ensure_ascii=False)};\n\n"

    render_logic = """\
const grid = document.querySelector("#dataset-grid");
const search = document.querySelector("#dataset-search");
const count = document.querySelector("#dataset-count");

function caseLabel(n) {
  return n > 1 ? "(" + n + " cases)" : "(1 case)";
}

function render(items) {
  if (count) {
    count.textContent = String(datasets.length);
  }

  if (grid.dataset.layout === "gallery") {
    grid.innerHTML = items
      .map(
        (dataset) => `
        <article class="dataset-tile">
          <a href="${dataset.detailUrl}" aria-label="${dataset.title}">
            <img src="${dataset.imageUrl}" alt="${dataset.title}" />
            <span>${dataset.title}</span>
            <small class="case-count">${caseLabel(dataset.caseCount)}</small>
          </a>
        </article>
      `
      )
      .join("");
    return;
  }

  grid.innerHTML = items
    .map((dataset) => {
      const tagsHtml = dataset.tags && dataset.tags.length
        ? `<div class="tags">${dataset.tags.map((tag) => `<span class="tag">${tag}</span>`).join("")}</div>`
        : "";

      const meta = [];
      if (dataset.samples) meta.push(`<span><strong>Samples</strong>${dataset.samples}</span>`);
      if (dataset.grid) meta.push(`<span><strong>Grid</strong>${dataset.grid}</span>`);
      if (dataset.fieldLocation) meta.push(`<span><strong>Field location</strong>${dataset.fieldLocation}</span>`);
      if (dataset.format) meta.push(`<span><strong>Format</strong>${dataset.format}</span>`);
      if (dataset.license) meta.push(`<span><strong>License</strong>${dataset.license}</span>`);
      if (dataset.size) meta.push(`<span><strong>Size</strong>${dataset.size}</span>`);
      const metaHtml = meta.length ? `<div class="meta">${meta.join("")}</div>` : "";

      const modelScopeLink = (dataset.caseCount <= 1 && dataset.dataUrl)
        ? `<a href="${dataset.dataUrl}">ModelScope</a>`
        : "";

      return `
      <article class="dataset-card">
        <div>
          <p class="eyebrow">${dataset.status} dataset</p>
          <h3>${dataset.title}</h3>
          ${dataset.subtitle ? `<p>${dataset.subtitle}</p>` : ""}
          <p class="case-count">${caseLabel(dataset.caseCount)}</p>
        </div>
        ${tagsHtml}
        ${metaHtml}
        <div class="card-actions">
          <a href="${dataset.detailUrl}">Dataset page</a>
          ${modelScopeLink}
        </div>
      </article>`;
    })
    .join("");
}

if (grid && search) {
  search.addEventListener("input", (event) => {
    const query = event.target.value.toLowerCase().trim();
    const filtered = datasets.filter((dataset) =>
      JSON.stringify(dataset).toLowerCase().includes(query)
    );
    render(filtered);
  });

  render(datasets);
}
"""

    OUTPUT.write_text(header + data_block + render_logic, encoding="utf-8")
    print(f"Generated {OUTPUT} with {len(entries)} dataset(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
