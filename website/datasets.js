// Auto-generated from datasets/*.json -- do not edit manually.
const datasets = [
  {
    "id": "droplet-breakup-in-hit-20260911-013152",
    "title": "Droplet breakup in HIT",
    "subtitle": "Direct numerical simulation data of a liquid droplet breaking up in forced homogeneous isotropic turbulence at Weber number 15",
    "status": "seed",
    "tags": [
      "interface dynamics",
      "flow-field learning",
      "VOF",
      "droplet breakup",
      "homogeneous isotropic turbulence",
      "DNS analysis"
    ],
    "samples": "81",
    "grid": "Nx=256, Ny=256, Nz=256",
    "fieldLocation": "cell-centered",
    "format": "custom binary",
    "license": "CC-BY-4.0",
    "size": "27.18 GB",
    "imageUrl": "assets/droplet-breakup-in-hit-20260911-013152/cover.png",
    "dataUrl": "https://modelscope.cn/datasets/yangqianqi/dns-droplet-breakup-hit-we15",
    "detailUrl": "dataset-droplet-breakup-in-hit-20260911-013152.html",
    "caseCount": 1
  },
  {
    "id": "droplet-breakup-in-hit-20260911-090201",
    "title": "Droplet breakup in HIT",
    "subtitle": "Direct numerical simulation data of a liquid droplet breaking up in forced homogeneous isotropic turbulence at Weber number 15",
    "status": "community",
    "tags": [
      "two-phase flow"
    ],
    "samples": "81",
    "grid": "Nx=256",
    "fieldLocation": "cell-centered",
    "format": "custom binary",
    "license": "CC-BY-4.0",
    "size": "27.18 GB",
    "imageUrl": "assets/droplet-breakup-in-hit-20260911-090201/cover.png",
    "dataUrl": "https://modelscope.cn/datasets/yangqianqi/dns-droplet-breakup-hit-we15",
    "detailUrl": "dataset-droplet-breakup-in-hit-20260911-090201.html",
    "caseCount": 1
  }
];

const grid = document.querySelector("#dataset-grid");
const search = document.querySelector("#dataset-search");
const count = document.querySelector("#dataset-count");
const caseTotal = document.querySelector("#case-total");
if (caseTotal) {
  const totalCases = datasets.reduce((sum, d) => sum + (d.caseCount || 1), 0);
  caseTotal.textContent = String(totalCases);
}

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
