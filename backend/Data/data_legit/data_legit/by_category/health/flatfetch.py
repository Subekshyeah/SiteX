import json
import csv
import glob
import re
import os
import random
from datetime import datetime, timedelta
from pathlib import Path

# ----------------------------------------------------------------------
# CONFIG
# ----------------------------------------------------------------------
INPUT_DIR   = "."          # <-- your JSON files
OUTPUT_DIR  = "csv"          # <-- CSVs here
# ----------------------------------------------------------------------


# ----------------------------------------------------------------------
# 1. Time parsing
# ----------------------------------------------------------------------
def _normalize_space(s: str) -> str:
    return s.replace('\u202f', ' ').replace('\xa0', ' ').strip()

def _parse_time_str(t: str) -> datetime:
    t = _normalize_space(t).upper()
    fmts = ['%I %p', '%I:%M %p', '%I%p', '%I:%M%p']
    for fmt in fmts:
        try:
            return datetime.strptime(t, fmt)
        except Exception:
            pass
    raise ValueError(f"Unrecognized time: {t!r}")

def _hours_from_entry(hours_str: str) -> float:
    s = _normalize_space(hours_str)
    if not s or s.lower() in ('closed', 'open 24 hours'):
        return 0.0 if s.lower() == 'closed' else 24.0
    total_seconds = 0
    ranges = re.split(r'\s*[;,]\s*', s)
    for r in ranges:
        parts = re.split(r"\s*(?:to|–|—|-)\s*", r, flags=re.I)
        if len(parts) < 2: continue
        try:
            start_dt = _parse_time_str(parts[0].strip())
            end_dt = _parse_time_str(parts[1].strip())
        except ValueError:
            continue
        delta = end_dt - start_dt
        if delta.total_seconds() <= 0:
            delta += timedelta(days=1)
        total_seconds += delta.total_seconds()
    return total_seconds / 3600.0

def _total_week_hours(opening_hours_list) -> float:
    total = 0.0
    for entry in opening_hours_list or []:
        total += _hours_from_entry(entry.get('hours', ''))
    return round(total, 2)


# ----------------------------------------------------------------------
# 2. Feature detection
# ----------------------------------------------------------------------
def has_feature(data, category, key):
    items = data.get("additionalInfo", {}).get(category, [])
    return 1 if any(key in item for item in items) else 0


# ----------------------------------------------------------------------
# 3. Generate realistic review distribution (only if missing)
# ----------------------------------------------------------------------
def generate_review_distribution(rating: float, total_reviews: int):
    if total_reviews == 0:
        return {f"reviewsDistribution_{i}Star": 0 for i in range(1, 6)}

    base_weights = {
        1: max(0.1, 5.5 - rating),
        2: max(0.3, 4.5 - rating),
        3: 1.0,
        4: max(1.0, rating - 2.0),
        5: max(2.0, rating - 1.0)
    }
    total = sum(base_weights.values())
    probs = [base_weights[i] / total for i in range(1, 6)]

    counts = [0] * 5
    for _ in range(total_reviews):
        star = random.choices(range(1, 6), weights=probs, k=1)[0]
        counts[star - 1] += 1

    current_sum = sum(counts)
    diff = total_reviews - current_sum
    if diff != 0:
        idx = probs.index(max(probs))
        counts[idx] += diff

    return {f"reviewsDistribution_{i}Star": counts[i-1] for i in range(1, 6)}


# ----------------------------------------------------------------------
# 4. Flatten place + handle reviewsDistribution correctly
# ----------------------------------------------------------------------
def flatten_place(data):
    flat = {}

    # Core
    flat["name"] = data.get("title", "")
    flat["main_category"] = data.get("categoryName", "")
    flat["category"] = (data.get("categories") or [None])[0] or ""
    flat["address"] = data.get("address", "")
    flat["city"] = data.get("city", "")
    flat["postal"] = data.get("postalCode", "")
    flat["country"] = data.get("countryCode", "")
    flat["phone"] = data.get("phone", "")
    flat["place_id"] = data.get("placeId", "")
    flat["cid"] = data.get("cid", "")
    flat["url"] = data.get("url", "")
    flat["search_term"] = data.get("searchString", "")

    # Hours
    hours_list = data.get("openingHours", [])
    flat["hours"] = hours_list[0].get("hours", "") if hours_list else ""
    flat["weekly_hours"] = _total_week_hours(hours_list)

    # Metrics
    flat["rating"] = float(data.get("totalScore") or 0)
    flat["reviews_count"] = int(data.get("reviewsCount") or 0)
    loc = data.get("location", {})
    flat["lat"] = float(loc.get("lat") or 0)
    flat["lng"] = float(loc.get("lng") or 0)

    # Boolean features
    flat["dine_in"] = has_feature(data, "Service options", "Dine-in")
    flat["takeout"] = has_feature(data, "Service options", "Takeout")
    flat["delivery"] = has_feature(data, "Service options", "Delivery")
    flat["breakfast"] = has_feature(data, "Dining options", "Breakfast")
    flat["lunch"] = has_feature(data, "Dining options", "Lunch")
    flat["dinner"] = has_feature(data, "Dining options", "Dinner")
    flat["vegetarian"] = has_feature(data, "Offerings", "Vegetarian options")
    flat["coffee"] = has_feature(data, "Offerings", "Coffee")
    flat["alcohol"] = has_feature(data, "Offerings", "Alcohol")
    flat["beer"] = has_feature(data, "Offerings", "Beer")
    flat["wifi"] = has_feature(data, "Amenities", "Wi-Fi") or has_feature(data, "Amenities", "Free Wi-Fi")
    flat["casual"] = has_feature(data, "Atmosphere", "Casual")
    flat["family_friendly"] = has_feature(data, "Crowd", "Family-friendly")
    flat["tourists"] = has_feature(data, "Crowd", "Tourists")
    flat["reservations"] = has_feature(data, "Planning", "Accepts reservations")
    flat["cash_only"] = has_feature(data, "Payments", "Cash-only")
    flat["wheelchair_accessible_entrance"] = has_feature(data, "Accessibility", "Wheelchair accessible entrance")

    # === HANDLE reviewsDistribution (your format) ===
    dist = data.get("reviewsDistribution", {})
    if isinstance(dist, dict):
        for star in ["oneStar", "twoStar", "threeStar", "fourStar", "fiveStar"]:
            key = f"reviewsDistribution_{star}"
            flat[key] = int(dist.get(star, 0))

    # Extract ALL nested fields
    def extract(obj, prefix=""):
        if isinstance(obj, dict):
            for k, v in obj.items():
                new_key = f"{prefix}_{k}" if prefix else k
                if isinstance(v, (dict, list)):
                    extract(v, new_key)
                else:
                    flat[new_key] = v
        elif isinstance(obj, list) and obj and isinstance(obj[0], dict):
            extract(obj[0], prefix)

    extract(data)
    extract(data.get("additionalInfo", {}), "info")
    extract(data.get("location", {}), "loc")

    return flat


# ----------------------------------------------------------------------
# 5. MAIN
# ----------------------------------------------------------------------
def main():
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    input_files = glob.glob(os.path.join(INPUT_DIR, "*.json"))
    if not input_files:
        print(f"No JSON files in {INPUT_DIR}")
        return

    # Discover ALL fields
    all_fields = set()
    print("Scanning fields...")
    for filepath in input_files:
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                for item in (data if isinstance(data, list) else [data]):
                    flat = flatten_place(item)
                    all_fields.update(flat.keys())
        except Exception as e:
            print(f"Scan error {filepath}: {e}")

    all_fields = sorted(all_fields)
    print(f"Found {len(all_fields)} fields.")

    # Process all
    seen_keys = set()
    rows = []
    total_input = 0

    for filepath in input_files:
        print(f"Processing {os.path.basename(filepath)}...")
        with open(filepath, "r", encoding="utf-8") as f:
            try:
                data_list = json.load(f)
                if not isinstance(data_list, list):
                    data_list = [data_list]
                total_input += len(data_list)
            except Exception as e:
                print(f"Load error {filepath}: {e}")
                continue

        for item in data_list:
            row = flatten_place(item)

            # Deduplicate
            lat, lng = row.get("lat"), row.get("lng")
            key = (round(float(lat), 6), round(float(lng), 6)) if lat and lng else None
            if key and key in seen_keys:
                continue
            if key:
                seen_keys.add(key)

            # === GENERATE MISSING reviewDistribution ===
            total_reviews = row.get("reviews_count", 0)
            dist_keys = [f"reviewsDistribution_{s}Star" for s in ["one", "two", "three", "four", "five"]]
            current_sum = sum(row.get(k, 0) for k in dist_keys)

            if total_reviews > 0 and (current_sum == 0 or current_sum != total_reviews):
                dist = generate_review_distribution(
                    rating=row.get("rating", 0),
                    total_reviews=total_reviews
                )
                for k, v in dist.items():
                    if row.get(k, 0) == 0:
                        row[k] = v

            # Add source
            row["source_file"] = os.path.basename(filepath)

            # Fill missing
            final_row = {}
            for field in all_fields:
                val = row.get(field)
                if val in (None, ""):
                    final_row[field] = 0 if any(x in field for x in ["count", "hours", "Distribution", "Star", "lat", "lng", "rating"]) else ""
                else:
                    final_row[field] = val
            rows.append(final_row)

    # Write CSVs
    full_csv = os.path.join(OUTPUT_DIR, "flattened_all_fields.csv")
    compact_csv = os.path.join(OUTPUT_DIR, "compact_summary.csv")

    compact_fields = [
        "name","main_category","category","address","city",
        "lat","lng","rating","reviews_count",
        "reviewsDistribution_oneStar","reviewsDistribution_twoStar",
        "reviewsDistribution_threeStar","reviewsDistribution_fourStar","reviewsDistribution_fiveStar",
        "weekly_hours", "imageUrl", "url"
    ]

    with open(full_csv, "w", newline="", encoding="utf-8") as f_full, \
         open(compact_csv, "w", newline="", encoding="utf-8") as f_compact:

        writer_full = csv.DictWriter(f_full, fieldnames=all_fields)
        writer_full.writeheader()

        writer_compact = csv.DictWriter(f_compact, fieldnames=compact_fields)
        writer_compact.writeheader()

        for row in rows:
            writer_full.writerow(row)
            compact_row = {k: row.get(k, 0 if k in compact_fields[:14] else "") for k in compact_fields}
            writer_compact.writerow(compact_row)

    print(f"\nDone!")
    print(f"   Input: {total_input}, Unique: {len(rows)}")
    print(f"   Full: {full_csv}")
    print(f"   Compact: {compact_csv}")


if __name__ == "__main__":
    main()
