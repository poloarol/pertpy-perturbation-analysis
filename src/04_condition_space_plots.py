import os
import sys

import scanpy as sc
import matplotlib.pyplot as plt


def main():

    if len(sys.argv) != 4:
        print(
            "Usage: python 04_condition_space_plots.py "
            "<input_h5ad> <pca_png> <umap_png>"
        )
        return 1


    in_path = sys.argv[1]
    pca_path = sys.argv[2]
    umap_path = sys.argv[3]


    if not os.path.exists(in_path):
        raise FileNotFoundError(
            f"Missing {in_path}"
        )


    os.makedirs(
        os.path.dirname(pca_path),
        exist_ok=True
    )


    pb = sc.read_h5ad(in_path)


    print(
        "[INFO] Loaded:",
        pb
    )


    # --------------------------------------------------
    # PCA
    # --------------------------------------------------

    sc.pp.scale(
        pb,
        max_value=10
    )

    sc.tl.pca(
        pb
    )


    sc.pl.pca(
        pb,
        color=[
            "nperts",
            "ncounts",
            "ngenes",
            "percent_mito",
            "gemgroup",
            "number_of_cells",
        ],
        show=False,
    )

    plt.savefig(
        pca_path,
        bbox_inches="tight",
        dpi=200
    )

    plt.close()

    print(
        "[OK] Saved:",
        pca_path
    )


    # --------------------------------------------------
    # UMAP
    # --------------------------------------------------

    n = pb.n_obs

    if n >= 3:

        sc.pp.neighbors(
            pb,
            n_neighbors=min(10, n - 1)
        )

        sc.tl.umap(
            pb
        )


        sc.pl.umap(
            pb,
            color=[
                "nperts",
                "ncounts",
                "ngenes",
                "percent_mito",
                "gemgroup",
                "number_of_cells",
            ],
            show=False,
        )


        plt.savefig(
            umap_path,
            bbox_inches="tight",
            dpi=200
        )

        plt.close()

        print(
            "[OK] Saved:",
            umap_path
        )

    else:

        print(
            "[INFO] Not enough pseudobulk points for UMAP"
        )


    return 0


if __name__ == "__main__":
    raise SystemExit(main())