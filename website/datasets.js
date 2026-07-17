const datasets = [
  {
    id: "dns_droplet_breakup_hit_we15",
    title: "DNS of Droplet Breakup in HIT (We = 15)",
    summary:
      "Direct numerical simulation data for a liquid droplet breaking up in forced homogeneous isotropic turbulence at Weber number 15.",
    status: "seed",
    modality: "simulation",
    physics: ["VOF", "two-phase flow", "droplet breakup", "homogeneous isotropic turbulence"],
    tasks: ["interface dynamics", "flow-field learning", "DNS analysis"],
    samples: "81 snapshots",
    resolution: "256^3 cells",
    format: "custom binary",
    license: "CC BY 4.0",
    dataUrl: "https://modelscope.cn/datasets/yangqianqi/dns-droplet-breakup-hit-we15",
    detailUrl: "dataset-hit-droplet-breakup.html",
    metadataUrl: "../datasets/dns_droplet_breakup_hit_we15.json"
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
