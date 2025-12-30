import json
import glob
import os
from pathlib import Path

# ----------------------------------------------------------------------
# CONFIG
# ----------------------------------------------------------------------
INPUT_DIR   = "."          # folder with your *.json files
OUTPUT_DIR  = "by_category"     # where <category>.json files will go
# ----------------------------------------------------------------------


def sanitize(name: str) -> str:
    """Turn any categoryName into a safe filename."""
    return "".join(c if c.isalnum() or c in " _-." else "_" for c in name).strip()


def main():
    # create output folder
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

    # dict: category → list of place objects
    groups = {}

    # ------------------------------------------------------------------
    # 1. Scan every JSON file
    # ------------------------------------------------------------------
    for filepath in glob.glob(os.path.join(INPUT_DIR, "*.json")):
        with open(filepath, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)               # expect list of places
                if not isinstance(data, list):
                    print(f"Warning: {filepath} is not a list – skipping")
                    continue
            except json.JSONDecodeError as e:
                print(f"Error: JSON error in {filepath}: {e}")
                continue

        # ----------------------------------------------------------------
        # 2. Group by categoryName
        # ----------------------------------------------------------------
        for place in data:
            cat = place.get("categoryName", "Unknown")
            groups.setdefault(cat, []).append(place)

    # ------------------------------------------------------------------
    # 3. Write one file per category
    # ------------------------------------------------------------------
    for cat, items in groups.items():
        safe_name = sanitize(cat)
        out_path = os.path.join(OUTPUT_DIR, f"{safe_name}.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(items, f, ensure_ascii=False, indent=2)
        print(f"{cat!r} → {out_path}  ({len(items)} places)")

    print("\nDone! All files are in:", OUTPUT_DIR)


if __name__ == "__main__":
    main()
