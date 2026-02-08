import os
import scanpy as sc
import pertpy as pt

IN_PATH = os.path.join("outputs", "data", "atlas_prepared.h5ad")
OUT_PB = os.path.join("outputs", "data", "pseudobulk_by_condition.h5ad")
OUT_CD = os.path.join("outputs", "data", "pseudobulk_control_diff.h5ad")

def main():
    if not os.path.exists(IN_PATH):
        raise FileNotFoundError(f"Missing {IN_PATH}. Run scripts/02_prepare_labels.py first.")

    adata = sc.read_h5ad(IN_PATH)

    target_col = adata.uns.get("pertpy_target_col", "condition")
    ctrl = adata.uns.get("pertpy_control_label", None)
    if ctrl is None:
        raise KeyError("Missing adata.uns['pertpy_control_label'].")

    ps = pt.tl.PseudobulkSpace()

    # one profile per condition
    pb = ps.compute(adata, target_col=target_col, mode="mean")
    os.makedirs(os.path.dirname(OUT_PB), exist_ok=True)
    pb.write(OUT_PB)
    print("[OK] Saved pseudobulk:", OUT_PB)

    # compute control difference into a new object
    pb_cd = ps.compute_control_diff(
        pb,
        target_col=target_col,
        reference_key=ctrl,
        new_layer_key="control_diff",
        copy=True,
    )

    # set X to control_diff for downstream embeddings
    pb_cd.X = pb_cd.layers["control_diff"].copy()
    pb_cd.write(OUT_CD)
    print("[OK] Saved control-diff pseudobulk:", OUT_CD)

if __name__ == "__main__":
    main()
