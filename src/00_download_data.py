import os
import sys
import urllib.request

URL = (
    "https://zenodo.org/records/13350497/files/"
    "NormanWeissman2019_filtered.h5ad?download=1"
)


def main() -> int:

    if len(sys.argv) != 2:
        print(
            "Usage: python 00_download_data.py <output_path>"
        )
        return 1

    out_path = sys.argv[1]

    out_dir = os.path.dirname(out_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    print("[INFO] Downloading dataset")
    print("[INFO] Source:", URL)
    print("[INFO] Output:", out_path)

    try:
        urllib.request.urlretrieve(
            URL,
            out_path
        )

    except Exception as e:
        print("[ERROR] Download failed:", e)
        return 1

    size_mb = (
        os.path.getsize(out_path)
        / (1024 * 1024)
    )

    print(
        f"[OK] Downloaded: {out_path} "
        f"({size_mb:.1f} MB)"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())