# Perturb-seq Analysis with PertPy

A reproducible computational workflow for analyzing CRISPR Perturb-seq data using **PertPy, Scanpy, Python, and Snakemake**.

This project uses the Norman et al. (2019) CRISPR Perturb-seq benchmark dataset to characterize transcriptional responses to genetic perturbations and identify perturbations that produce distinct transcriptional phenotypes relative to control cells.

> **Project status:** Complete core analysis; workflow automation and containerization in progress.

---

## Overview

Perturb-seq combines pooled genetic perturbation with single-cell RNA sequencing to measure how targeted perturbations affect cellular transcriptional states.

This project explores a reproducible analysis workflow that:

1. Loads and inspects a standardized Perturb-seq dataset
2. Prepares perturbation and control labels
3. Generates pseudobulk expression profiles for individual perturbations
4. Calculates perturbation-vs-control transcriptional differences
5. Characterizes perturbation-specific gene-level effects
6. Identifies perturbations with the largest overall transcriptional deviations from control
7. Projects perturbations into transcriptional space using PCA and UMAP
8. Produces reproducible tables and visualizations
9. Orchestrates the complete analysis using Snakemake

The workflow is designed to separate **scientific analysis from workflow orchestration**, making individual analysis components reusable and allowing the complete workflow to be reproduced from a clean environment.

---

## Scientific Question

### Which perturbations produce the most distinct transcriptional phenotypes relative to controls?

Rather than only examining individual differentially affected genes, this project represents each perturbation as a transcriptional effect profile relative to control cells.

For a perturbation (P) and control profile (C):

[E_P = P - C]

where (E_P) represents the transcriptional effect associated with perturbation (P).

The overall magnitude of this effect is then quantified to identify perturbations producing the largest transcriptomic deviations from control.

This provides a complementary perspective to gene-level analysis:

* **Gene-level analysis:** Which genes are most strongly affected by each perturbation?
* **Perturbation-level analysis:** Which perturbations produce the strongest overall transcriptional phenotype?

---

## Dataset

The analysis uses the **Norman & Weissman 2019 CRISPR Perturb-seq dataset**, distributed as a standardized AnnData object through the scPerturb ecosystem.

The dataset contains single-cell transcriptomic profiles associated with genetic perturbations and control conditions.

The original tutorial that inspired this project is available here:

https://github.com/TaufiaHussain/pertpy-perturbation-analysis

This repository extends that workflow with additional perturbation-level analysis and workflow automation.

---

## Analysis Workflow

```text
             Norman & Weissman
             Perturb-seq Data
                    │
                    ▼
           Load & Inspect Data
                    │
                    ▼
        Prepare Perturbation Labels
                    │
                    ▼
              Pseudobulk
         Profiles per Perturbation
                    │
                    ▼
        Perturbation − Control
          Expression Profiles
                    │
          ┌─────────┴─────────┐
          ▼                   ▼
     Gene-level           Perturbation-level
       effects                 effects
          │                   │
          ▼                   ▼
    Top affected          Effect magnitude
        genes                 ranking
          │                   │
          └─────────┬─────────┘
                    ▼
          Perturbation Space
             PCA / UMAP
                    │
                    ▼
          Biological Interpretation
```

---

## Repository Structure

```text
pertpy-perturbation-analysis/
├── data/
│   └──                       # Local dataset; not tracked by Git
│
├── outputs/
│   ├── data/                 # Intermediate AnnData objects
│   ├── figures/              # PCA / UMAP visualizations
│   └── tables/               # Analysis results
│
├── scripts/
│   ├── 00_download_data.py
│   ├── 01_load_and_inspect.py
│   ├── 02_prepare_labels.py
│   ├── 03_pertpy_pseudobulk.py
│   ├── 04_condition_space_plots.py
│   ├── 05_top_genes_reports.py
│   └── 06_perturbation_effects.py
│
├── Snakefile
├── requirements.txt
├── Dockerfile
├── README.md
└── LICENSE
```

---

## Pipeline Components

### 1. Dataset Download

`00_download_data.py`

Downloads the standardized Perturb-seq AnnData dataset and stores it locally.

### 2. Dataset Inspection

`01_load_and_inspect.py`

Examines the AnnData object, including cell-level metadata and available annotations, and generates checkpoint and metadata summary files.

### 3. Perturbation Label Preparation

`02_prepare_labels.py`

Creates a standardized perturbation label used throughout the PertPy workflow and identifies the appropriate control condition.

### 4. Pseudobulk Analysis

`03_pertpy_pseudobulk.py`

Generates one pseudobulk transcriptional profile per perturbation and calculates perturbation-vs-control expression differences.

The resulting AnnData object contains the `control_diff` representation used for downstream analysis.

### 5. Perturbation Space Visualization

`04_condition_space_plots.py`

Projects perturbation-level transcriptional profiles into lower-dimensional space using PCA and UMAP.

These representations allow perturbations with similar transcriptional phenotypes to be compared.

### 6. Gene-level Perturbation Effects

`05_top_genes_reports.py`

For each perturbation, identifies the genes exhibiting the largest absolute transcriptional differences relative to control.

The resulting table contains:

* perturbation
* rank
* gene
* control difference
* absolute difference

### 7. Perturbation-level Effect Analysis

`06_perturbation_effects.py`

Quantifies the overall magnitude of transcriptional change associated with each perturbation.

The analysis reports:

* overall transcriptional effect magnitude
* mean absolute gene-level change
* maximum individual gene-level change
* number of genes contributing to the calculation

Perturbations can then be ranked according to the magnitude of their transcriptional phenotype.

---

## Outputs

Representative outputs include:

### Intermediate data

```text
outputs/data/atlas_loaded.h5ad
outputs/data/atlas_prepared.h5ad
outputs/data/pseudobulk_by_condition*.h5ad
outputs/data/pseudobulk_control_diff*.h5ad
```

### Figures

```text
outputs/figures/pca_condition_space.png
outputs/figures/umap_condition_space.png
```

### Tables

```text
outputs/tables/obs_columns.csv
outputs/tables/obs_nunique_top30.csv
outputs/tables/top_genes_per_perturbation_top30.csv
outputs/tables/perturbation_transcriptional_effects.csv
```

---

## Reproducibility

The analysis is orchestrated using **Snakemake**, with individual Python scripts responsible for the scientific analysis.

The intended workflow is:

```bash
snakemake --cores 4
```

```bash
docker run --rm pertpy-analysis

docker run --rm \
  -v "$(pwd):/workspace" \
  pertpy-analysis

docker run --rm \
  -v "/path/to/my/project:/workspace" \
  pertpy-analysis

docker run --rm -it \
  -v "$(pwd):/workspace" \
  pertpy-analysis \
  bash
```

This allows the complete analysis to be reproduced from the workflow definition while preserving intermediate outputs and dependencies between analysis stages.

---

## Technologies

### Biological analysis

* Perturb-seq
* single-cell RNA sequencing
* pseudobulk analysis
* perturbation analysis
* transcriptional profiling

### Computational tools

* Python
* Scanpy
* PertPy
* AnnData
* NumPy
* Pandas
* Matplotlib

### Reproducibility & infrastructure

* Snakemake
* Docker
* Git / GitHub

---

## What I Learned

This project was undertaken to develop hands-on experience with **Perturb-seq and perturbational single-cell analysis**.

My previous computational biology work has focused on single-cell and spatial transcriptomics, DNA methylation, multi-omics analysis, machine learning, and reproducible bioinformatics workflows. Perturb-seq provides a natural extension of these skills by adding an explicit experimental perturbation to single-cell transcriptomic profiling.

The project also provided an opportunity to explore how perturbation-level representations can be used to move from conventional cell-level analysis toward characterization of **functional transcriptional phenotypes**.

---

## Attribution

This project builds upon the original PertPy Perturb-seq workflow developed by **Taufia Hussain**:

https://github.com/TaufiaHussain/pertpy-perturbation-analysis

The original workflow was reproduced and subsequently extended with:

* perturbation-level transcriptional effect analysis
* additional result tables
* Snakemake workflow orchestration
* Docker-based reproducibility

The underlying dataset is based on the Norman et al. (2019) Perturb-seq study and its standardized scPerturb distribution.

Please refer to the original repository and associated publications for the original analysis and dataset attribution.

---

## License

MIT License
