import os
import numpy as np
import pandas as pd
import scanpy as sc

IN_PATH = os.path.join("outputs", "data", "pseudobulk_control_diff.h5ad")
OUT_DIR = os.path.join("outputs", "tables")
os.makedirs(OUT_DIR, exist_ok=True)

def main():
    if not os.path.exists(IN_PATH):
        raise FileNotFoundError(f"Missing {IN_PATH}. Run scripts/03_pertpy_pseudobulk.py first.")

    pb = sc.read_h5ad(IN_PATH)

    # pb.X is control_diff
    X = pb.X
    if not isinstance(X, np.ndarray):
        X = X.toarray()

    genes = pb.var_names.to_numpy()
    perts = pb.obs_names.to_numpy()

    topk = 30
    rows = []
    for i, p in enumerate(perts):
        diff = X[i, :]
        idx = np.argsort(np.abs(diff))[::-1][:topk]
        for rank, j in enumerate(idx, start=1):
            rows.append({
                "perturbation": p,
                "rank": rank,
                "gene": genes[j],
                "control_diff": float(diff[j]),
                "abs_diff": float(abs(diff[j])),
            })

    df = pd.DataFrame(rows)
    out_path = os.path.join(OUT_DIR, "top_genes_per_perturbation_top30.csv")
    df.to_csv(out_path, index=False)
    print("[OK] Saved:", out_path)

if __name__ == "__main__":
    main()
