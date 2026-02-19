import csv
import glob
import json
import os
import random
import re
import shutil
from datetime import datetime, timedelta
from pathlib import Path

# ----------------------------------------------------------------------
# CONFIG
# ----------------------------------------------------------------------
INPUT_DIR = "."          # <-- your JSON files
OUTPUT_DIR = "csv"        # <-- CSVs here
BY_CATEGORY_DIR = "by_category"
# Use CSV headers as guidance for minimal output fields per category.
REFERENCE_HEADER_DIR = Path(__file__).resolve().parents[3] / "CSV_Reference"
REFERENCE_EXPORT_DIR = Path(__file__).resolve().parents[3] / "CSV_Reference"
# ----------------------------------------------------------------------

CATEGORY_RULES = {
    "cafes": {
        "Adventure sports center",
        "American restaurant",
        "Animal cafe",
        "Asian restaurant",
        "Asian fusion restaurant",
        "Assamese restaurant",
        "Bakery",
        "Bar & grill",
        "Banquet hall",
        "Barbecue restaurant",
        "Bar",
        "Bed & breakfast",
        "Bed-breakfast",
        "Beer garden",
        "Biryani restaurant",
        "Breakfast restaurant",
        "Brunch restaurant",
        "Bubble tea store",
        "Cafe",
        "Cafeteria",
        "Candy store",
        "Cake shop",
        "Cat cafe",
        "Chicken restaurant",
        "Chicken wings restaurant",
        "Chinese noodle restaurant",
        "Chinese restaurant",
        "Children's cafe",
        "Chocolate cafe",
        "Cosplay cafe",
        "Coffee roasters",
        "Coffee shop",
        "Coffee stand",
        "Coffee store",
        "Cocktail bar",
        "Continental restaurant",
        "Cottage rental",
        "Dairy store",
        "Dance restaurant",
        "Deli",
        "Dessert restaurant",
        "Dessert shop",
        "Dim sum restaurant",
        "Dog cafe",
        "Door manufacturer",
        "Dumpling restaurant",
        "Eatery",
        "English restaurant",
        "Espresso bar",
        "Family restaurant",
        "Fast food restaurant",
        "Fish restaurant",
        "Food court",
        "Frozen food store",
        "Grill",
        "Guest house",
        "Halal restaurant",
        "Hamburger restaurant",
        "Holiday apartment rental",
        "Hong kong style fast food restaurant",
        "Ice cream shop",
        "Indian restaurant",
        "Indian Muslim restaurant",
        "Internet cafe",
        "Italian restaurant",
        "Japanese restaurant",
        "Karaoke bar",
        "Korean restaurant",
        "Live music bar",
        "Lodge",
        "Lounge",
        "Lunch restaurant",
        "Mandarin restaurant",
        "Meat dish restaurant",
        "Mexican restaurant",
        "Momo restaurant",
        "Musical club",
        "Nepalese restaurant",
        "Organic restaurant",
        "Pan-Asian restaurant",
        "Pizza restaurant",
        "Pub",
        "Resort hotel",
        "Restaurant",
        "Restaurant or cafe",
        "Rice restaurant",
        "Sichuan restaurant",
        "Snack bar",
        "Southeast Asian restaurant",
        "Southern restaurant (US)",
        "Spanish restaurant",
        "Sports bar",
        "Takeout Restaurant",
        "Tea house",
        "Tea store",
        "Thai restaurant",
        "Tibetan restaurant",
        "Vegan restaurant",
        "Vegetarian restaurant",
        "Western restaurant",
        "Wholesale bakery",
        "Wine bar",
        "Hotel",
        "Farmstay",
        "Art cafe",
        "British restaurant",
        "Buffet restaurant",
    },
    "banks": {
        "Bank",
        "Cooperative bank",
        "ATM",
        "Private sector bank",
        "Public sector bank",
    },
    "education": {
        "Accounting school",
        "After school program",
        "Art school",
        "Agricultural high school",
        "Bartending school",
        "Boarding school",
        "Business school",
        "Children_s library",
        "Children's library",
        "Chinese language school",
        "College",
        "Combined primary and secondary school",
        "Coaching center",
        "Community school",
        "Community college",
        "Computer training school",
        "Dance school",
        "Drawing lessons",
        "Drivers license training school",
        "Driving school",
        "Educational institution",
        "Education center",
        "Educational consultant",
        "Educational supply store",
        "Elementary school",
        "English language school",
        "Engineering school",
        "Farm school",
        "General education school",
        "German language school",
        "Girls' high school",
        "Government college",
        "Government school",
        "Hospitality high school",
        "Higher secondary school",
        "High school",
        "Hotel management school",
        "International school",
        "Japanese language instructor",
        "K-12 school",
        "Kindergarten",
        "Language school",
        "Library",
        "Middle school",
        "Montessori preschool",
        "Montessori school",
        "Music school",
        "Preschool",
        "Primary school",
        "Private educational institution",
        "Private college",
        "Private university",
        "Public educational institution",
        "Public university",
        "Residential college",
        "School administration office",
        "School center",
        "School house",
        "School supply store",
        "Secondary school",
        "Special education school",
        "Single sex secondary school",
        "Software training institute",
        "Study at home school",
        "Studying center",
        "Trade school",
        "Taekwondo school",
        "Technical school",
        "Training center",
        "University library",
        "University",
        "Vocational secondary school",
        "Vocational school",
        "Women's college",
        "Polytechnic institute",
        "Cooking school",
        "Culinary school",
        "Law school",
        "Massage school",
        "Medical school",
        "Motorcycle driving school",
    },
    "health": {
        "Acupuncture clinic",
        "Animal hospital",
        "Ayurvedic clinic",
        "Blood bank",
        "Cancer treatment center",
        "Child health care center",
        "Children's hospital",
        "Chiropractor",
        "Community health center",
        "Dental clinic",
        "Dental implants periodontist",
        "Dermatologist",
        "Dentist",
        "Diagnostic center",
        "Doctor",
        "Emergency veterinarian service",
        "Faculty of pharmacy",
        "Fertility clinic",
        "Free clinic",
        "General hospital",
        "Government hospital",
        "Health and beauty shop",
        "Health consultant",
        "Health food store",
        "Health insurance agency",
        "Health resort",
        "Health spa",
        "Home health care service",
        "Holistic medicine practitioner",
        "Homeopathic pharmacy",
        "Hospital department",
        "Hospital equipment and supplies",
        "Hospitality and tourism school",
        "Hospital",
        "Medical Center",
        "Medical equipment supplier",
        "Medical clinic",
        "Mental health service",
        "Mental health clinic",
        "Maternity hospital",
        "Naturopathic practitioner",
        "Nursing agency",
        "Oncologist",
        "Occupational health service",
        "Orthopedic surgeon",
        "Orthotics & prosthetics service",
        "Orthopedic clinic",
        "Pain control clinic",
        "Pain management physician",
        "Pharmacy",
        "Pediatric clinic",
        "Physical therapy clinic",
        "Physical therapist",
        "Private hospital",
        "Psychiatric hospital",
        "Psychiatrist",
        "Public library",
        "Rehabilitation center",
        "Savings bank",
        "Self service health station",
        "Software company",
        "Massage spa",
        "Military hospital",
        "Spa",
        "Spa and health club",
        "Surgical supply store",
        "Ticket office",
        "Tour operator",
        "Traffic police station",
        "Travel agency",
        "Travel clinic",
        "University hospital",
        "Veterans hospital",
        "Veterinarian",
        "Veterinary pharmacy",
        "Weight loss service",
        "Wellness center",
        "Women's health clinic",
    },
    "other": {
        "Adventure sports center",
        "Accounting",
        "Accounting firm",
        "Acoustical consultant",
        "Adult entertainment club",
        "Advertising agency",
        "Amusement park",
        "Aquarium",
        "Architectural designer",
        "Architecture firm",
        "Art gallery",
        "Art studio",
        "Artistic handicrafts",
        "Association / Organization",
        "Aviation consultant",
        "Athletic park",
        "Banquet hall",
        "Barber shop",
        "Beautician",
        "Beauty salon",
        "Beauty school",
        "Beauty supply store",
        "Bakery equipment",
        "Botanical garden",
        "Book store",
        "Boutique",
        "Boxing gym",
        "Business park",
        "Business broker",
        "Business management consultant",
        "Business networking company",
        "Building consultant",
        "Building materials store",
        "Butcher shop",
        "Car rental agency",
        "Catering equipment rental service",
        "Catering food and drink supplier",
        "Cell phone store",
        "Chartered accountant",
        "City government office",
        "Church supply store",
        "Clothing store",
        "Coffee machine supplier",
        "Community garden",
        "Computer service",
        "Computer software store",
        "Computer support and services",
        "Confectionery wholesaler",
        "Construction company",
        "Consultant",
        "Convenience store",
        "Copy shop",
        "Cosmetics store",
        "Counselor",
        "Corporate office",
        "County government office",
        "Cultural center",
        "Dairy farm equipment supplier",
        "Dance company",
        "Day care center",
        "Day spa",
        "Delivery service",
        "Department store",
        "Design agency",
        "District office",
        "District government office",
        "Driver's license office",
        "Driving test center",
        "E-commerce service",
        "Education",
        "Employment consultant",
        "Engineering consultant",
        "Environment office",
        "Event venue",
        "Farm",
        "Federal government office",
        "Financial institution",
        "Financial audit",
        "Financial consultant",
        "Food bank",
        "Food and beverage consultant",
        "Food products supplier",
        "Fertilizer supplier",
        "Film and photograph library",
        "Fitness center",
        "Furniture store",
        "Futsal court",
        "Garden",
        "Garden center",
        "General store",
        "Grocery store",
        "Hair salon",
        "Government economic program",
        "Government",
        "Government office",
        "Gym",
        "Herb shop",
        "Herbal medicine store",
        "Historical landmark",
        "Historical place museum",
        "Home goods store",
        "Human resource consulting",
        "Importer",
        "Insurance company",
        "Interior architect office",
        "Internet marketing service",
        "Internet service provider",
        "Japanese prefecture government office",
        "Jewelry store",
        "Kitchen supply store",
        "Land registry office",
        "Land surveying office",
        "Liquor store",
        "Local government office",
        "Make-up artist",
        "Marketing agency",
        "Marketing consultant",
        "Meat products store",
        "Media house",
        "Men's clothing store",
        "Military recruiting office",
        "Motorcycle parts store",
        "Music management and promotion",
        "Musical instrument store",
        "National forest",
        "Nail salon",
        "Natural goods store",
        "Non-governmental organization",
        "Non-profit organization",
        "Memorial park",
        "Military school",
        "Mobile home park",
        "Muay Thai boxing gym",
        "Office",
        "Office accessories wholesaler",
        "Office equipment supplier",
        "Office furniture store",
        "Office supply wholesaler",
        "Office supply store",
        "Party planner",
        "Park",
        "Park _ ride",
        "Perfume store",
        "Photography studio",
        "Photo shop",
        "Photographer",
        "Playground",
        "Plaza",
        "Political party office",
        "Post office",
        "Public defender's office",
        "Publisher",
        "Recording studio",
        "Regional government office",
        "Registration office",
        "Religious goods store",
        "Religious lodging",
        "Research and product development",
        "Research institute",
        "Restaurant supply store",
        "Rideshare pickup location",
        "Sanitation service",
        "Sewing shop",
        "Shoe store",
        "Social security office",
        "Sports complex",
        "Stationery store",
        "Store",
        "State government office",
        "Technology park",
        "Telecommunications",
        "Tax attorney",
        "Tax consultant",
        "Tax department",
        "Tax preparation service",
        "Tea manufacturer",
        "Tailor",
        "Tour agency",
        "Tourist information center",
        "Toy library",
        "Travel services",
        "Vastu consultant",
        "Video game store",
        "Video production service",
        "Visa and passport office",
        "Visa consulting service",
        "Vitamin & supplements store",
        "Wallpaper store",
        "Website designer",
        "Wedding bakery",
        "Women's clothing store",
        "Yoga studio",
        "Water park",
    },
    "temples": {
        "Buddhist temple",
        "Hindu temple",
        "Tourist attraction",
        "Abundant Life church",
        "Alliance church",
        "Anglican church",
        "Apostolic church",
        "Catholic church",
        "Christian church",
        "Church",
        "Church council office",
        "Church of Christ",
        "Church of the Nazarene",
        "Eastern Orthodox Church",
        "Evangelical church",
        "Friends church",
        "Jain temple",
        "Methodist church",
        "Monastery",
        "Mosque",
        "Parsi temple",
        "Pentecostal church",
        "Protestant church",
        "Taoist temple",
    },
}

# Minimal fields per category, based on the reference CSV headers.
BASE_MIN_FIELDS = [
    "name",
    "main_category",
    "category",
    "categoryName",
    "address",
    "street",
    "neighborhood",
    "city",
    "state",
    "postal",
    "country",
    "lat",
    "lng",
    "phone",
    "phoneUnformatted",
    "website",
    "placeId",
    "place_id",
    "rank",
    "rating",
    "reviewsCount",
    "reviews_count",
    "weekly_hours",
    "hours",
    "permanentlyClosed",
    "temporarilyClosed",
    "price",
    "imageUrl",
]

CATEGORY_EXTRA_FIELDS = {
    "cafes": [
        "dine_in",
        "takeout",
        "delivery",
        "breakfast",
        "lunch",
        "dinner",
        "vegetarian",
        "coffee",
        "alcohol",
        "beer",
        "wifi",
        "casual",
        "family_friendly",
        "tourists",
        "reservations",
        "cash_only",
        "wheelchair_accessible_entrance",
    ],
    "banks": [],
    "education": [],
    "health": [],
    "temples": [],
    "other": [],
}

CATEGORY_HEADER_FILES = {
    "cafes": "cafes.csv",
    "banks": "banks.csv",
    "education": "education.csv",
    "health": "health.csv",
    "temples": "temples.csv",
    "other": "other.csv",
}


def _read_header_fields(csv_path: Path) -> list:
    if not csv_path.exists():
        return []
    with csv_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        return next(reader, [])


def _minimal_fields_for_category(category: str, all_fields: set) -> list:
    header_path = REFERENCE_HEADER_DIR / CATEGORY_HEADER_FILES.get(category, "")
    header_fields = _read_header_fields(header_path) if header_path else []
    desired = BASE_MIN_FIELDS + CATEGORY_EXTRA_FIELDS.get(category, [])

    minimal = []
    seen = set()
    for field in desired:
        if header_fields and field not in header_fields:
            continue
        if field not in all_fields:
            continue
        if field in seen:
            continue
        minimal.append(field)
        seen.add(field)

    if minimal:
        return minimal

    # Fallback to base fields only (still minimal).
    for field in BASE_MIN_FIELDS:
        if field in all_fields and field not in seen:
            minimal.append(field)
            seen.add(field)

    return minimal


# ----------------------------------------------------------------------
# 1. Time parsing
# ----------------------------------------------------------------------

def _normalize_space(s: str) -> str:
    return s.replace("\u202f", " ").replace("\xa0", " ").strip()


def _parse_time_str(t: str) -> datetime:
    t = _normalize_space(t).upper()
    fmts = ["%I %p", "%I:%M %p", "%I%p", "%I:%M%p"]
    for fmt in fmts:
        try:
            return datetime.strptime(t, fmt)
        except Exception:
            pass
    raise ValueError(f"Unrecognized time: {t!r}")


def _hours_from_entry(hours_str: str) -> float:
    s = _normalize_space(hours_str)
    if not s or s.lower() in ("closed", "open 24 hours"):
        return 0.0 if s.lower() == "closed" else 24.0
    total_seconds = 0
    ranges = re.split(r"\s*[;,]\s*", s)
    for r in ranges:
        parts = re.split(r"\s*(?:to|–|—|-)\s*", r, flags=re.I)
        if len(parts) < 2:
            continue
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
        total += _hours_from_entry(entry.get("hours", ""))
    return round(total, 2)


def _first_non_empty(*values):
    for value in values:
        if value not in (None, ""):
            return value
    return ""


# ----------------------------------------------------------------------
# 2. Feature detection
# ----------------------------------------------------------------------

def has_feature(data, category, key):
    if not isinstance(data, dict):
        return 0
    additional_info = data.get("additionalInfo") or {}
    if not isinstance(additional_info, dict):
        return 0
    items = additional_info.get(category) or []
    if not isinstance(items, list):
        return 0
    return 1 if any(isinstance(item, str) and key in item for item in items) else 0


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
        5: max(2.0, rating - 1.0),
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

    return {f"reviewsDistribution_{i}Star": counts[i - 1] for i in range(1, 6)}


# ----------------------------------------------------------------------
# 4. Flatten place + handle reviewsDistribution correctly
# ----------------------------------------------------------------------

def flatten_place(data):
    if not isinstance(data, dict):
        return {}
    flat = {}

    # Core
    flat["name"] = data.get("title", "")
    flat["main_category"] = data.get("categoryName", "")
    flat["category"] = (data.get("categories") or [None])[0] or data.get("categoryName", "")
    flat["address"] = _first_non_empty(data.get("address"), data.get("street"), data.get("plusCode"))
    flat["city"] = data.get("city", "")
    flat["postal"] = data.get("postalCode", "")
    flat["country"] = data.get("countryCode", "")
    flat["phone"] = _first_non_empty(data.get("phone"), data.get("phoneUnformatted"))
    flat["website"] = data.get("website", "") or ""
    flat["url"] = data.get("url", "") or ""
    flat["place_id"] = data.get("placeId", "")
    flat["cid"] = data.get("cid", "")
    flat["url"] = data.get("url", "")
    flat["search_term"] = data.get("searchString", "")
    flat["rank"] = data.get("rank", "")

    # Hours
    hours_list = data.get("openingHours", [])
    flat["hours"] = hours_list[0].get("hours", "") if hours_list else ""
    flat["weekly_hours"] = _total_week_hours(hours_list)

    # Metrics
    flat["rating"] = float(data.get("totalScore") or 0)
    flat["reviews_count"] = int(data.get("reviewsCount") or 0)
    loc = data.get("location") or {}
    if not isinstance(loc, dict):
        loc = {}
    flat["lat"] = float((loc.get("lat") if isinstance(loc, dict) else None) or data.get("lat") or 0)
    flat["lng"] = float((loc.get("lng") if isinstance(loc, dict) else None) or data.get("lng") or 0)

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
# 5. Categorization helpers
# ----------------------------------------------------------------------

def _normalize_category(text: str) -> str:
    text = text.lower().replace("_", " ")
    text = re.sub(r"[^a-z0-9\s]", "", text)
    return " ".join(text.split())


def _category_index():
    category_index = {}
    for folder, labels in CATEGORY_RULES.items():
        category_index[folder] = {_normalize_category(label) for label in labels}
    return category_index


def _bucket_for_row(row, category_index):
    category_name = row.get("categoryName")
    if isinstance(category_name, str) and category_name:
        normalized = _normalize_category(category_name)
        for folder in ["cafes", "banks", "education", "health", "temples", "other"]:
            if normalized in category_index.get(folder, set()):
                return folder

    return "other"


# ----------------------------------------------------------------------
# 6. MAIN
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
            key = None
            if lat is not None and lng is not None:
                key = (round(float(lat), 6), round(float(lng), 6))
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
                    total_reviews=total_reviews,
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
                    final_row[field] = 0 if any(
                        x in field for x in ["count", "hours", "Distribution", "Star", "lat", "lng", "rating", "rank"]
                    ) else ""
                else:
                    final_row[field] = val
            rows.append(final_row)

    # Write CSVs
    output_prefix = Path(INPUT_DIR).resolve().name
    full_csv = os.path.join(OUTPUT_DIR, f"{output_prefix}_flattened_all_fields.csv")
    compact_csv = os.path.join(OUTPUT_DIR, f"{output_prefix}_compact_summary.csv")
    summary_csv = os.path.join(OUTPUT_DIR, f"{output_prefix}_category_summary.csv")

    compact_fields = [
        "name","main_category","category","address","street","neighborhood","city",
        "state","postal","country","phone","phoneUnformatted","website","url","price",
        "temporarilyClosed","permanentlyClosed","claimThisBusiness",
        "rank","lat","lng","rating","reviews_count",
        "reviewsDistribution_oneStar","reviewsDistribution_twoStar",
        "reviewsDistribution_threeStar","reviewsDistribution_fourStar","reviewsDistribution_fiveStar",
        "weekly_hours","wifi","dine_in","takeout","delivery",
        "breakfast","lunch","dinner","vegetarian","coffee","alcohol","beer",
        "casual","family_friendly","tourists","reservations","cash_only",
        "wheelchair_accessible_entrance","source_file"
    ]

    numeric_compact_fields = {
        "rank","lat","lng","rating","reviews_count",
        "reviewsDistribution_oneStar","reviewsDistribution_twoStar",
        "reviewsDistribution_threeStar","reviewsDistribution_fourStar","reviewsDistribution_fiveStar",
        "weekly_hours","wifi","dine_in","takeout","delivery",
        "breakfast","lunch","dinner","vegetarian","coffee","alcohol","beer",
        "casual","family_friendly","tourists","reservations","cash_only",
        "wheelchair_accessible_entrance"
    }

    with open(full_csv, "w", newline="", encoding="utf-8") as f_full, \
         open(compact_csv, "w", newline="", encoding="utf-8") as f_compact:

        writer_full = csv.DictWriter(f_full, fieldnames=all_fields)
        writer_full.writeheader()

        writer_compact = csv.DictWriter(f_compact, fieldnames=compact_fields)
        writer_compact.writeheader()

        for row in rows:
            writer_full.writerow(row)
            compact_row = {k: row.get(k, 0 if k in numeric_compact_fields else "") for k in compact_fields}
            writer_compact.writerow(compact_row)

    # Categorize CSVs (write minimal fields per category)
    category_index = _category_index()
    by_category_dir = Path(OUTPUT_DIR) / BY_CATEGORY_DIR
    by_category_dir.mkdir(parents=True, exist_ok=True)

    minimal_fields_by_category = {
        category: _minimal_fields_for_category(category, set(all_fields))
        for category in CATEGORY_RULES.keys()
    }

    writers = {}
    writers_all = {}
    files = {}
    json_buckets = {k: [] for k in CATEGORY_RULES.keys()}
    counts = {k: 0 for k in CATEGORY_RULES.keys()}
    missing_category_counts = {}

    for row in rows:
        bucket = _bucket_for_row(row, category_index)
        category_name = row.get("categoryName") or row.get("main_category") or row.get("category")
        if isinstance(category_name, str) and category_name:
            normalized = _normalize_category(category_name)
            known = False
            for labels in category_index.values():
                if normalized in labels:
                    known = True
                    break
            if not known:
                missing_category_counts[category_name] = missing_category_counts.get(category_name, 0) + 1

        if bucket not in writers:
            out_path = by_category_dir / f"{bucket}.csv"
            f_out = out_path.open("w", encoding="utf-8", newline="")
            files[bucket] = f_out
            fieldnames = minimal_fields_by_category.get(bucket, [])
            writer = csv.DictWriter(f_out, fieldnames=fieldnames)
            writer.writeheader()
            writers[bucket] = writer

            out_path_all = by_category_dir / f"{bucket}_all_data.csv"
            f_out_all = out_path_all.open("w", encoding="utf-8", newline="")
            files[f"{bucket}_all_data"] = f_out_all
            writer_all = csv.DictWriter(f_out_all, fieldnames=all_fields)
            writer_all.writeheader()
            writers_all[bucket] = writer_all

        fieldnames = minimal_fields_by_category.get(bucket, [])
        minimal_row = {k: row.get(k, "") for k in fieldnames}
        writers[bucket].writerow(minimal_row)
        writers_all[bucket].writerow(row)
        counts[bucket] += 1
        json_buckets[bucket].append(row)

    for f_out in files.values():
        f_out.close()


    # Export category CSVs into backend/Data/CSV_Reference (overwrite)
    REFERENCE_EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    for csv_path in by_category_dir.glob("*.csv"):
        shutil.copy2(csv_path, REFERENCE_EXPORT_DIR / csv_path.name)

    # Export category CSVs into a local data/ folder (relative to script)
    local_data_dir = Path(__file__).parent / "data"
    local_data_dir.mkdir(parents=True, exist_ok=True)
    for csv_path in by_category_dir.glob("*.csv"):
        if not csv_path.name.endswith("_all_data.csv"):
            shutil.copy2(csv_path, local_data_dir / csv_path.name)

    # Export category summary CSVs into site_x_ui/data/final (frontend)
    site_x_ui_data_dir = Path(__file__).resolve().parents[5] / "site_x_ui" / "data" / "final"
    site_x_ui_data_dir.mkdir(parents=True, exist_ok=True)
    for csv_path in by_category_dir.glob("*.csv"):
        if not csv_path.name.endswith("_all_data.csv"):
            shutil.copy2(csv_path, site_x_ui_data_dir / csv_path.name)

    for bucket, items in json_buckets.items():
        out_path = by_category_dir / f"{bucket}.json"
        with out_path.open("w", encoding="utf-8") as f_out:
            json.dump(items, f_out, ensure_ascii=False, indent=2)

    with open(summary_csv, "w", newline="", encoding="utf-8") as f_summary:
        writer_summary = csv.writer(f_summary)
        writer_summary.writerow(["category", "count"])
        for folder in ["cafes", "banks", "education", "health", "temples", "other"]:
            writer_summary.writerow([folder, counts.get(folder, 0)])

    missing_csv = os.path.join(OUTPUT_DIR, f"{output_prefix}_missing_category_rule.csv")
    with open(missing_csv, "w", newline="", encoding="utf-8") as f_missing:
        writer_missing = csv.writer(f_missing)
        writer_missing.writerow(["category", "count"])
        for name, count in sorted(missing_category_counts.items()):
            writer_missing.writerow([name, count])

    print("\nDone!")
    print(f"   Input: {total_input}, Unique: {len(rows)}")
    print(f"   Full: {full_csv}")
    print(f"   Compact: {compact_csv}")
    print(f"   Category Summary: {summary_csv}")
    print(f"   Missing Category Rules: {missing_csv}")
    print(f"   By category: {by_category_dir}")
    for folder in CATEGORY_RULES.keys():
        print(f"   {folder}: {counts.get(folder, 0)}")


if __name__ == "__main__":
    main()
