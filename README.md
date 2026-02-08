# PertPy Perturb-seq Demo 

A reproducible **PertPy** pipeline (pure **`.py` scripts**, VS Code-friendly) demonstrating **perturbation analysis** on an open CRISPR Perturb-seq benchmark dataset:

- **Dataset:** `NormanWeissman2019_filtered.h5ad` (scPerturb standardized AnnData)
- **What this repo does:** downloads the dataset → inspects metadata → prepares labels → builds **pseudobulk** profiles per perturbation → computes **control-difference** profiles → generates PCA/UMAP figures + top-gene tables.


## 1 What you’ll get (outputs)

After running the pipeline, you’ll have:

- **Checkpoint AnnData**
  - `outputs/data/atlas_loaded.h5ad`
  - `outputs/data/atlas_prepared.h5ad`
- **Perturbation / pseudobulk outputs**
  - `outputs/data/pseudobulk_by_condition*.h5ad`
  - `outputs/data/pseudobulk_control_diff*.h5ad`
- **Figures**
  - `outputs/figures/pca_condition_space.png`
  - `outputs/figures/umap_condition_space.png` (if enough pseudobulk points)
- **Tables**
  - `outputs/tables/obs_columns.csv`
  - `outputs/tables/obs_nunique_top30.csv`
  - `outputs/tables/top_genes_per_perturbation_top30.csv`


## 2 Repo structure

```text
pertpy-norman2019-vscode/
├─ data/                         # dataset goes here (gitignore recommended)
├─ outputs/
│  ├─ data/
│  ├─ tables/
│  └─ figures/
├─ scripts/
│  ├─ 00_download_data.py
│  ├─ 01_load_and_inspect.py
│  ├─ 02_prepare_labels.py
│  ├─ 03_pertpy_pseudobulk.py
│  ├─ 04_condition_space_plots.py
│  └─ 05_top_genes_reports.py
├─ requirements.txt
└─ README.md
```


## 3 Quickstart (Windows / VS Code)

### A Create and activate a virtual environment (recommended)
From repo root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### B Install dependencies

```powershell
python -m pip install -U pip
python -m pip install -r requirements.txt
```

> **Important compatibility note (Windows):**
> Some PertPy versions expect **decoupler < 2** for pseudobulk.
> If you see `AttributeError: module 'decoupler' has no attribute 'get_pseudobulk'`,
> run:
>
> ```powershell
> python -m pip uninstall -y decoupler
> python -m pip install "decoupler<2"
> ```

### C Run the pipeline

```powershell
python scripts/00_download_data.py
python scripts/01_load_and_inspect.py
python scripts/02_prepare_labels.py
python scripts/03_pertpy_pseudobulk.py
python scripts/04_condition_space_plots.py
python scripts/05_top_genes_reports.py
```


## 4 Scripts overview

### `00_download_data.py`
Downloads the `.h5ad` dataset into `data/`.

### `01_load_and_inspect.py`
Loads AnnData, prints `.obs` and `.var` info, and saves a checkpoint:
- `outputs/data/atlas_loaded.h5ad`

Also writes metadata summary tables to `outputs/tables/`.

### `02_prepare_labels.py`
Creates a clean perturbation label column:
- `adata.obs["condition"]` (derived from `.obs["perturbation"]` when present)

Stores settings in:
- `adata.uns["pertpy_target_col"] = "condition"`
- `adata.uns["pertpy_control_label"] = "control"` (auto-detected)

Saves:
- `outputs/data/atlas_prepared.h5ad`

### `03_pertpy_pseudobulk.py`
Builds one pseudobulk profile per perturbation and a control-difference layer:
- `pseudobulk_by_condition*.h5ad`
- `pseudobulk_control_diff*.h5ad` (where `.X` is set to `control_diff`)

### `04_condition_space_plots.py`
Runs PCA and optional UMAP on pseudobulk control-diff profiles and saves figures.

### `05_top_genes_reports.py`
For each perturbation, reports genes with highest absolute control-difference (top 30) to CSV.


## 5 Troubleshooting

### A `AttributeError: module 'decoupler' has no attribute 'get_pseudobulk'`
Your `decoupler` version is too new for your PertPy build. Fix:

```powershell
python -m pip uninstall -y decoupler
python -m pip install "decoupler<2"
```

### B `Unable to allocate ... GiB` (memory error during pseudobulk)
Your machine is running out of RAM during sparse conversion / aggregation.

**Recommended fix:** compute pseudobulk on HVGs only (2,000–3,000 genes).
In `03_pertpy_pseudobulk.py`, subset to HVGs before `ps.compute(...)`.

If you prefer a guaranteed low-memory approach, you can switch to a manual
pseudobulk function that works directly on sparse matrices (no CSR conversion).

### C VS Code is using a different Python than your terminal
Check:

```powershell
python -c "import sys; print(sys.executable)"
```

Then VS Code → **Ctrl+Shift+P** → **Python: Select Interpreter** → choose the same path.


## 6 Citation / attribution

If you use this repo in a report or public work, cite:
- Norman *et al.* (2019) Perturb-seq dataset (Weissman lab)
- scPerturb standardized dataset release / repository (AnnData `.h5ad` distribution)



## 7 License
MIT License 





