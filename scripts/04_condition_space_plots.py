import os
import scanpy as sc

IN_PATH = os.path.join("outputs", "data", "pseudobulk_control_diff.h5ad")
FIG_DIR = os.path.join("outputs", "figures")
os.makedirs(FIG_DIR, exist_ok=True)

def main():
    if not os.path.exists(IN_PATH):
        raise FileNotFoundError(f"Missing {IN_PATH}. Run scripts/03_pertpy_pseudobulk.py first.")

    pb = sc.read_h5ad(IN_PATH)

    # Scale then PCA
    sc.pp.scale(pb, max_value=10)
    sc.tl.pca(pb)

    sc.pl.pca(pb, show=False)
    pca_path = os.path.join(FIG_DIR, "pca_condition_space.png")
    import matplotlib.pyplot as plt
    plt.savefig(pca_path, bbox_inches="tight", dpi=200)
    plt.close()
    print("[OK] Saved:", pca_path)

    # UMAP (optional)
    n = pb.n_obs
    if n >= 3:
        sc.pp.neighbors(pb, n_neighbors=min(10, n - 1))
        sc.tl.umap(pb)

        sc.pl.umap(pb, show=False)
        umap_path = os.path.join(FIG_DIR, "umap_condition_space.png")
        plt.savefig(umap_path, bbox_inches="tight", dpi=200)
        plt.close()
        print("[OK] Saved:", umap_path)
    else:
        print("[INFO] Not enough pseudobulk points for UMAP (need >=3).")

if __name__ == "__main__":
    main()
