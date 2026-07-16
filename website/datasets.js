const datasets = [
  {
    id: "hit_droplet_breakup_ensight_gvol_gcurv_v_subset",
    title: "HIT Droplet Breakup: Gvol, Gcurv, and Velocity",
    summary:
      "Raw EnSight Gold subset from a 3D droplet breakup case in homogeneous isotropic turbulence, including selected Gvol, Gcurv, and velocity snapshots.",
    status: "seed",
    modality: "simulation",
    physics: ["VOF", "two-phase flow", "droplet breakup", "homogeneous isotropic turbulence"],
    tasks: ["interface dynamics", "curvature analysis", "flow-field learning"],
    samples: "67 snapshots",
    resolution: "256^3 cells",
    format: "EnSight Gold binary",
    license: "TBD",
    dataUrl: "https://modelscope.cn/datasets/yangqianqi/dns-droplet-breakup-hit-we15",
    detailUrl: "dataset-hit-droplet-breakup.html",
    metadataUrl: "../datasets/hit_droplet_breakup_ensight_gvol_gcurv_v_subset.json"
  }
];

const grid = document.querySelector("#dataset-grid");
const search = document.querySelector("#dataset-search");
const count = document.querySelector("#dataset-count");

function render(items) {
  if (count) {
    count.textContent = String(datasets.length);
  }

  grid.innerHTML = items
    .map(
      (dataset) => `
      <article class="dataset-card">
        <div>
          <p class="eyebrow">${dataset.status} dataset</p>
          <h3>${dataset.title}</h3>
          <p>${dataset.summary}</p>
        </div>
        <div class="tags">
          ${[...dataset.physics, ...dataset.tasks].map((tag) => `<span class="tag">${tag}</span>`).join("")}
        </div>
        <div class="meta">
          <span><strong>Samples</strong>${dataset.samples}</span>
          <span><strong>Resolution</strong>${dataset.resolution}</span>
          <span><strong>Format</strong>${dataset.format}</span>
          <span><strong>License</strong>${dataset.license}</span>
        </div>
        <div class="card-actions">
          <a href="${dataset.detailUrl}">Dataset page</a>
          <a href="${dataset.dataUrl}">ModelScope</a>
          <a href="${dataset.metadataUrl}">Metadata JSON</a>
        </div>
      </article>
    `
    )
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
