# Kaggle Dataset Package Standard for Multiphase-Flow Data

The goal is practical reuse: a downloader should be able to read the uploaded
field data with Python and construct task-specific training, testing, or
visualization datasets.

The data format is not forced, but metadata must be clear, variables must be
defined, and at least one sample should be readable without private code.

## Recommended Package Structure

Each Kaggle dataset should contain:

```text
dataset-metadata.json
info.json
README.md
load_example.py
checksums.sha256
data/
```

Required:

```text
dataset-metadata.json
info.json
data/
```

Strongly recommended:

```text
load_example.py
README.md
checksums.sha256
```

## `dataset-metadata.json`

This file is required by Kaggle.

Following the BlastNet tutorial, it is usually generated automatically by:

```bash
kaggle datasets init -p <path/to/dataset>
```

After generation, edit:

```json
{
  "title": "Dataset title",
  "id": "kaggle-user/dataset-slug",
  "licenses": [
    {
      "name": "CC-BY-4.0"
    }
  ]
}
```

The owner in `id` must match the Kaggle username.

## `info.json`

`info.json` is the authoritative metadata file.

It should contain:

```text
global: dataset-level information
local: snapshot/case/sample-level file paths and time information
```

Required `global` information:

- dataset id;
- title;
- description;
- format;
- number of snapshots or samples;
- variables;
- grid;
- physics;
- contributors;
- license;
- DOI or citation note;
- known limitations.

Required `local` information:

- snapshot or sample id;
- time, if available;
- file paths for variables included in that snapshot/sample.

`info.json` must match the actual uploaded files. If only `Gvol` is uploaded,
do not list missing `V` or `P` files as available.

## `data/`

`data/` stores the actual field data.

Accepted data types include:

```text
1. Preprocessed array formats:
   .npy, .npz, .h5, .hdf5, .zarr, NetCDF

2. Common CFD or visualization formats:
   .dat, .vtk, .vti, .vtu, .vtr, .xdmf + .h5, EnSight, OpenFOAM

3. Solver-specific binary files without standard extensions:
   Gvol.000001, V.000001, P.000001, VOF.000001
```

For the first two types, document variables, shapes, units, grid, and reading
method in `info.json`.

For solver-specific binary files, additionally document:

- header bytes;
- dtype;
- endianness;
- payload shape;
- vector component layout;
- reshape order;
- file path pattern;
- units;
- grid dimensions and coordinate convention.

For solver-specific binary files, `load_example.py` is mandatory.

## Required Multiphase Variables

For a complete two-phase or multiphase CFD dataset, the recommended required
variable groups are:

```text
velocity
pressure
interface variable
```

Examples:

```text
velocity: u, v, w, or V
pressure: p or P
interface: alpha, Gvol, VOF, phi, level-set, interface mask
```

The interface phase convention must be documented, for example whether `Gvol=1`
means liquid or gas.

Optional variables include:

```text
curvature: kappa, Gcurv
normal vector: normal, Gnorm
density field: rho
viscosity field: mu
temperature: T
species: Y_i
vorticity, strain rate, dissipation, and other diagnostics
```

If `rho`, `mu`, `sigma`, or `g` are fixed case parameters, they should usually
be stored in metadata rather than uploaded as field variables.

## `load_example.py`

Strongly recommended for all datasets and mandatory for solver-specific binary
files.

The script should:

- run from the dataset root;
- read at least one snapshot or sample;
- print variable names, shapes, dtype, min, and max;
- avoid private code;
- use common Python packages when possible.

## `README.md`

Recommended but should remain short. It does not need to repeat all details in
`info.json`.

Suggested content:

```text
dataset name
one-paragraph description
included variables
see info.json for full metadata
see load_example.py for Python reading
citation or DOI
```

## `checksums.sha256`

Recommended for file-integrity verification.

Generate with:

```bash
find . -type f ! -name checksums.sha256 -print0 | sort -z | xargs -0 sha256sum > checksums.sha256
```

## Optional Files

Include as needed:

```text
figures/
scripts/
grid/
metadata/
case files
mesh files
```

For uniform Cartesian grids, coordinate files are not required if `info.json`
fully specifies dimensions, bounds, spacing, coordinate order, and field
location. If the grid cannot be reconstructed from metadata, upload mesh,
coordinate, or geometry files.

## Upload Checklist

Before uploading or submitting a dataset, verify:

- `dataset-metadata.json` exists and has the correct Kaggle owner id;
- `info.json` exists;
- all file paths listed in `info.json` exist;
- velocity, pressure, and interface variables are included, or missing groups
  are explicitly explained;
- units, shapes, and dtype are documented;
- grid reconstruction is possible;
- phase convention is documented;
- at least one sample can be read with Python;
- solver-specific binary files include `load_example.py`;
- license and citation information are clear.

