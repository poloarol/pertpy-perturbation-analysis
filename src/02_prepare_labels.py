import os
import sys
import scanpy as sc


def guess_control_label(values):
    """
    Choose a reasonable control label from perturbation labels.
    """

    priority_substrings = [
        "control",
        "ctrl",
        "non-target",
        "nontarget",
        "non_target",
        "nt",
        "negctrl",
        "neg_ctrl",
        "scramble",
    ]

    values_str = [str(v) for v in values]

    for p in priority_substrings:
        for v in values_str:
            if p in v.lower():
                return v

    return None


def main():

    if len(sys.argv) != 3:
        print(
            "Usage: python 02_prepare_labels.py "
            "<input_h5ad> <output_h5ad>"
        )
        return 1


    in_path = sys.argv[1]
    out_path = sys.argv[2]


    if not os.path.exists(in_path):
        raise FileNotFoundError(
            f"Missing {in_path}"
        )


    adata = sc.read_h5ad(in_path)


    # Identify perturbation column
    if "perturbation" in adata.obs.columns:

        target_col = "perturbation"

    else:

        candidates = [
            c for c in adata.obs.columns
            if "perturb" in c.lower()
        ]

        if not candidates:
            raise KeyError(
                "Could not find perturbation column"
            )

        target_col = candidates[0]


    # Create standardized condition column
    adata.obs["condition"] = (
        adata.obs[target_col]
        .astype(str)
        .str.strip()
    )


    unique_conditions = (
        adata.obs["condition"]
        .unique()
    )


    ctrl = guess_control_label(
        unique_conditions
    )


    if ctrl is None:

        ctrl = (
            adata.obs["condition"]
            .value_counts()
            .index[0]
        )


    # Store pertpy settings
    adata.uns["pertpy_target_col"] = (
        "condition"
    )

    adata.uns["pertpy_control_label"] = (
        ctrl
    )


    print(
        "[INFO] target_col:",
        target_col
    )

    print(
        "[INFO] condition column created"
    )

    print(
        "[INFO] control label:",
        ctrl
    )

    print("\nTop conditions:")
    print(
        adata.obs["condition"]
        .value_counts()
        .head(15)
    )


    os.makedirs(
        os.path.dirname(out_path),
        exist_ok=True
    )

    adata.write(out_path)


    print(
        "\n[OK] Saved:",
        out_path
    )


    return 0


if __name__ == "__main__":
    raise SystemExit(main())