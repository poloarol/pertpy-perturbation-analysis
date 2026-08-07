import os
import sys
import scanpy as sc
import pertpy as pt


def main():

    if len(sys.argv) != 4:
        print(
            "Usage: python 03_pertpy_pseudobulk.py "
            "<input_h5ad> <output_pb> <output_cd>"
        )
        return 1


    in_path = sys.argv[1]
    out_pb = sys.argv[2]
    out_cd = sys.argv[3]


    if not os.path.exists(in_path):
        raise FileNotFoundError(
            f"Missing {in_path}"
        )


    adata = sc.read_h5ad(in_path)


    target_col = adata.uns.get(
        "pertpy_target_col",
        "condition"
    )

    ctrl = adata.uns.get(
        "pertpy_control_label",
        None
    )

    if ctrl is None:
        raise KeyError(
            "Missing adata.uns['pertpy_control_label']"
        )


    print("[INFO] target column:", target_col)
    print("[INFO] control label:", ctrl)


    ps = pt.tl.PseudobulkSpace()


    # --------------------------------------------------
    # Compute pseudobulk profiles
    # --------------------------------------------------

    pb = ps.compute(
        adata,
        target_col=target_col,
        mode="mean"
    )


    os.makedirs(
        os.path.dirname(out_pb),
        exist_ok=True
    )

    pb.write(out_pb)

    print(
        "[OK] Saved pseudobulk:",
        out_pb
    )


    # --------------------------------------------------
    # Compute control differences
    # --------------------------------------------------

    pb_cd = ps.compute_control_diff(
        pb,
        target_col=target_col,
        reference_key=ctrl,
        layer_key="mean",
        new_layer_key="control_diff",
        copy=True,
    )


    assert "control_diff" in pb_cd.layers


    # Use control differences for embeddings
    pb_cd.X = (
        pb_cd.layers["control_diff"]
        .copy()
    )


    pb_cd.write(out_cd)

    print(
        "[OK] Saved control-diff pseudobulk:",
        out_cd
    )


    return 0


if __name__ == "__main__":
    raise SystemExit(main())