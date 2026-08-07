# Snakefile

PROJECT = "."

DATA = "data"

rule all:
    input:
        "data/NormanWeissman2019_filtered.h5ad",
        "results/figures/pca_condition_space.png",
        "results/figures/umap_condition_space.png",
        "results/tables/top_perturbations_by_effect_size.csv",
        "results/figures/top_perturbations_stats.png",
        "results/tables/obs_columns.csv",
        "results/tables/var_columns.csv",
        "results/tables/obs_nunique_top30.csv",
        "results/tables/top_genes_per_perturbation_top30.csv"

rule download_data:
    output:
        "data/NormanWeissman2019_filtered.h5ad"
    shell:
        """
        python src/00_download_data.py {output}
        """

rule load_and_inspect:
    input:
        "data/NormanWeissman2019_filtered.h5ad"
    output:
        h5ad="results/data/atlas_loaded.h5ad",
        obs_cols="results/tables/obs_columns.csv",
        var_cols="results/tables/var_columns.csv",
        obs_summary="results/tables/obs_nunique_top30.csv"
    shell:
        """
        python src/01_load_and_inspect.py \
            {input} \
            {output.h5ad} \
            {output.obs_cols} \
            {output.var_cols} \
            {output.obs_summary}
        """

rule prepare_labels:
    input:
        "results/data/atlas_loaded.h5ad"
    output:
        "results/data/atlas_prepared.h5ad"
    shell:
        """
        python src/02_prepare_labels.py \
            {input} \
            {output}
        """

rule pseudobulk:
    input:
        "results/data/atlas_prepared.h5ad"
    output:
        pb="results/data/pseudobulk_by_condition.h5ad",
        cd="results/data/pseudobulk_control_diff.h5ad"
    shell:
        """
        python src/03_pertpy_pseudobulk.py \
            {input} \
            {output.pb} \
            {output.cd}
        """

rule condition_space_plots:
    input:
        "results/data/pseudobulk_control_diff.h5ad"
    output:
        pca="results/figures/pca_condition_space.png",
        umap="results/figures/umap_condition_space.png"
    shell:
        """
        python src/04_condition_space_plots.py \
            {input} \
            {output.pca} \
            {output.umap}
        """

rule top_genes_report:
    input:
        "results/data/pseudobulk_control_diff.h5ad"
    output:
        table="results/tables/top_genes_per_perturbation_top30.csv"
    shell:
        """
        python src/05_top_genes_reports.py \
            {input} \
            {output.table}
        """

rule top_perturbation_report:
    input:
        "results/data/pseudobulk_control_diff.h5ad"
    output:
        table="results/tables/top_perturbations_by_effect_size.csv",
        figure="results/figures/top_perturbations_stats.png"
    shell:
        """
        python src/06_top_pertubations_report.py \
            {input} \
            {output.table} \
            {output.figure}
        """