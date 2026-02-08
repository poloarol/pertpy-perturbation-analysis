import os
import scanpy as sc
import pandas as pd

DATA_PATH = os.path.join("data", "NormanWeissman2019_filtered.h5ad")
OUT_TABLES = os.path.join("outputs", "tables")
os.makedirs(OUT_TABLES, exist_ok=True)

def main():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Missing {DATA_PATH}. Run scripts/00_download_data.py first.")

    adata = sc.read_h5ad(DATA_PATH)
    print(adata)

    # Save obs/var column lists
    obs_cols = pd.DataFrame({"obs_columns": list(adata.obs.columns)})
    var_cols = pd.DataFrame({"var_columns": list(adata.var.columns)})

    obs_cols.to_csv(os.path.join(OUT_TABLES, "obs_columns.csv"), index=False)
    var_cols.to_csv(os.path.join(OUT_TABLES, "var_columns.csv"), index=False)

    # Basic summaries
    adata.obs.nunique().sort_values(ascending=False).head(30).to_csv(
        os.path.join(OUT_TABLES, "obs_nunique_top30.csv")
    )

    # Print key candidates if present
    for c in ["perturbation", "perturbation_type", "celltype", "nperts", "percent_mito", "ncounts"]:
        if c in adata.obs.columns:
            print(f"\n=== {c} value_counts (top 15) ===")
            print(adata.obs[c].value_counts().head(15))

    # checkpoint
    out_ckpt = os.path.join("outputs", "data", "atlas_loaded.h5ad")
    os.makedirs(os.path.dirname(out_ckpt), exist_ok=True)
    adata.write(out_ckpt)
    print("\n[OK] Saved checkpoint:", out_ckpt)

if __name__ == "__main__":
    main()
