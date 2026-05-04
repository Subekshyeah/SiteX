"""
node_features.py — Per-node feature vector computation for the SiteX GNN.

Three node types are supported:

  junction  — OSMnx road intersections
                x = [lat_norm, lon_norm, degree, street_count]

  cafe      — each cafe from cafes.csv / master_cafes_metrics.csv
                x = [lat_norm, lon_norm, reviews_norm, weekly_hours_norm,
                     rating_norm, snap_dist_norm,
                     banks_count_norm, education_count_norm, health_count_norm,
                     temples_count_norm, other_count_norm,
                     poi_composite_norm, cafe_weight]

  poi       — banks / education / health / temples / other POIs
                x = [lat_norm, lon_norm, rating_norm, reviews_norm,
                     subcategory_weight, snap_dist_norm,
                     <category one-hot: 5 dims>]

All normalisations are min-max over the dataset being processed and are
stored inside the returned NodeFeatureMeta so that you can apply the same
transform to unseen (inference-time) nodes.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

POI_CATEGORIES: List[str] = ["banks", "education", "health", "temples", "other"]
DEFAULT_WEEKLY_HOURS = 72.0  # assumed default when missing (12 h × 6 days)
MAX_RATING = 5.0


# ---------------------------------------------------------------------------
# Helper — safe min-max normalisation
# ---------------------------------------------------------------------------

def _minmax(arr: np.ndarray, lo: float, hi: float) -> np.ndarray:
    span = hi - lo
    if span < 1e-9:
        return np.zeros_like(arr, dtype=np.float32)
    return np.clip((arr - lo) / span, 0.0, 1.0).astype(np.float32)


def _log1p_norm(arr: np.ndarray) -> Tuple[np.ndarray, float]:
    """Log-normalise a count/review array. Returns (normed, max_log_value)."""
    log_arr = np.log1p(arr.astype(np.float64))
    max_val = float(log_arr.max()) if log_arr.size > 0 else 1.0
    if max_val < 1e-9:
        max_val = 1.0
    return (log_arr / max_val).astype(np.float32), max_val


# ---------------------------------------------------------------------------
# Meta dataclass — stores normalisation stats so inference can reuse them
# ---------------------------------------------------------------------------

@dataclass
class NodeFeatureMeta:
    """Normalisation parameters computed during graph construction.

    Pass this object to the same feature functions at inference time with
    fit=False to apply the training-set statistics to new nodes.
    """
    lat_range: Tuple[float, float] = (0.0, 1.0)
    lon_range: Tuple[float, float] = (0.0, 1.0)

    # junction
    degree_range: Tuple[float, float] = (0.0, 10.0)

    # cafe
    reviews_max_log: float = 1.0
    weekly_range: Tuple[float, float] = (0.0, DEFAULT_WEEKLY_HOURS)
    poi_composite_range: Tuple[float, float] = (0.0, 1.0)
    cafe_snap_range: Tuple[float, float] = (0.0, 120.0)

    # poi
    poi_reviews_max_log: float = 1.0
    poi_snap_range: Tuple[float, float] = (0.0, 120.0)

    # feature dimensions (set after build)
    junction_dim: int = 4
    cafe_dim: int = 13
    poi_dim: int = 11


# ---------------------------------------------------------------------------
# Junction features
# ---------------------------------------------------------------------------

def junction_features(
    graph,                          # nx.MultiDiGraph from OSMnx
    node_ids: Sequence[int],
    meta: NodeFeatureMeta,
    fit: bool = True,
) -> np.ndarray:
    """Return float32 array of shape (N_junctions, junction_dim).

    Features: [lat_norm, lon_norm, degree_norm, street_count_norm]
    """
    lats = np.array([graph.nodes[n].get("y", 0.0) for n in node_ids], dtype=np.float64)
    lons = np.array([graph.nodes[n].get("x", 0.0) for n in node_ids], dtype=np.float64)
    degrees = np.array([graph.degree(n) for n in node_ids], dtype=np.float64)
    street_counts = np.array(
        [graph.nodes[n].get("street_count", graph.degree(n)) for n in node_ids],
        dtype=np.float64,
    )

    if fit:
        meta.lat_range = (float(lats.min()), float(lats.max()))
        meta.lon_range = (float(lons.min()), float(lons.max()))
        meta.degree_range = (0.0, float(degrees.max()) if degrees.size > 0 else 10.0)

    lat_norm = _minmax(lats, *meta.lat_range)
    lon_norm = _minmax(lons, *meta.lon_range)
    deg_norm = _minmax(degrees, *meta.degree_range)
    sc_norm = _minmax(street_counts, *meta.degree_range)  # same scale as degree

    x = np.stack([lat_norm, lon_norm, deg_norm, sc_norm], axis=1)
    meta.junction_dim = x.shape[1]
    return x


# ---------------------------------------------------------------------------
# Cafe features
# ---------------------------------------------------------------------------

def cafe_features(
    cafe_df: pd.DataFrame,
    snap_distances_m: np.ndarray,   # shape (N_cafes,) — from snap_point / snap_to_edge
    meta: NodeFeatureMeta,
    fit: bool = True,
) -> np.ndarray:
    """Return float32 array of shape (N_cafes, cafe_dim).

    Features:
      lat_norm, lon_norm,
      reviews_norm, weekly_hours_norm, rating_norm,
      snap_dist_norm,
      banks_count_norm, education_count_norm, health_count_norm,
      temples_count_norm, other_count_norm,
      poi_composite_norm, cafe_weight
    """
    df = cafe_df.reset_index(drop=True)

    # Coordinates
    lats = pd.to_numeric(df.get("lat", df.get("location_lat", 0)), errors="coerce").fillna(0).to_numpy(np.float64)
    lons = pd.to_numeric(df.get("lng", df.get("loc_lng", df.get("lon", 0))), errors="coerce").fillna(0).to_numpy(np.float64)

    if fit:
        meta.lat_range = (float(lats.min()), float(lats.max()))
        meta.lon_range = (float(lons.min()), float(lons.max()))

    lat_norm = _minmax(lats, *meta.lat_range)
    lon_norm = _minmax(lons, *meta.lon_range)

    # Reviews (log-normalised)
    reviews_raw = pd.to_numeric(
        df.get("reviews_count", df.get("reviewsCount", 0)), errors="coerce"
    ).fillna(0).to_numpy(np.float64)
    if fit:
        reviews_norm, meta.reviews_max_log = _log1p_norm(reviews_raw)
    else:
        reviews_norm = (np.log1p(reviews_raw) / meta.reviews_max_log).clip(0, 1).astype(np.float32)

    # Weekly hours (capped at DEFAULT_WEEKLY_HOURS)
    weekly_raw = pd.to_numeric(df.get("weekly_hours", DEFAULT_WEEKLY_HOURS), errors="coerce").fillna(DEFAULT_WEEKLY_HOURS)
    weekly_raw = weekly_raw.replace(0, DEFAULT_WEEKLY_HOURS).to_numpy(np.float64)
    weekly_norm = np.clip(weekly_raw / DEFAULT_WEEKLY_HOURS, 0.0, 1.0).astype(np.float32)

    # Rating (0–5 → 0–1)
    rating_raw = pd.to_numeric(df.get("rating", df.get("totalScore", 0)), errors="coerce").fillna(0).to_numpy(np.float64)
    rating_norm = np.clip(rating_raw / MAX_RATING, 0.0, 1.0).astype(np.float32)

    # Snap distance
    snap_m = np.asarray(snap_distances_m, dtype=np.float64)
    if fit:
        meta.cafe_snap_range = (0.0, float(np.nanmax(snap_m)) if snap_m.size > 0 else 120.0)
    snap_norm = _minmax(np.nan_to_num(snap_m, nan=meta.cafe_snap_range[1]), *meta.cafe_snap_range)

    # POI counts (from master metrics if present, else zeros)
    def _get_count(col: str) -> np.ndarray:
        # master uses _1km suffix; also accept _1_5km
        for suffix in ("_count_1km", "_count_1_5km", "_count_2km"):
            key = f"{col}{suffix}"
            if key in df.columns:
                return pd.to_numeric(df[key], errors="coerce").fillna(0).to_numpy(np.float64)
        return np.zeros(len(df), dtype=np.float64)

    count_arrs = {cat: _get_count(cat) for cat in POI_CATEGORIES}
    max_counts = {cat: float(a.max()) if a.max() > 0 else 1.0 for cat, a in count_arrs.items()}
    count_norms = [np.clip(count_arrs[cat] / max_counts[cat], 0, 1).astype(np.float32) for cat in POI_CATEGORIES]

    # poi_composite_score (pre-computed in master metrics)
    composite_raw = pd.to_numeric(df.get("poi_composite_score", 0), errors="coerce").fillna(0).to_numpy(np.float64)
    if fit:
        c_max = float(composite_raw.max()) if composite_raw.max() > 0 else 1.0
        meta.poi_composite_range = (0.0, c_max)
    composite_norm = _minmax(composite_raw, *meta.poi_composite_range)

    # cafe_weight (already 0–1 from master)
    cafe_w = pd.to_numeric(df.get("cafe_weight", 0), errors="coerce").fillna(0).clip(0, 1).to_numpy(np.float32)

    x = np.stack(
        [lat_norm, lon_norm, reviews_norm, weekly_norm, rating_norm,
         snap_norm, *count_norms, composite_norm, cafe_w],
        axis=1,
    )
    meta.cafe_dim = x.shape[1]
    return x


# ---------------------------------------------------------------------------
# POI features
# ---------------------------------------------------------------------------

def poi_features(
    poi_df: pd.DataFrame,
    category_labels: np.ndarray,    # integer index into POI_CATEGORIES, shape (N_pois,)
    snap_distances_m: np.ndarray,   # shape (N_pois,)
    subcategory_weights: np.ndarray, # shape (N_pois,) — from compute_weights_and_annotate
    meta: NodeFeatureMeta,
    fit: bool = True,
) -> np.ndarray:
    """Return float32 array of shape (N_pois, poi_dim).

    Features:
      lat_norm, lon_norm,
      rating_norm, reviews_norm,
      subcategory_weight,
      snap_dist_norm,
      <category one-hot: 5 dims>
    """
    df = poi_df.reset_index(drop=True)

    lats = pd.to_numeric(df.get("lat", df.get("location_lat", 0)), errors="coerce").fillna(0).to_numpy(np.float64)
    lons = pd.to_numeric(df.get("lng", df.get("loc_lng", df.get("lon", 0))), errors="coerce").fillna(0).to_numpy(np.float64)

    if fit:
        # Update lat/lon range using POI coordinates too (called after junction_features)
        lat_lo = min(meta.lat_range[0], float(lats.min()))
        lat_hi = max(meta.lat_range[1], float(lats.max()))
        lon_lo = min(meta.lon_range[0], float(lons.min()))
        lon_hi = max(meta.lon_range[1], float(lons.max()))
        meta.lat_range = (lat_lo, lat_hi)
        meta.lon_range = (lon_lo, lon_hi)

    lat_norm = _minmax(lats, *meta.lat_range)
    lon_norm = _minmax(lons, *meta.lon_range)

    rating_raw = pd.to_numeric(df.get("rating", df.get("totalScore", 0)), errors="coerce").fillna(0).to_numpy(np.float64)
    rating_norm = np.clip(rating_raw / MAX_RATING, 0.0, 1.0).astype(np.float32)

    reviews_raw = pd.to_numeric(
        df.get("reviewsCount", df.get("reviews_count", 0)), errors="coerce"
    ).fillna(0).to_numpy(np.float64)
    if fit:
        reviews_norm, meta.poi_reviews_max_log = _log1p_norm(reviews_raw)
    else:
        reviews_norm = (np.log1p(reviews_raw) / meta.poi_reviews_max_log).clip(0, 1).astype(np.float32)

    subcat_w = np.asarray(subcategory_weights, dtype=np.float32).clip(0, 1)

    snap_m = np.asarray(snap_distances_m, dtype=np.float64)
    if fit:
        meta.poi_snap_range = (0.0, float(np.nanmax(snap_m)) if snap_m.size > 0 else 120.0)
    snap_norm = _minmax(np.nan_to_num(snap_m, nan=meta.poi_snap_range[1]), *meta.poi_snap_range)

    # Category one-hot  (N_pois × 5)
    n_cats = len(POI_CATEGORIES)
    one_hot = np.zeros((len(df), n_cats), dtype=np.float32)
    labels = np.asarray(category_labels, dtype=np.int64)
    valid = (labels >= 0) & (labels < n_cats)
    one_hot[np.where(valid), labels[valid]] = 1.0

    x = np.stack(
        [lat_norm, lon_norm, rating_norm, reviews_norm, subcat_w, snap_norm],
        axis=1,
    )
    x = np.concatenate([x, one_hot], axis=1)
    meta.poi_dim = x.shape[1]
    return x
