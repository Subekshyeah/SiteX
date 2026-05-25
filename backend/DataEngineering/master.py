#!/usr/bin/env python3
"""
Generate POI-influenced metrics for cafes and write a master CSV.

Creates: backend/Data/master_cafes_metrics.csv
"""

import os
import sys
import math
import argparse
from collections import defaultdict
from typing import Optional, Tuple, List, Dict

import numpy as np
import pandas as pd

BACKEND_ROOT = os.path.dirname(os.path.dirname(__file__))
if BACKEND_ROOT not in sys.path:
    sys.path.insert(0, BACKEND_ROOT)

try:
    from app.lib.road_network import RoadNetwork
except Exception:  # pragma: no cover
    RoadNetwork = None

DATA_DIR = os.path.join(os.path.dirname(__file__), "CSV_Reference")
CAFE_FILE = os.path.join(DATA_DIR, "cafes.csv")
MASTER_OUT = os.path.join(DATA_DIR, "master_cafes_metrics.csv")

ROADWAY_GEOJSON = os.path.join(os.path.dirname(__file__), "Roadway.geojson")
ROAD_GRAPH_CACHE = os.path.join(os.path.dirname(__file__), "road_graph_cache.pkl")
ROAD_SNAP_TOLERANCE_M = 120.0
MASTER_DECAY_M = 1000.0

POI_FILES = {
    "banks": os.path.join(DATA_DIR, "banks.csv"),
    "education": os.path.join(DATA_DIR, "education.csv"),
    "health": os.path.join(DATA_DIR, "health.csv"),
    "temples": os.path.join(DATA_DIR, "temples.csv"),
    "other": os.path.join(DATA_DIR, "other.csv"),
}

# Default category influence weights (can be tuned)
CATEGORY_WEIGHTS = {
    "banks": 0.6,
    "education": 1.0,
    "health": 0.9,
    "temples": 0.8,
    "other": 0.9,
}

# Per-subcategory weights for education POIs. Edit values as needed.
EDUCATION_SUBCAT_WEIGHTS = {
    "College": 1.0,
    "Government school": 1.0,
    "Driving school": 1.0,
    "University": 1.0,
    "High school": 1.0,
    "Higher secondary school": 1.0,
    "International school": 1.0,
    "Language school": 1.0,

    "Library": 0.7,
    "Middle school": 0.7,
    "After school program": 0.5,
    "Art school": 0.7,
    "Drivers license training school": 1.0,
    "Bartending school": 0.8,
    "Boarding school": 0.7,
    "Business school": 0.8,
    "Children_s library": 0.5,
    "Chinese language school": 0.7,
    "Combined primary and secondary school": 0.7,
    "Community college": 0.9,
    "Computer training school": 0.8,
    "Dance school": 0.8,

    "Drawing lessons": 0.5,
    "Education center": 0.5,
    "Educational institution": 0.5,
    "Elementary school": 0.5,
    "English language school": 0.5,
    "Farm school": 0.5,
    "General education school": 0.5,
    "German language school": 0.5,
    "Montessori preschool": 0.5,
    "Montessori school": 0.5,
    "Music school": 0.5,
    "Preschool": 0.5,
    "Primary school": 0.5,
    "Private educational institution": 0.5,
    "School center": 0.5,
    "School house": 0.5,
    "School supply store": 0.5,
    "Secondary school": 0.5,
    "Special education school": 0.5,
    "Taekwondo school": 0.5,
    "Technical school": 0.5,
    "Training center": 0.5,
    "Vocational school": 0.5,
}

BANK_SUBCAT_WEIGHTS = {
    "Bank": 1.0,
    "Cooperative bank": 0.7,
}

HEALTH_SUBCAT_WEIGHTS = {
    "Hospital": 1.0,
    "General hospital": 1.0,
    "Government hospital": 1.0,
    "Dentist": 1.0,
    "Community health center": 1.0,
    "Animal hospital": 1.0,
    "Pharmacy": 1.0,
    "Ayurvedic clinic": 1.0,
    "Acupuncture clinic": 1.0,
    "Public library": 1.0,
    "Software company": 1.0,
    "Medical clinic": 1.0,
    "Orthopedic clinic": 1.0,
    "Dental clinic": 1.0,

    "Blood bank": 0.5,
    "Cancer treatment center": 0.5,
    "Child health care center": 0.5,
    "Faculty of pharmacy": 0.5,
    "Health and beauty shop": 0.5,
    "Health consultant": 0.5,
    "Health food store": 0.5,
    "Health insurance agency": 0.5,
    "Home health care service": 0.5,
    "Hospital department": 0.5,
    "Hospital equipment and supplies": 0.5,
    "Hospitality and tourism school": 0.5,
    "Mental health service": 0.5,
    "Naturopathic practitioner": 0.5,
    "Occupational health service": 0.5,
    "Pain management physician": 0.5,
    "Physical therapy c": 0.5,
    "Private hospital": 0.5,
    "Savings bank": 0.5,
    "Self service health station": 0.5,
    "Ticket office": 0.5,
    "Tour operator": 0.5,
    "Traffic police station": 0.5,
    "Travel agency": 0.5,
    "Veterinarian": 0.5,
    "Veterinary pharmacy": 0.5,
}

OTHER_SUBCAT_WEIGHTS = {
    "Federal government office": 1.0,
    "District office": 1.0,
    "Post office": 1.0,
    "Political party office": 1.0,
    "State government office": 1.0,
    "Government economic program": 1.0,
    "Local government office": 1.0,
    "Memorial park": 1.0,
    "Athletic park": 1.0,
    "Boxing gym": 1.0,
    "Garden": 1.0,
    "Gym": 1.0,
    "Government office": 1.0,
    "Government": 1.0,
    "Park _ ride": 1.0,
    "Park": 1.0,
    "Muay Thai boxing gym": 1.0,
    "Corporate office": 1.0,

    "Water park": 0.6,
    "Banquet hall": 0.6,
    "Adventure sports center": 0.6,
    "Beauty salon": 0.6,
    "Beauty school": 0.6,
    "Business park": 0.6,
    "City government office": 0.6,
    "Community garden": 0.6,
    "Financial institution": 0.6,
    "Food bank": 0.6,
    "Military school": 0.6,
    "Mobile home park": 0.6,
    "Office supply store": 0.6,
    "Photography studio": 0.6,
    "Plaza": 0.6,
}

TEMPLE_SUBCAT_WEIGHTS = {
    "Buddhist temple": 1.0,
    "Hindu temple": 1.0,
    "Tourist attraction": 1.0,
}

# Radius to use for master aggregation (meters) — set to 1.5 km
MASTER_RADIUS_M = 1500
DEFAULT_WEEKLY = 12 * 6
# weight to apply to cafe-level properties when computing composite
CAFE_PROPS_WEIGHT = 1.0
# weight to apply to nearby cafes' combined properties
CAFE_NEIGHBOR_WEIGHT = 1.0

# Candidate names for lat/lon columns in CSVs
LAT_COL_CANDS = ["lat", "latitude", "y", "LAT", "Latitude"]
LON_COL_CANDS = ["lon", "lng", "longitude", "x", "LON", "Longitude"]

# Candidate names for per-POI weight columns
WEIGHT_COL_CANDS = ["weight", "importance", "rating", "score", "pop", "count", "rank"]
RATING_COL_CANDS = ["rating", "stars"]
REVIEWS_COL_CANDS = ["reviewsCount", "reviews_count", "reviews", "reviewscount", "reviews_count"]
WEEKLY_HOURS_COL_CANDS = [
    "weekly_hours",
    "weeklyHours",
    "hours_per_week",
    "weekly_open_hours",
    "open_hours_week",
    "weeklyopenhours",
    "hours_week",
    "weekly_opening_hours",
    "opening_hours_week",
]


def haversine_m(lat1: float, lon1: float, lat2: np.ndarray, lon2: np.ndarray) -> np.ndarray:
    """
    Vectorized haversine distance (meters) from a single point (lat1,lon1)
    to arrays lat2, lon2 (in degrees).
    """
    R = 6371000.0  # earth radius in meters
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = np.radians(lat2)
    lon2_rad = np.radians(lon2)
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    a = np.sin(dlat / 2.0) ** 2 + np.cos(lat1_rad) * np.cos(lat2_rad) * np.sin(dlon / 2.0) ** 2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    return R * c


def detect_latlon(df: pd.DataFrame) -> Optional[Tuple[str, str]]:
    for latc in LAT_COL_CANDS:
        for lonc in LON_COL_CANDS:
            if latc in df.columns and lonc in df.columns:
                return latc, lonc
    # fallback: try common pairs
    pairs = [("latitude", "longitude"), ("lat", "lon"), ("y", "x")]
    for (a, b) in pairs:
        if a in df.columns and b in df.columns:
            return a, b
    return None


def detect_weight_col(df: pd.DataFrame) -> Optional[str]:
    # Prefer an explicit rank column if present (may be named 'rank' or contain 'rank')
    for c in df.columns:
        if "rank" == c.lower() or "rank" in c.lower():
            return c
    for c in WEIGHT_COL_CANDS:
        if c in df.columns:
            return c
    return None


def detect_name_col(df: pd.DataFrame) -> Optional[str]:
    # common name/title columns
    for c in ("name", "title", "place", "place_name"):
        if c in df.columns:
            return c
    return None


def compute_poi_metrics_for_cafes(
    cafes: pd.DataFrame,
    poi: pd.DataFrame,
    poi_name: str,
    category_weight: float,
    radius_m: float = 1000.0,
    road_network: Optional["RoadNetwork"] = None,
    snap_tolerance_m: float = ROAD_SNAP_TOLERANCE_M,
    decay_scale_m: float = MASTER_DECAY_M,
) -> pd.DataFrame:
    latlon = detect_latlon(poi)
    if latlon is None:
        # no coordinates in POI, return zeros
        cafes[f"{poi_name}_count_1km"] = 0
        cafes[f"{poi_name}_weight_1km"] = 0.0
        cafes[f"{poi_name}_min_dist_m"] = np.nan
        return cafes

    poi_lat_col, poi_lon_col = latlon
    poi_lats = pd.to_numeric(poi[poi_lat_col], errors="coerce").to_numpy(dtype=float)
    poi_lons = pd.to_numeric(poi[poi_lon_col], errors="coerce").to_numpy(dtype=float)

    weight_col = detect_weight_col(poi)
    # if a precomputed weight column exists (created by helper), use it
    if "_computed_weight" in poi.columns:
        poi_weights = pd.to_numeric(poi["_computed_weight"], errors="coerce").fillna(1.0).to_numpy().astype(float)
    else:
        # gather optional rating/review columns
        def _detect_rating_col(df: pd.DataFrame) -> Optional[str]:
            for c in RATING_COL_CANDS:
                if c in df.columns:
                    return c
            return None

        def _detect_reviews_col(df: pd.DataFrame) -> Optional[str]:
            for c in REVIEWS_COL_CANDS:
                if c in df.columns:
                    return c
            return None

        rating_col = _detect_rating_col(poi)
        reviews_col = _detect_reviews_col(poi)

        if weight_col is not None:
            raw_vals = pd.to_numeric(poi[weight_col], errors="coerce")
            # base score from rank-like column (lower is better)
            if "rank" in weight_col.lower():
                maxr = raw_vals.max(skipna=True)
                if pd.isna(maxr) or maxr <= 0:
                    maxr = 1.0
                fill_val = float(maxr) + 1.0
                ranks = raw_vals.fillna(fill_val).replace(0.0, fill_val).astype(float)
                inv = 1.0 / (ranks + 1e-9)
                base_norm = inv / float(inv.max()) if inv.max() > 0 else pd.Series(np.ones(len(ranks)), index=ranks.index)
            else:
                # treat column as higher-is-better; normalize by max
                v = raw_vals.fillna(0.0).astype(float)
                base_norm = v / float(v.max()) if v.max() > 0 else pd.Series(np.zeros(len(v)), index=v.index)

            # optional rating and reviews influence
            rating_vals = pd.to_numeric(poi[rating_col], errors="coerce") if rating_col is not None else None
            reviews_vals = pd.to_numeric(poi[reviews_col], errors="coerce") if reviews_col is not None else None

            # Use base/rank and (optionally) reviews only — do NOT use rating or weekly-hours
            comps = [base_norm]
            if reviews_vals is not None:
                rv = reviews_vals.fillna(0.0).astype(float)
                maskr = rv > 0
                if maskr.any():
                    # log-scale normalize by max
                    norm_rev = pd.Series(0.0, index=rv.index)
                    maxlog = float(np.log1p(rv[maskr]).max())
                    if maxlog > 0:
                        norm_rev[maskr] = np.log1p(rv[maskr]) / maxlog
                    comps.append(norm_rev)

            # final per-POI weight is mean of available components
            stacked = np.vstack([c.to_numpy() for c in comps])
            poi_weights = np.nanmean(stacked, axis=0).astype(float)
        else:
            # no explicit weight column: use reviews only (do NOT use rating or weekly-hours)
            reviews_vals = pd.to_numeric(poi[reviews_col], errors="coerce") if reviews_col is not None else None
            if reviews_vals is not None:
                rv = reviews_vals.fillna(0.0).astype(float)
                maskr = rv > 0
                norm_rev = pd.Series(0.0, index=rv.index)
                if maskr.any():
                    maxlog = float(np.log1p(rv[maskr]).max())
                    if maxlog > 0:
                        norm_rev[maskr] = np.log1p(rv[maskr]) / maxlog
                    poi_weights = norm_rev.to_numpy().astype(float)
                else:
                    poi_weights = np.ones_like(poi_lats, dtype=float)
            else:
                poi_weights = np.ones_like(poi_lats, dtype=float)

    poi_weights = np.asarray(poi_weights, dtype=float)

    # Prepare result columns (use suffix based on radius)
    try:
        suffix = f"_{int(radius_m/1000)}km"
    except Exception:
        suffix = "_1km"
    counts = []
    weight_sums = []
    min_dists = []

    # detect cafe lat/lon columns
    cafe_latlon = detect_latlon(cafes)
    if cafe_latlon is None:
        raise ValueError("Could not detect lat/lon in cafes CSV")

    cafe_lat_col, cafe_lon_col = cafe_latlon
    cafe_lats = pd.to_numeric(cafes[cafe_lat_col], errors="coerce").to_numpy(dtype=float)
    cafe_lons = pd.to_numeric(cafes[cafe_lon_col], errors="coerce").to_numpy(dtype=float)

    use_network = bool(road_network) and getattr(road_network, "node_count", 0) > 0
    node_to_poi: Dict[int, List[int]] = defaultdict(list)
    poi_snap_offsets: List[float] = []
    if use_network:
        poi_nodes, poi_snap_offsets = road_network.snap_points(poi_lats, poi_lons, max_snap_m=snap_tolerance_m)
        for idx, node_id in enumerate(poi_nodes):
            if node_id is not None and math.isfinite(poi_snap_offsets[idx]):
                node_to_poi[int(node_id)].append(idx)
        if not node_to_poi:
            use_network = False

    def _network_stats(cafe_node: int, cafe_offset: float) -> Optional[Tuple[int, float, float]]:
        if not use_network:
            return None
        lengths = road_network.shortest_paths_from(cafe_node, cutoff=radius_m)
        if not lengths:
            return None
        total_count = 0
        total_weight = 0.0
        min_dist = None
        for node_id, path_dist in lengths.items():
            poi_indices = node_to_poi.get(node_id)
            if not poi_indices:
                continue
            for poi_idx in poi_indices:
                total_dist = path_dist + cafe_offset + poi_snap_offsets[poi_idx]
                if total_dist <= radius_m:
                    total_count += 1
                    try:
                        decayed = float(poi_weights[poi_idx]) * math.exp(-(float(total_dist) / float(decay_scale_m)))
                    except Exception:
                        decayed = float(poi_weights[poi_idx])
                    total_weight += decayed
                    if min_dist is None or total_dist < min_dist:
                        min_dist = total_dist
        if total_count == 0 or min_dist is None:
            return None
        return total_count, total_weight, float(min_dist)

    # Iterate cafes and compute distances
    for i in range(len(cafes)):
        lat = cafe_lats[i]
        lon = cafe_lons[i]
        if not math.isfinite(lat) or not math.isfinite(lon):
            counts.append(0)
            weight_sums.append(0.0)
            min_dists.append(float(np.nan))
            continue
        if use_network:
            cafe_node, cafe_offset = road_network.snap_point(lat, lon, max_snap_m=snap_tolerance_m)
            if cafe_node is not None:
                cafe_offset = float(cafe_offset or 0.0)
                net_stats = _network_stats(cafe_node, cafe_offset)
                if net_stats is not None:
                    cnt, wsum, mind = net_stats
                    counts.append(int(cnt))
                    weight_sums.append(float(wsum))
                    min_dists.append(float(mind))
                    continue
        dists = haversine_m(lat, lon, poi_lats, poi_lons)  # meters
        within_mask = dists <= radius_m
        counts.append(int(np.count_nonzero(within_mask)))
        if np.any(within_mask):
            try:
                ds = dists[within_mask].astype(float)
                pws = poi_weights[within_mask].astype(float)
                decayed_arr = pws * np.exp(-(ds / float(decay_scale_m)))
                weight_sum = float(np.sum(decayed_arr))
            except Exception:
                weight_sum = float(np.sum(poi_weights[within_mask]))
            weight_sums.append(weight_sum)
            min_dists.append(float(np.min(dists[within_mask])))
        else:
            weight_sums.append(0.0)
            min_dists.append(float(np.nan))

    cafes[f"{poi_name}_count{suffix}"] = counts
    cafes[f"{poi_name}_weight{suffix}"] = weight_sums
    cafes[f"{poi_name}_min_dist_m"] = min_dists

    # Also store category weight so downstream composite score can use it
    cafes[f"{poi_name}_category_weight"] = category_weight

    return cafes


def generate_master_metrics(
    cafe_file: str = CAFE_FILE,
    poi_files: Dict[str, str] = POI_FILES,
    category_weights: Dict[str, float] = CATEGORY_WEIGHTS,
    out_file: str = MASTER_OUT,
    road_geojson_path: Optional[str] = ROADWAY_GEOJSON,
    use_road_network: bool = True,
    road_cache_path: Optional[str] = ROAD_GRAPH_CACHE,
    snap_tolerance_m: float = ROAD_SNAP_TOLERANCE_M,
    decay_scale_m: float = MASTER_DECAY_M,
):
    cafes = pd.read_csv(cafe_file)
    if detect_latlon(cafes) is None:
        raise ValueError(f"Could not detect lat/lon columns in cafes file: {cafe_file}")

    # Ensure deterministic order
    cafes = cafes.reset_index(drop=True)

    road_network = None
    if use_road_network and road_geojson_path and RoadNetwork is not None:
        try:
            road_network = RoadNetwork.from_geojson(
                road_geojson_path,
                cache_path=road_cache_path,
                snap_tolerance_m=snap_tolerance_m,
            )
            print(
                "Loaded road network graph: "
                f"{road_network.node_count} nodes / {road_network.edge_count} edges."
            )
        except Exception as exc:
            print(f"Warning: Failed to initialize road network ({exc}); using haversine distances.")
            road_network = None
    elif use_road_network and RoadNetwork is None:
        print("Warning: RoadNetwork utilities unavailable; using haversine distances instead.")

    # For each POI dataset, compute metrics and merge into cafes
    # Use configured radius for master aggregation unless overridden
    master_radius = MASTER_RADIUS_M
    for name, path in poi_files.items():
        if not os.path.exists(path):
            cafes[f"{name}_count_1km"] = 0
            cafes[f"{name}_weight_1km"] = 0.0
            cafes[f"{name}_min_dist_m"] = np.nan
            cafes[f"{name}_category_weight"] = category_weights.get(name, 1.0)
            continue
        poi = pd.read_csv(path)
        # compute per-POI weights, annotate POI df, save per-category CSV
        try:
            annotated_poi, weights, dyn_cat_w = compute_weights_and_annotate(poi, name)
        except Exception:
            annotated_poi = poi.copy()
            weights = np.ones(len(poi), dtype=float)
            dyn_cat_w = float(category_weights.get(name, 1.0))
        # save annotated POI data
        out_path = os.path.join(DATA_DIR, f"{name}_all_data.csv")
        try:
            annotated_poi.to_csv(out_path, index=False)
            print(f"Wrote annotated POI data for {name} to: {out_path}")
        except Exception:
            pass
        # also write a lightweight final CSV with only name, lat, lon, category (if available)
        try:
            final_cols = []
            # detect name and lat/lon in annotated poi
            poi_name_col = detect_name_col(annotated_poi)
            latlon = detect_latlon(annotated_poi)
            category_col = None
            for c in ("category", "type", "place_type", "amenity", "class"):
                if c in annotated_poi.columns:
                    category_col = c
                    break
            if poi_name_col is not None:
                final_cols.append(poi_name_col)
            if latlon is not None:
                final_cols.extend([latlon[0], latlon[1]])
            if category_col is not None:
                final_cols.append(category_col)
            # include subcategory weight for education POIs
            if name == "education" and "subcategory_weight" in annotated_poi.columns and "subcategory_weight" not in final_cols:
                final_cols.append("subcategory_weight")
            # include computed weight/score if present
            if "_computed_weight" in annotated_poi.columns:
                final_cols.append("_computed_weight")
            elif "combined_score" in annotated_poi.columns:
                final_cols.append("combined_score")
            # include original weight/rank column(s) if present so final CSV preserves rank info
            detected_wc = detect_weight_col(annotated_poi)
            if detected_wc is not None and detected_wc not in final_cols:
                final_cols.append(detected_wc)
            # include any explicit rank-like columns (e.g., 'rank', 'filled_rank')
            for c in annotated_poi.columns:
                try:
                    if "rank" == c.lower() or "rank" in c.lower():
                        if c not in final_cols:
                            final_cols.append(c)
                except Exception:
                    continue
            if final_cols:
                # ensure uniqueness and preserve order
                seen = set()
                final_cols = [x for x in final_cols if not (x in seen or seen.add(x))]
                final_df = annotated_poi.loc[:, final_cols].copy()
                # normalize column name for final weight
                if "_computed_weight" in final_df.columns:
                    final_df = final_df.rename(columns={"_computed_weight": "final_weight"})
                if "combined_score" in final_df.columns and "final_weight" not in final_df.columns:
                    final_df = final_df.rename(columns={"combined_score": "final_weight"})
                # ensure final output folder exists
                final_dir = os.path.join(DATA_DIR, "final")
                os.makedirs(final_dir, exist_ok=True)
                final_out = os.path.join(final_dir, f"{name}_final.csv")
                final_df.to_csv(final_out, index=False)
                print(f"Wrote final POI CSV for {name} to: {final_out}")
        except Exception:
            pass
        # override the category weight for this category so later scoring uses the dynamic value
        category_weights[name] = dyn_cat_w
        # pass annotated poi (which includes '_computed_weight') into metric computation
        cafes = compute_poi_metrics_for_cafes(
            cafes,
            annotated_poi,
            name,
            dyn_cat_w,
            radius_m=master_radius,
            road_network=road_network,
            snap_tolerance_m=snap_tolerance_m,
            decay_scale_m=decay_scale_m,
        )

    # After processing all POI categories, build the composite score (using master radius)
    suffix = f"_{int(master_radius/1000)}km"
    score_components = []
    for pname in poi_files.keys():
        weight_col = f"{pname}_weight{suffix}"
        cat_w = cafes.get(f"{pname}_category_weight", series_or_scalar(category_weights.get(pname, 1.0)))
        max_val = cafes[weight_col].max() if weight_col in cafes.columns else 0.0
        if pd.isna(max_val) or max_val == 0:
            norm = np.zeros(len(cafes))
        else:
            norm = cafes[weight_col].astype(float) / float(max_val)
        score_components.append(norm * float(category_weights.get(pname, 1.0)))

    # Include cafe-level properties (rating, reviews, weekly_hours, rank) as an additional component
    cafe_prop_components = []
    # rating: intentionally ignored for cafe-level scoring (use star-distribution + review counts instead)
    caf_rating_col = None
    for c in RATING_COL_CANDS:
        if c in cafes.columns:
            caf_rating_col = c
            break
    # reviews
    caf_reviews_col = None
    for c in REVIEWS_COL_CANDS:
        if c in cafes.columns:
            caf_reviews_col = c
            break
    if caf_reviews_col is not None:
        rv = pd.to_numeric(cafes[caf_reviews_col], errors="coerce").fillna(0.0).astype(float)
        logv = np.log1p(rv)
        maxlog = float(logv.max()) if logv.max() > 0 else 1.0
        cafe_prop_components.append((logv / maxlog).to_numpy())
    # weekly hours
    caf_weekly_col = None
    for c in WEEKLY_HOURS_COL_CANDS:
        if c in cafes.columns:
            caf_weekly_col = c
            break
    if caf_weekly_col is not None:
        wh = pd.to_numeric(cafes[caf_weekly_col], errors="coerce").fillna(DEFAULT_WEEKLY).astype(float)
        cafe_prop_components.append((wh / float(DEFAULT_WEEKLY)).clip(0.0, 1.0).to_numpy())
    # do not use any cafe-level `rank` column in scoring

    if cafe_prop_components:
        cafe_props = np.nanmean(np.vstack(cafe_prop_components), axis=0)
        score_components.append(cafe_props * float(CAFE_PROPS_WEIGHT))

    # Compute sum of nearby cafes' property-weights for each cafe (exclude itself)
    try:
        cafe_latlon = detect_latlon(cafes)
        if cafe_latlon is not None:
            clat_col, clon_col = cafe_latlon
            cafe_lats = cafes[clat_col].astype(float).to_numpy()
            cafe_lons = cafes[clon_col].astype(float).to_numpy()
            # ensure cafe_props exists
            if 'cafe_props' not in locals():
                cafe_props = np.zeros(len(cafes), dtype=float)
            nearby_vals = []
            for i in range(len(cafes)):
                dists = haversine_m(cafe_lats[i], cafe_lons[i], cafe_lats, cafe_lons)
                mask = (dists <= master_radius)
                mask[i] = False
                nearby_vals.append(float(np.sum(cafe_props[mask])))
            nearby_arr = np.array(nearby_vals, dtype=float)
            # save raw nearby weight column
            cafes[f"cafes_nearby_weight{suffix}"] = nearby_arr
            # normalize nearby_arr to 0..1 for inclusion
            maxn = float(nearby_arr.max()) if nearby_arr.size > 0 else 0.0
            if maxn > 0:
                nearby_norm = nearby_arr / maxn
            else:
                nearby_norm = np.zeros_like(nearby_arr)
            score_components.append(nearby_norm * float(CAFE_NEIGHBOR_WEIGHT))
            # also compute count of other cafes within 1km
            try:
                count_radius = 1000.0
                cafe_counts_1km = []
                for i in range(len(cafes)):
                    dists = haversine_m(cafe_lats[i], cafe_lons[i], cafe_lats, cafe_lons)
                    maskc = (dists <= count_radius)
                    maskc[i] = False
                    cafe_counts_1km.append(int(np.count_nonzero(maskc)))
                cafes[f"cafes_count_1km"] = cafe_counts_1km
            except Exception:
                cafes[f"cafes_count_1km"] = 0
    except Exception:
        pass

    if score_components:
        composite = np.sum(np.vstack(score_components), axis=0)
    else:
        composite = np.zeros(len(cafes))

    cafes["poi_composite_score"] = composite

    # Ensure `cafe_props` exists and save individual cafe-level score
    if 'cafe_props' not in locals():
        cafe_props = np.zeros(len(cafes), dtype=float)
    cafes["cafe_individual_score"] = cafe_props

    # Normalize individual score to create a cafe-level weight (0..1)
    try:
        max_ind = float(np.nanmax(cafe_props)) if len(cafe_props) > 0 else 0.0
    except Exception:
        max_ind = 0.0
    if max_ind > 0:
        cafes["cafe_weight"] = cafe_props / max_ind
    else:
        cafes["cafe_weight"] = 0.0

    # Save master
    cafes.to_csv(out_file, index=False)
    print(f"Master dataset written to: {out_file}")

    # Also write a fuller cafe_final CSV with per-cafe individual score, weight and POI counts
    try:
        final_dir = os.path.join(DATA_DIR, "final")
        os.makedirs(final_dir, exist_ok=True)
        # choose a set of useful columns for cafe_final
        cols = []
        title_col = detect_name_col(cafes)
        if title_col is not None:
            cols.append(title_col)
        cafe_latlon = detect_latlon(cafes)
        if cafe_latlon is not None:
            cols.extend([cafe_latlon[0], cafe_latlon[1]])
        # basic cafe fields (exclude raw `rating` and raw `rank` columns from outputs and scoring)
        for c in (caf_reviews_col, caf_weekly_col):
            if c is not None and c in cafes.columns:
                cols.append(c)
        # include individual score and weight
        cols.append("cafe_individual_score")
        cols.append("cafe_weight")
        # include POI counts and weights for visibility
        for pname in poi_files.keys():
            count_col = f"{pname}_count{suffix}"
            wcol = f"{pname}_weight{suffix}"
            if count_col in cafes.columns:
                cols.append(count_col)
            if wcol in cafes.columns:
                cols.append(wcol)
        # ensure uniqueness and fallback to full frame if empty
        seen = set()
        final_cols = [x for x in cols if not (x in seen or seen.add(x))]
        if not final_cols:
            final_df = cafes.copy()
        else:
            final_df = cafes.loc[:, final_cols].copy()
        # add per-category ranks (higher weight/count gets rank 1)
        for pname in poi_files.keys():
            wcol = f"{pname}_weight{suffix}"
            count_col = f"{pname}_count{suffix}"
            rank_col = f"{pname}_rank"
            if wcol in final_df.columns:
                try:
                    final_df[rank_col] = final_df[wcol].rank(method="min", ascending=False)
                except Exception:
                    final_df[rank_col] = pd.NA
            elif count_col in final_df.columns:
                try:
                    final_df[rank_col] = final_df[count_col].rank(method="min", ascending=False)
                except Exception:
                    final_df[rank_col] = pd.NA
        final_out = os.path.join(final_dir, "cafe_final.csv")
        final_df.to_csv(final_out, index=False)
        print(f"Wrote cafe final CSV to: {final_out}")
    except Exception:
        pass

    # Also write a minimal master with only title (or name) and assigned scores
    try:
        title_col = detect_name_col(cafes) or "title"
        minimal_cols = []
        if title_col in cafes.columns:
            minimal_cols.append(title_col)
        # include cafe lat/lon if available
        cafe_latlon = detect_latlon(cafes)
        if cafe_latlon is not None:
            lat_col, lon_col = cafe_latlon
            # insert lat/lon after title
            minimal_cols.append(lat_col)
            minimal_cols.append(lon_col)
        # include cafe category if present
        category_col = None
        for c in ("category", "categoryName", "main_category"):
            if c in cafes.columns:
                category_col = c
                break
        if category_col is not None:
            minimal_cols.append(category_col)
        # include counts and weights per POI category
        for pname in poi_files.keys():
            count_col = f"{pname}_count{suffix}"
            wcol = f"{pname}_weight{suffix}"
            if count_col in cafes.columns:
                minimal_cols.append(count_col)
            if wcol in cafes.columns:
                minimal_cols.append(wcol)
        # include computed cafe weight and composite score
        minimal_cols.append("cafe_weight")
        minimal_cols.append("poi_composite_score")
        minimal_df = cafes.loc[:, minimal_cols].copy()
        minimal_out_dir = os.path.join(DATA_DIR, "final")
        os.makedirs(minimal_out_dir, exist_ok=True)
        minimal_out = os.path.join(minimal_out_dir, "master_cafes_minimal.csv")
        minimal_df.to_csv(minimal_out, index=False)
        print(f"Wrote minimal master CSV to: {minimal_out}")
    except Exception:
        pass


def compute_weights_and_annotate(poi: pd.DataFrame, name: str) -> Tuple[pd.DataFrame, np.ndarray, float]:
    """Compute per-row combined weight from rank/weight, rating, and reviews.
    Returns (annotated_poi_df, weights_array, dynamic_category_weight).
    """
    df = poi.copy()
    wc = detect_weight_col(df)
    name_col = detect_name_col(df)

    # Assign per-subcategory weights based on category name
    mapping = None
    default_weight = 0.5

    if name == "education":
        mapping = EDUCATION_SUBCAT_WEIGHTS
    elif name == "banks":
        mapping = BANK_SUBCAT_WEIGHTS
    elif name == "health":
        mapping = HEALTH_SUBCAT_WEIGHTS
    elif name == "other":
        mapping = OTHER_SUBCAT_WEIGHTS
    elif name == "temples":
        mapping = TEMPLE_SUBCAT_WEIGHTS

    if mapping is not None:
        # detect a category-like column
        cat_col = None
        for c in ("category", "type", "place_type", "amenity", "class", "categoryName", "main_category"):
            if c in df.columns:
                cat_col = c
                break
        if cat_col is not None:
            df["subcategory"] = df[cat_col]
            # Map weights; if subcategory not in mapping, default to 0.5
            df["subcategory_weight"] = df[cat_col].map(mapping).fillna(0.5).astype(float)
        else:
            df["subcategory_weight"] = default_weight
    else:
        # Fallback if no mapping found or category not configured
        df["subcategory_weight"] = 1.0

    # detect rating/reviews
    rating_col = None
    reviews_col = None
    weekly_col = None
    # use module-level DEFAULT_WEEKLY
    for c in RATING_COL_CANDS:
        if c in df.columns:
            rating_col = c
            break
    for c in REVIEWS_COL_CANDS:
        if c in df.columns:
            reviews_col = c
            break
    for c in WEEKLY_HOURS_COL_CANDS:
        if c in df.columns:
            weekly_col = c
            break

    vals = pd.to_numeric(df[wc], errors="coerce") if wc is not None else pd.Series([np.nan] * len(df))

    # base score
    if wc is not None and "rank" in wc.lower():
        maxr = vals.max(skipna=True)
        if pd.isna(maxr) or maxr <= 0:
            maxr = 1.0
        fill_val = float(maxr) + 1.0
        ranks = vals.fillna(fill_val).replace(0.0, fill_val).astype(float)
        inv = 1.0 / (ranks + 1e-9)
        base = inv / float(inv.max()) if inv.max() > 0 else pd.Series(np.ones(len(ranks)), index=ranks.index)
        df["filled_rank"] = ranks
        df["base_score"] = base
    elif wc is not None:
        v = vals.fillna(0.0).astype(float)
        base = v / float(v.max()) if v.max() > 0 else pd.Series(np.zeros(len(v)), index=v.index)
        df["filled_value"] = v
        df["base_score"] = base
    else:
        base = pd.Series(np.zeros(len(df)), index=df.index)
        df["base_score"] = base

    # rating
    if rating_col is not None:
        r = pd.to_numeric(df[rating_col], errors="coerce").fillna(0.0).astype(float)
        df["rating_raw"] = r
        df["rating_norm"] = (r / 5.0).clip(0.0, 1.0)
    else:
        df["rating_raw"] = np.nan
        df["rating_norm"] = 0.0

    # reviews
    if reviews_col is not None:
        rv = pd.to_numeric(df[reviews_col], errors="coerce").fillna(0.0).astype(float)
        df["reviews_raw"] = rv
        logv = np.log1p(rv)
        maxlog = float(logv.max()) if logv.max() > 0 else 1.0
        df["reviews_norm"] = (logv / maxlog) if maxlog > 0 else 0.0
    else:
        df["reviews_raw"] = np.nan
        df["reviews_norm"] = 0.0

    # weekly hours
    if weekly_col is not None:
        wh = pd.to_numeric(df[weekly_col], errors="coerce")
        wh = wh.fillna(DEFAULT_WEEKLY).astype(float)
        # treat 0 or implausibly large values (>115) as missing and set to DEFAULT_WEEKLY
        mask_bad = (wh == 0) | (wh > 115)
        if mask_bad.any():
            wh.loc[mask_bad] = float(DEFAULT_WEEKLY)
        df["weekly_hours_raw"] = wh
        # normalize against DEFAULT_WEEKLY (cap at 1.0)
        df["weekly_hours_norm"] = (wh / float(DEFAULT_WEEKLY)).clip(0.0, 1.0)
    else:
        # if not present, assume DEFAULT_WEEKLY for all rows (so normalized factor = 1.0)
        df["weekly_hours_raw"] = float(DEFAULT_WEEKLY)
        df["weekly_hours_norm"] = 1.0

    # combine available components: base (+ subcategory for education) and reviews only
    comps = [df["base_score"].to_numpy()]
    # include subcategory weight for education if present
    if "subcategory_weight" in df.columns:
        comps.append(df["subcategory_weight"].to_numpy())
    # include reviews influence only (do NOT include rating or weekly-hours)
    if reviews_col is not None and (df["reviews_raw"].fillna(0.0) > 0).any():
        comps.append(df["reviews_norm"].to_numpy())

    stacked = np.vstack(comps)
    combined = np.nanmean(stacked, axis=0)
    df["combined_score"] = combined
    df["_computed_weight"] = combined

    dyn_cat_w = float(np.nanmean(combined)) if len(combined) > 0 else 1.0
    return df, combined.astype(float), dyn_cat_w

    

    dyn_cat_w = float(np.nanmean(combined)) if len(combined) > 0 else 1.0
    return df, combined.astype(float), dyn_cat_w


def series_or_scalar(x):
    # helper to allow retrieving category weight when column absent
    return x


def main():
    parser = argparse.ArgumentParser(description="Generate cafe POI metrics and master dataset.")
    parser.add_argument("--cafes", default=CAFE_FILE, help="Path to cafes CSV")
    parser.add_argument("--out", default=MASTER_OUT, help="Output master CSV path")
    parser.add_argument(
        "--road-geojson",
        default=ROADWAY_GEOJSON,
        help="Path to Roadway.geojson for network distances (set empty to skip)",
    )
    parser.add_argument(
        "--road-cache",
        default=ROAD_GRAPH_CACHE,
        help="Optional cache file for serialized road graph",
    )
    parser.add_argument(
        "--disable-road-network",
        action="store_true",
        help="Force fallback to direct haversine distances",
    )
    parser.add_argument(
        "--snap-max-meters",
        type=float,
        default=ROAD_SNAP_TOLERANCE_M,
        help="Maximum allowed snap distance from a point to the nearest road node",
    )
    parser.add_argument(
        "--decay-scale-meters",
        type=float,
        default=MASTER_DECAY_M,
        help="Exponential decay length scale in meters for POI weight decay (default: 1000)",
    )
    args = parser.parse_args()

    road_geojson = args.road_geojson if args.road_geojson else None
    generate_master_metrics(
        cafe_file=args.cafes,
        out_file=args.out,
        road_geojson_path=road_geojson,
        use_road_network=not args.disable_road_network,
        road_cache_path=args.road_cache,
        snap_tolerance_m=args.snap_max_meters,
        decay_scale_m=args.decay_scale_meters,
    )


if __name__ == "__main__":
    main()