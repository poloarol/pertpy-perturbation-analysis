# Perturb-seq Analysis with PertPy

A reproducible and containerized workflow for analyzing CRISPR Perturb-seq data using **PertPy, Scanpy, Python, Snakemake, and Docker**.

This project analyzes the Norman & Weissman 2019 CRISPR Perturb-seq benchmark dataset to characterize transcriptional responses to genetic perturbations and identify perturbations that produce distinct transcriptional phenotypes relative to control cells.

> **Project status:** Core analysis, workflow automation, and containerization complete.

---

## Overview

Perturb-seq combines pooled genetic perturbation with single-cell RNA sequencing to measure how targeted genetic perturbations alter cellular transcriptional states.

This project explores a reproducible computational workflow that:

* Loads and inspects a standardized Perturb-seq dataset
* Prepares perturbation and control labels
* Generates pseudobulk expression profiles for individual perturbations
* Calculates perturbation-vs-control transcriptional differences
* Identifies genes with the largest perturbation-specific effects
* Quantifies the overall transcriptional effect of each perturbation
* Ranks perturbations according to their transcriptional effect size
* Projects perturbations into transcriptional space using PCA and UMAP
* Generates reproducible tables and visualizations
* Automates the complete analysis using Snakemake
* Packages the analysis environment using Docker

The workflow separates **scientific analysis from workflow orchestration**, allowing individual analysis components to be reused while making the complete pipeline reproducible.

---

## Scientific Question

### Which perturbations produce the most distinct transcriptional phenotypes relative to controls?

Rather than examining only individual differentially affected genes, each perturbation is represented by its transcriptional difference relative to control.

For perturbation (P) and control profile (C):

[
E_P = P - C
]

where (E_P) represents the transcriptional effect associated with perturbation (P).

The overall magnitude of this effect is used to rank perturbations according to the extent of their transcriptional deviation from control.

This provides two complementary levels of analysis:

| Analysis           | Question                                                                     |
| ------------------ | ---------------------------------------------------------------------------- |
| Gene-level         | Which genes are most strongly affected by each perturbation?                 |
| Perturbation-level | Which perturbations produce the strongest overall transcriptional phenotype? |

---

## Workflow

```text
                  Perturb-seq Dataset
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
             ┌───────────┴───────────┐
             ▼                       ▼
       Gene-level Effects     Perturbation-level
             │                   Effects
             ▼                       ▼
      Top Affected Genes       Effect Magnitude
             │                       │
             └───────────┬───────────┘
                         ▼
                Perturbation Space
                   PCA / UMAP
                         │
                         ▼
              Biological Interpretation
```

---

## Pipeline

The complete analysis is orchestrated using **Snakemake**.

```text
download_data
      │
      ▼
load_and_inspect
      │
      ▼
prepare_labels
      │
      ▼
pseudobulk
      │
      ├───────────────┐
      ▼               ▼
condition_space    top_genes
      │               │
      │               ▼
      │          gene-level effects
      │
      └───────────────┐
                      ▼
              top_perturbation_report
                      │
                      ▼
             ranked perturbations
```

The workflow is defined in `Snakefile`, while individual scientific analyses are implemented as Python scripts in `src/`.

---

## Repository Structure

```text
pertpy-perturbation-analysis/
│
├── src/
│   ├── 00_download_data.py
│   ├── 01_load_and_inspect.py
│   ├── 02_prepare_labels.py
│   ├── 03_pertpy_pseudobulk.py
│   ├── 04_condition_space_plots.py
│   ├── 05_top_genes_reports.py
│   └── 06_top_pertubations_report.py
│
├── data/
│   └── NormanWeissman2019_filtered.h5ad
│
├── results/
│   ├── data/
│   ├── figures/
│   └── tables/
│
├── Snakefile
├── Dockerfile
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

The dataset and generated results are excluded from version control where appropriate.

---

## Analysis Components

### 1. Dataset Download

`src/00_download_data.py`

Downloads the standardized Norman & Weissman 2019 Perturb-seq dataset.

### 2. Dataset Inspection

`src/01_load_and_inspect.py`

Loads the AnnData object and summarizes cell-level and gene-level metadata.

Outputs include:

* AnnData checkpoint
* observation metadata
* variable metadata
* metadata summary tables

### 3. Perturbation Label Preparation

`src/02_prepare_labels.py`

Creates a standardized perturbation label and identifies the appropriate control condition for downstream PertPy analysis.

### 4. Pseudobulk Analysis

`src/03_pertpy_pseudobulk.py`

Generates pseudobulk transcriptional profiles for individual perturbations and calculates perturbation-vs-control expression differences.

The resulting `AnnData` object contains the `control_diff` representation used for downstream analysis.

### 5. Perturbation Space

`src/04_condition_space_plots.py`

Projects perturbation-level transcriptional profiles into lower-dimensional space using:

* Principal Component Analysis (PCA)
* Uniform Manifold Approximation and Projection (UMAP)

This allows perturbations with similar transcriptional phenotypes to be compared in perturbation space.

### 6. Gene-level Perturbation Effects

`src/05_top_genes_reports.py`

For each perturbation, identifies the genes exhibiting the largest absolute expression differences relative to control.

Output:

```text
results/tables/top_genes_per_perturbation_top30.csv
```

### 7. Perturbation-level Effect Analysis

`src/06_top_pertubations_report.py`

Quantifies and ranks the overall transcriptional effect associated with each perturbation.

The analysis summarizes:

* overall transcriptional effect size
* mean absolute gene-level difference
* maximum gene-level difference
* number of genes contributing to the calculation

Outputs include:

```text
results/tables/top_perturbations_by_effect_size.csv
results/figures/top_perturbations_stats.png
```

---

## Outputs

The pipeline generates intermediate AnnData objects, visualizations, and analysis tables.

### Data

```text
results/data/
├── atlas_loaded.h5ad
├── atlas_prepared.h5ad
├── pseudobulk_by_condition.h5ad
└── pseudobulk_control_diff.h5ad
```

### Figures

```text
results/figures/
├── pca_condition_space.png
├── umap_condition_space.png
└── top_perturbations_stats.png
```

### Tables

```text
results/tables/
├── obs_columns.csv
├── var_columns.csv
├── obs_nunique_top30.csv
├── top_genes_per_perturbation_top30.csv
└── top_perturbations_by_effect_size.csv
```

---

## Reproducibility

The workflow is designed to be executed from a clean computational environment using Snakemake.

### Run locally

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Then execute:

```bash
snakemake --cores 4
```

Snakemake determines the required execution order from the workflow dependencies and generates the complete set of outputs.

---

## Docker

The analysis environment is containerized using Docker.

Build the image:

```bash
docker build -t pertpy-perturbation-analysis .
```

Run the complete workflow:

```bash
docker run --rm \
    -v "$(pwd):/workspace" \
    pertpy-perturbation-analysis
```

The container includes the Python analysis environment and Snakemake required to execute the workflow.

This provides a reproducible computational environment independent of the host Python installation.

---

## Technologies

### Single-cell & perturbation analysis

* Perturb-seq
* PertPy
* Scanpy
* AnnData
* Pseudobulk analysis

### Programming & analysis

* Python
* NumPy
* Pandas
* Matplotlib
* scikit-learn

### Workflow & reproducibility

* Snakemake
* Docker
* Git
* GitHub

---

## Results

### Perturbation Space

PCA and UMAP representations are used to visualize relationships between perturbations based on their transcriptional effects.

![PCA perturbation space](results/figures/pca_condition_space.png)

![UMAP perturbation space](results/figures/umap_condition_space.png)

### Perturbation Effect Size

Perturbations are ranked according to the magnitude of their transcriptional deviation from control.

![Top perturbations](results/figures/top_perturbations_stats.png)

### Top Perturbation-associated Genes

For each perturbation, the genes with the largest absolute transcriptional differences from control are reported.

---

## Motivation

This project was developed to gain hands-on experience with **perturbational single-cell genomics** and to explore how genetic perturbations can be represented as transcriptional phenotypes.

The analysis builds on experience with single-cell and spatial transcriptomics, multi-omics analysis, statistical modelling, machine learning, and reproducible bioinformatics workflows.

Perturb-seq provides a natural extension of these approaches by introducing an explicit experimental perturbation and enabling computational analysis of the resulting transcriptional response.

The project also demonstrates a broader principle in computational biology: moving from exploratory analysis toward **reproducible, modular, and portable scientific workflows**.

---

## Attribution

This project builds upon the original PertPy Perturb-seq workflow developed by **Taufia Hussain**:

https://github.com/TaufiaHussain/pertpy-perturbation-analysis

The original workflow was reproduced and extended with:

* perturbation-level transcriptional effect analysis
* perturbation effect-size ranking
* additional result tables and visualizations
* Snakemake workflow orchestration
* Docker-based reproducibility

The underlying dataset is based on the Norman et al. (2019) CRISPR Perturb-seq study and its standardized scPerturb distribution.

Please refer to the original repository and associated publications for the original workflow and dataset attribution.

---

## License

MIT License
