import os
import re
import scanpy as sc

IN_PATH = os.path.join("outputs", "data", "atlas_loaded.h5ad")
OUT_PATH = os.path.join("outputs", "data", "atlas_prepared.h5ad")

def guess_control_label(values) -> str:
    """
    Choose a reasonable control label from a list of unique perturbation labels.
    Fallback: most frequent label.
    """
    priority_substrings = [
        "control", "ctrl", "non-target", "nontarget", "non_target",
        "nt", "negctrl", "neg_ctrl", "scramble"
    ]
    values_str = [str(v) for v in values]
    for p in priority_substrings:
        for v in values_str:
            if p in v.lower():
                return v
    return None

def main():
    if not os.path.exists(IN_PATH):
        raise FileNotFoundError(f"Missing {IN_PATH}. Run scripts/01_load_and_inspect.py first.")

    adata = sc.read_h5ad(IN_PATH)

    # pick perturbation column (this dataset usually has 'perturbation')
    if "perturbation" in adata.obs.columns:
        target_col = "perturbation"
    else:
        # minimal fallback: first column containing 'perturb'
        candidates = [c for c in adata.obs.columns if "perturb" in c.lower()]
        if not candidates:
            raise KeyError("Could not find a perturbation column (expected something like 'perturbation').")
        target_col = candidates[0]

    adata.obs["condition"] = adata.obs[target_col].astype(str).str.strip()
    uniq = adata.obs["condition"].unique()

    ctrl = guess_control_label(uniq)
    if ctrl is None:
        # fallback: most frequent label in condition
        ctrl = adata.obs["condition"].value_counts().index[0]

    adata.uns["pertpy_target_col"] = "condition"
    adata.uns["pertpy_control_label"] = ctrl

    print("[INFO] target_col:", target_col)
    print("[INFO] condition column created: adata.obs['condition']")
    print("[INFO] control label guessed:", ctrl)
    print("\nTop conditions:")
    print(adata.obs["condition"].value_counts().head(15))

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    adata.write(OUT_PATH)
    print("\n[OK] Saved:", OUT_PATH)

if __name__ == "__main__":
    main()
