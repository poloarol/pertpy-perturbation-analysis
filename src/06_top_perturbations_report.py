import os
import sys

import numpy as np
import pandas as pd
import scanpy as sc
import matplotlib.pyplot as plt
import seaborn as sns


def main():

    if len(sys.argv) != 4:
        print(
            "Usage: python 06_top_pertubations_report.py "
            "<input_h5ad> <output_csv> <output_png>"
        )
        return 1


    in_path = sys.argv[1]
    out_csv = sys.argv[2]
    out_fig = sys.argv[3]


    pb = sc.read_h5ad(in_path)


    os.makedirs(
        os.path.dirname(out_csv),
        exist_ok=True
    )

    os.makedirs(
        os.path.dirname(out_fig),
        exist_ok=True
    )


    # --------------------------------------------------
    # Extract control-difference matrix
    # --------------------------------------------------

    X = pb.X

    if not isinstance(X, np.ndarray):
        X = X.toarray()


    # --------------------------------------------------
    # Effect statistics
    # --------------------------------------------------

    results = []

    for i, pert in enumerate(pb.obs_names):

        diff = X[i, :].astype(float)

        valid = np.isfinite(diff)

        diff = diff[valid]


        if len(diff) == 0:
            continue


        l2_effect = np.linalg.norm(diff)

        mean_abs_diff = np.mean(
            np.abs(diff)
        )

        max_abs_diff = np.max(
            np.abs(diff)
        )

        n_changed = np.sum(
            np.abs(diff) > 1
        )


        results.append(
            {
                "perturbation": pert,
                "l2_effect": l2_effect,
                "normalized_l2": (
                    l2_effect /
                    np.sqrt(len(diff))
                ),
                "mean_abs_diff": mean_abs_diff,
                "max_abs_diff": max_abs_diff,
                "n_changed_genes": n_changed,
                "n_genes": len(diff),
            }
        )


    df = pd.DataFrame(results)


    df["specificity"] = (
        df["max_abs_diff"] /
        df["mean_abs_diff"]
    )


    # Add metadata
    metadata = pb.obs[
        [
            "perturbation",
            "nperts"
        ]
    ].drop_duplicates()


    df = df.merge(
        metadata,
        on="perturbation",
        how="left"
    )


    df["perturbation_type"] = (
        df["nperts"]
        .map(
            {
                0: "Control",
                1: "Single",
                2: "Double"
            }
        )
    )


    # Rank
    df = (
        df
        .sort_values(
            "normalized_l2",
            ascending=False
        )
        .reset_index(drop=True)
    )


    df.insert(
        0,
        "rank",
        np.arange(1, len(df)+1)
    )


    df.to_csv(
        out_csv,
        index=False
    )


    print(
        "[OK] Saved:",
        out_csv
    )


    # --------------------------------------------------
    # Highlight top perturbations
    # --------------------------------------------------

    top_hits = (
        df
        .head(10)
        ["perturbation"]
        .tolist()
    )


    pb.obs["effect_group"] = np.where(
        pb.obs["perturbation"].isin(top_hits),
        pb.obs["perturbation"],
        "Other"
    )


    # --------------------------------------------------
    # Plotting
    # --------------------------------------------------

    fig, axes = plt.subplots(
        2,
        2,
        figsize=(14,12)
    )


    top_df = (
        df
        .head(20)
        .sort_values(
            "normalized_l2"
        )
    )


    sns.barplot(
        data=top_df,
        x="normalized_l2",
        y="perturbation",
        ax=axes[0,0],
        color="steelblue"
    )

    axes[0,0].set_title(
        "Top perturbation effects"
    )


    sns.scatterplot(
        data=df,
        x="n_changed_genes",
        y="normalized_l2",
        hue="specificity",
        ax=axes[0,1]
    )

    axes[0,1].set_title(
        "Effect magnitude vs breadth"
    )


    sns.scatterplot(
        data=df,
        x="normalized_l2",
        y="specificity",
        hue="perturbation_type",
        palette="Dark2",
        ax=axes[1,0]
    )

    axes[1,0].set_title(
        "Focused vs broad effects"
    )


    # PCA/UMAP embedding
    sc.pp.scale(
        pb,
        max_value=10
    )

    sc.tl.pca(pb)

    sc.pp.neighbors(
        pb,
        n_neighbors=min(10, pb.n_obs-1)
    )

    sc.tl.umap(pb)


    sc.pl.umap(
        pb,
        color="effect_group",
        ax=axes[1,1],
        show=False
    )


    axes[1,1].set_title(
        "Top perturbations in embedding"
    )


    plt.tight_layout()

    plt.savefig(
        out_fig,
        dpi=200,
        bbox_inches="tight"
    )

    plt.close()


    print(
        "[OK] Saved:",
        out_fig
    )


    return 0


if __name__ == "__main__":
    raise SystemExit(main())