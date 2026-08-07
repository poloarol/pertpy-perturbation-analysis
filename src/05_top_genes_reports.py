import os
import sys

import numpy as np
import pandas as pd
import scanpy as sc


def main():

    if len(sys.argv) != 3:
        print(
            "Usage: python 05_top_genes_reports.py "
            "<input_h5ad> <output_csv>"
        )
        return 1

    in_path = sys.argv[1]
    out_csv = sys.argv[2]

    os.makedirs(
        os.path.dirname(out_csv),
        exist_ok=True
    )

    pb = sc.read_h5ad(in_path)

    # --------------------------------------------------
    # Extract control-difference matrix
    # --------------------------------------------------

    X = pb.X

    if not isinstance(X, np.ndarray):
        X = X.toarray()

    genes = pb.var_names.to_numpy()
    perts = pb.obs_names.to_numpy()

    # --------------------------------------------------
    # Find top 30 genes for each perturbation
    # --------------------------------------------------

    topk = 30
    rows = []

    for i, pert in enumerate(perts):

        diff = X[i, :].astype(float)

        valid = np.isfinite(diff)

        diff = diff[valid]

        valid_genes = genes[valid]

        if len(diff) == 0:
            continue

        idx = np.argsort(
            np.abs(diff)
        )[::-1][:topk]

        for rank, j in enumerate(idx, start=1):

            rows.append(
                {
                    "perturbation": pert,
                    "rank": rank,
                    "gene": valid_genes[j],
                    "control_diff": float(diff[j]),
                    "abs_diff": float(abs(diff[j])),
                }
            )

    df = pd.DataFrame(rows)

    # --------------------------------------------------
    # Save output
    # --------------------------------------------------

    df.to_csv(
        out_csv,
        index=False
    )

    print(
        "[OK] Saved:",
        out_csv
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())