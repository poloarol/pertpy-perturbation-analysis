import os
import sys
import scanpy as sc
import pandas as pd


def main():

    if len(sys.argv) != 6:
        print(
            "Usage: python 01_load_and_inspect.py "
            "<input_h5ad> <output_h5ad> "
            "<obs_columns_csv> <var_columns_csv> "
            "<obs_summary_csv>"
        )
        return 1

    data_path = sys.argv[1]
    out_h5ad = sys.argv[2]
    obs_csv = sys.argv[3]
    var_csv = sys.argv[4]
    summary_csv = sys.argv[5]


    if not os.path.exists(data_path):
        raise FileNotFoundError(
            f"Missing {data_path}"
        )


    # Create output folders
    for path in [
        out_h5ad,
        obs_csv,
        var_csv,
        summary_csv
    ]:
        os.makedirs(
            os.path.dirname(path),
            exist_ok=True
        )


    adata = sc.read_h5ad(data_path)

    print(adata)


    # Save obs / var metadata summaries
    pd.DataFrame(
        {"obs_columns": list(adata.obs.columns)}
    ).to_csv(
        obs_csv,
        index=False
    )


    pd.DataFrame(
        {"var_columns": list(adata.var.columns)}
    ).to_csv(
        var_csv,
        index=False
    )


    adata.obs.nunique() \
        .sort_values(ascending=False) \
        .head(30) \
        .to_csv(summary_csv)


    # Print useful metadata summaries
    for c in [
        "perturbation",
        "perturbation_type",
        "celltype",
        "nperts",
        "percent_mito",
        "ncounts",
    ]:
        if c in adata.obs.columns:
            print(
                f"\n=== {c} value_counts (top 15) ==="
            )
            print(
                adata.obs[c]
                .value_counts()
                .head(15)
            )


    # Save checkpoint
    adata.write(out_h5ad)

    print(
        "\n[OK] Saved checkpoint:",
        out_h5ad
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())