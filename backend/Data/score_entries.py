"""
Flexible scoring script to assign a success score to entries.

- Configurable feature definitions (weight, type, direction)
- Normalizes numeric features (log where useful, min-max)
- Maps binary/categorical features to 0/1 via rules
- Produces a `*_scored.csv` with `success_score` (0-100) and component breakdown

Usage:
    python score_entries.py --input path/to/compact_cafe_selected.csv

Edit the CONFIG dict below to change features, weights and types.
"""

import argparse
import math
import json
from pathlib import Path

import numpy as np
import pandas as pd

# ----------------------- CONFIG (adjust to your data) -----------------------
# For each feature provide: type: 'numeric'|'binary'|'categorical',
# weight: positive number, direction: 'higher_better' or 'lower_better'
# optional: transform: 'log' for skewed counts
# For categorical provide mapping dict in 'map'
CONFIG = {
    # numeric features (higher is better unless noted)
    "rating": {"type": "numeric", "weight": 4.0, "direction": "higher_better"},
    "rating.1": {"type": "numeric", "weight": 1.0, "direction": "higher_better"},
    "reviews_count": {"type": "numeric", "weight": 2.0, "direction": "higher_better", "transform": "log1p"},

    # review distributions: more five/four stars is better; more one/two stars is worse
    "reviewsDistribution_oneStar": {"type": "numeric", "weight": 1.0, "direction": "lower_better"},
    "reviewsDistribution_twoStar": {"type": "numeric", "weight": 0.3, "direction": "lower_better"},
    "reviewsDistribution_threeStar": {"type": "numeric", "weight": 0.5, "direction": "higher_better"},
    "reviewsDistribution_fourStar": {"type": "numeric", "weight": 0.8, "direction": "higher_better"},
    "reviewsDistribution_fiveStar": {"type": "numeric", "weight": 1.2, "direction": "higher_better"},

    # service / flags
    "takeout": {"type": "binary", "weight": 0.4, "direction": "higher_better"},
    "temporarilyClosed": {"type": "binary", "weight": 2.0, "direction": "lower_better"},
    "title": {"type": "categorical", "weight": 0.0},
    "tourists": {"type": "numeric", "weight": 0.2, "direction": "higher_better", "transform": "log1p"},
    "vegetarian": {"type": "binary", "weight": 0.2, "direction": "higher_better"},
    "weekly_hours": {"type": "numeric", "weight": 0.5, "direction": "higher_better"},

    # accessibility and amenities
    "wheelchair_accessible_entrance": {"type": "binary", "weight": 0.6, "direction": "higher_better"},
    "wifi": {"type": "binary", "weight": 0.6, "direction": "higher_better"},

    # nearby POI counts / weights (log scaled where appropriate)
    "banks_count_1km": {"type": "numeric", "weight": 0.2, "direction": "higher_better", "transform": "log1p"},
    "banks_weight_1km": {"type": "numeric", "weight": 0.1, "direction": "higher_better", "transform": "log1p"},
    "banks_category_weight": {"type": "numeric", "weight": 0.1, "direction": "higher_better"},

    "education_count_1km": {"type": "numeric", "weight": 0.2, "direction": "higher_better", "transform": "log1p"},
    "education_weight_1km": {"type": "numeric", "weight": 0.1, "direction": "higher_better", "transform": "log1p"},
    "education_category_weight": {"type": "numeric", "weight": 0.1, "direction": "higher_better"},

    "health_count_1km": {"type": "numeric", "weight": 0.2, "direction": "higher_better", "transform": "log1p"},
    "health_weight_1km": {"type": "numeric", "weight": 0.1, "direction": "higher_better", "transform": "log1p"},
    "health_category_weight": {"type": "numeric", "weight": 0.1, "direction": "higher_better"},

    "temples_count_1km": {"type": "numeric", "weight": 0.1, "direction": "higher_better", "transform": "log1p"},
    "temples_weight_1km": {"type": "numeric", "weight": 0.05, "direction": "higher_better", "transform": "log1p"},
    "temples_category_weight": {"type": "numeric", "weight": 0.05, "direction": "higher_better"},

    "other_count_1km": {"type": "numeric", "weight": 0.1, "direction": "higher_better", "transform": "log1p"},
    "other_weight_1km": {"type": "numeric", "weight": 0.05, "direction": "higher_better", "transform": "log1p"},
    "other_category_weight": {"type": "numeric", "weight": 0.05, "direction": "higher_better"},

    # composite score if available
    "poi_composite_score": {"type": "numeric", "weight": 1.5, "direction": "higher_better"},
}

# ----------------------- Helper functions -----------------------

def is_truthy(val: str) -> bool:
    if pd.isna(val):
        return False
    s = str(val).strip().lower()
    if s in ("1", "true", "yes", "y", "t"): 
        return True
    return False


def numeric_transform(series: pd.Series, transform: str):
    if transform == "log1p":
        # convert to numeric safely
        s = pd.to_numeric(series, errors="coerce").fillna(0).astype(float)
        return np.log1p(s)
    # default: numeric coercion
    return pd.to_numeric(series, errors="coerce").astype(float)


def min_max_scale(arr: np.ndarray):
    arr = np.array(arr, dtype=float)
    # guard against constant arrays
    mn = np.nanmin(arr)
    mx = np.nanmax(arr)
    if math.isclose(mx, mn) or mx == mn:
        # return 1.0 where value exists, 0 elsewhere
        return np.where(np.isnan(arr), 0.0, 1.0)
    out = (arr - mn) / (mx - mn)
    # clip
    out = np.clip(out, 0.0, 1.0)
    # replace NaN with 0
    out = np.where(np.isnan(out), 0.0, out)
    return out

# ----------------------- Scoring implementation -----------------------

def score_dataframe(df: pd.DataFrame, config: dict) -> pd.DataFrame:
    df = df.copy()
    feature_scores = {}
    weights = {}

    # Preprocess columns and compute normalized component scores
    for feat, params in config.items():
        if feat not in df.columns:
            print(f"Warning: feature '{feat}' not found in CSV — skipping")
            continue
        ftype = params.get("type", "numeric")
        weight = float(params.get("weight", 1.0))
        direction = params.get("direction", "higher_better")
        transform = params.get("transform", None)

        weights[feat] = weight

        if ftype == "numeric":
            if transform:
                arr = numeric_transform(df[feat], transform)
            else:
                arr = pd.to_numeric(df[feat], errors="coerce").astype(float).values
            norm = min_max_scale(arr)
            if direction == "lower_better":
                norm = 1.0 - norm
            feature_scores[feat] = norm

        elif ftype == "binary":
            # map truthy to 1, else 0
            arr = df[feat].apply(is_truthy).astype(float).values
            # binary already in 0..1
            norm = arr
            if direction == "lower_better":
                norm = 1.0 - norm
            feature_scores[feat] = norm

        elif ftype == "categorical":
            mapping = params.get("map") or {}
            # map category -> numeric, then normalize
            mapped = df[feat].map(mapping).astype(float)
            norm = min_max_scale(mapped.values)
            if direction == "lower_better":
                norm = 1.0 - norm
            feature_scores[feat] = norm

        else:
            print(f"Unknown type '{ftype}' for feature '{feat}' — skipping")

    if not feature_scores:
        raise ValueError("No features processed — check CONFIG and CSV columns")

    # Compute weighted sum
    weight_array = np.array([weights[f] for f in feature_scores.keys()], dtype=float)
    components = np.vstack([feature_scores[f] for f in feature_scores.keys()])
    # shape = (n_features, n_rows)

    # multiply each row by weight
    weighted = (weight_array[:, None] * components)

    # sum across features
    raw_score = np.nansum(weighted, axis=0)

    # normalize by total weight to keep in comparable range
    total_weight = weight_array.sum()
    # avoid division by zero
    if total_weight <= 0:
        total_weight = 1.0
    normalized_score = raw_score / total_weight

    # scale to 0-100
    min_s = np.nanmin(normalized_score)
    max_s = np.nanmax(normalized_score)
    if math.isclose(max_s, min_s):
        final_score = np.where(np.isnan(normalized_score), 0.0, 50.0)
    else:
        final_score = 100.0 * (normalized_score - min_s) / (max_s - min_s)

    # Attach component breakdown to dataframe
    for i, feat in enumerate(feature_scores.keys()):
        df[f"score_{feat}"] = feature_scores[feat] * weights[feat]

    df["raw_score"] = raw_score
    df["success_score"] = final_score

    # Optional: rank
    df["success_rank"] = df["success_score"].rank(method="min", ascending=False)

    return df

# ----------------------- CLI and main -----------------------

def main():
    parser = argparse.ArgumentParser(description="Score entries based on configurable features")
    parser.add_argument("--input", "-i", required=True, help="Path to input CSV")
    parser.add_argument("--output", "-o", required=False, help="Path to output CSV (optional)")
    parser.add_argument("--config", "-c", required=False, help="Path to JSON config to override defaults")
    args = parser.parse_args()

    in_path = Path(args.input)
    if not in_path.exists():
        raise FileNotFoundError(f"Input file not found: {in_path}")

    out_path = Path(args.output) if args.output else in_path.with_name(in_path.stem + "_scored.csv")

    # load CSV
    print(f"Loading {in_path}")
    df = pd.read_csv(in_path, dtype=str, low_memory=False)

    # optionally override CONFIG
    config_to_use = CONFIG.copy()
    if args.config:
        cfg_path = Path(args.config)
        if not cfg_path.exists():
            raise FileNotFoundError(f"Config file not found: {cfg_path}")
        loaded = json.loads(cfg_path.read_text(encoding="utf-8"))
        # shallow update
        config_to_use.update(loaded)
        print("Loaded config overrides from", cfg_path)

    # run scoring
    scored = score_dataframe(df, config_to_use)

    # save
    print(f"Saving scored output to {out_path}")
    scored.to_csv(out_path, index=False)
    print("Done. Columns added: success_score, raw_score, success_rank and score_<feature> components")


if __name__ == "__main__":
    main()
