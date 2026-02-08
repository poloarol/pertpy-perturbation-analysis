import os
import sys
import urllib.request

URL = "https://zenodo.org/records/13350497/files/NormanWeissman2019_filtered.h5ad?download=1"
OUT_PATH = os.path.join("data", "NormanWeissman2019_filtered.h5ad")

def main() -> int:
    os.makedirs("data", exist_ok=True)

    if os.path.exists(OUT_PATH):
        size_mb = os.path.getsize(OUT_PATH) / (1024 * 1024)
        print(f"[OK] Already downloaded: {OUT_PATH} ({size_mb:.1f} MB)")
        return 0

    print("[INFO] Downloading dataset (this is ~699 MB).")
    print("[INFO] Source:", URL)
    try:
        urllib.request.urlretrieve(URL, OUT_PATH)
    except Exception as e:
        print("[ERROR] Download failed:", e)
        return 1

    size_mb = os.path.getsize(OUT_PATH) / (1024 * 1024)
    print(f"[OK] Downloaded: {OUT_PATH} ({size_mb:.1f} MB)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
