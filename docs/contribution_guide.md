# Contribution Guide

The goal is to make dataset submission easy while keeping the catalogue useful
for reproducible research.

## Submission Workflow

1. Host the dataset on a stable external platform.
2. Add a metadata JSON file under `datasets/`.
3. Add preview figures when available.
4. Open a pull request.
5. Maintainers review metadata completeness, link stability, license clarity,
   and basic scientific provenance.

## Hosting Recommendations

Recommended public hosts:

- ModelScope for China-accessible public dataset hosting;
- Kaggle for international machine-learning community access;
- Zenodo for DOI-backed archival releases;
- Figshare or institutional repositories for citable data packages;
- Hugging Face Datasets for ML-friendly public access;
- project object storage for very large datasets, with clear persistence notes.

The website repository should not store large data archives.

## Platform Summary

The detailed internal upload tutorials are intentionally not copied into the
public website. The public contribution pages should show only the durable
workflow:

- prepare a readable data package;
- include `README.md`, `info.json`, data files, checksums, and a loading example
  for solver-specific binary formats;
- upload to ModelScope, Kaggle, Zenodo, or institutional storage;
- submit the public landing page and metadata record for catalogue review.

Operational details such as API tokens, proxy settings, and account-specific
commands should remain outside the public website.

## Minimum Acceptance Criteria

A submitted dataset should have:

- explicit license;
- clear citation;
- working download link;
- documented variable names, units, and shapes;
- provenance information;
- at least one contact person;
- enough documentation for an external user to load a sample.

For Kaggle-hosted multiphase-flow datasets, follow
`docs/kaggle_dataset_package_standard.md`. The required core files are
`dataset-metadata.json`, `info.json`, and the data files. `load_example.py` is
mandatory for custom or solver-specific binary files and strongly recommended
for all datasets.

## Review Categories

Dataset records can be marked as:

- `draft`: metadata exists but the data is not ready for public reuse;
- `seed`: internally contributed dataset used to establish the standard;
- `community`: external community contribution;
- `benchmark`: curated dataset with fixed splits and metrics;
- `archived`: retained for citation but not actively maintained.
