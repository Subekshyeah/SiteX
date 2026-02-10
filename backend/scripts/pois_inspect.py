#!/usr/bin/env python3
"""Inspect POIs around a point and report haversine and roadway distances and weights.

Usage:
    python backend/scripts/pois_inspect.py --lat 27.6742856 --lon 85.4327744 --radius-km 1.0 --decay-scale-km 1.0

Outputs JSON to stdout with one entry per POI category and per-POI metrics.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd

_BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(_BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(_BACKEND_ROOT))

try:
    from app.lib.road_network import RoadNetwork
except Exception:
    RoadNetwork = None  # type: ignore


ROAD_SNAP_TOLERANCE_M = 120.0
SECONDARY_SNAP_TOLERANCE_M = 300.0


def haversine_km(aLat: float, aLon: float, bLat: float, bLon: float) -> float:
    R = 6371.0
    phi1 = math.radians(aLat)
    phi2 = math.radians(bLat)
    dphi = math.radians(bLat - aLat)
    dlambda = math.radians(bLon - aLon)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def resolve_data_dir() -> Path:
    # Prefer backend/Data/CSV, fallback to CSV_Reference/final
    base = Path(__file__).resolve().parents[1] / "Data"
    cand = base / "CSV"
    if cand.exists():
        return cand
    alt = base / "CSV_Reference" / "final"
    if alt.exists():
        return alt
    # try parent or sibling locations
    for p in [Path.cwd(), Path.cwd() / "backend"]:
        c = p / "Data" / "CSV"
        if c.exists():
            return c
    raise FileNotFoundError("Could not locate Data/CSV or Data/CSV_Reference/final folder")


def compute_road_distances(
    road_network: RoadNetwork,
    center_lat: float,
    center_lon: float,
    poi_lats: List[Optional[float]],
    poi_lons: List[Optional[float]],
    radius_m: float,
) -> Dict[int, float]:
    # mirrors the POIs endpoint behavior: snap and compute shortest paths
    center_node, center_offset = road_network.snap_point(center_lat, center_lon, max_snap_m=ROAD_SNAP_TOLERANCE_M)
    if center_node is None:
        center_node, center_offset = road_network.snap_point(center_lat, center_lon, max_snap_m=SECONDARY_SNAP_TOLERANCE_M)
    if center_node is None:
        center_node, center_offset = road_network.snap_point(center_lat, center_lon, max_snap_m=float("inf"))
        if center_node is not None:
            print("Info: using nearest-node fallback for center snapping to improve coverage")
    if center_node is None:
        return {}

    safe_lats: List[Optional[float]] = []
    safe_lons: List[Optional[float]] = []
    for a, b in zip(poi_lats, poi_lons):
        try:
            av = float(a)
            bv = float(b)
            if not math.isfinite(av) or not math.isfinite(bv):
                safe_lats.append(None)
                safe_lons.append(None)
            else:
                safe_lats.append(av)
                safe_lons.append(bv)
        except Exception:
            safe_lats.append(None)
            safe_lons.append(None)

    poi_nodes, poi_offsets = road_network.snap_points(safe_lats, safe_lons, max_snap_m=ROAD_SNAP_TOLERANCE_M)
    if any(n is None or not math.isfinite(o) for n, o in zip(poi_nodes, poi_offsets)):
        sec_nodes, sec_offsets = road_network.snap_points(safe_lats, safe_lons, max_snap_m=SECONDARY_SNAP_TOLERANCE_M)
        for i, (n, o) in enumerate(zip(poi_nodes, poi_offsets)):
            if (n is None or not math.isfinite(o)) and (sec_nodes[i] is not None and math.isfinite(sec_offsets[i])):
                poi_nodes[i] = sec_nodes[i]
                poi_offsets[i] = sec_offsets[i]

    node_to_indices: Dict[int, List[int]] = defaultdict(list)
    for idx, node_id in enumerate(poi_nodes):
        if node_id is not None and math.isfinite(poi_offsets[idx]):
            node_to_indices[int(node_id)].append(idx)

    if any(n is None or not math.isfinite(o) for n, o in zip(poi_nodes, poi_offsets)):
        inf_nodes, inf_offsets = road_network.snap_points(safe_lats, safe_lons, max_snap_m=float("inf"))
        for i, (n, o) in enumerate(zip(poi_nodes, poi_offsets)):
            if (n is None or not math.isfinite(o)) and (inf_nodes[i] is not None and math.isfinite(inf_offsets[i])):
                poi_nodes[i] = inf_nodes[i]
                poi_offsets[i] = inf_offsets[i]
        node_to_indices = defaultdict(list)
        for idx, node_id in enumerate(poi_nodes):
            if node_id is not None and math.isfinite(poi_offsets[idx]):
                node_to_indices[int(node_id)].append(idx)
        if node_to_indices:
            print("Info: using nearest-node fallback for POI snapping to improve coverage")

    if not node_to_indices:
        return {}

    lengths = road_network.shortest_paths_from(center_node, cutoff=radius_m)
    if not lengths:
        return {}
    center_offset_val = float(center_offset or 0.0)
    results: Dict[int, float] = {}
    for node_id, path_dist in lengths.items():
        poi_indices = node_to_indices.get(node_id)
        if not poi_indices:
            continue
        for poi_idx in poi_indices:
            total_m = path_dist + center_offset_val + poi_offsets[poi_idx]
            if total_m <= radius_m:
                results[poi_idx] = total_m / 1000.0
    return results


def road_distance_km_with_fallback(
    road_network: RoadNetwork,
    center_lat: float,
    center_lon: float,
    poi_lat: float,
    poi_lon: float,
) -> Optional[float]:
    for snap_m in (ROAD_SNAP_TOLERANCE_M, SECONDARY_SNAP_TOLERANCE_M, float("inf")):
        dist_m = road_network.distance_between(center_lat, center_lon, poi_lat, poi_lon, max_snap_m=snap_m)
        if dist_m is not None and math.isfinite(dist_m):
            return float(dist_m) / 1000.0
    return None


def main(argv: Optional[List[str]] = None) -> None:
    parser = argparse.ArgumentParser(description="Inspect POIs and compute haversine and roadway distances and weights")
    parser.add_argument("--lat", type=float, required=True)
    parser.add_argument("--lon", type=float, required=True)
    parser.add_argument("--radius-km", type=float, default=0.3)
    parser.add_argument("--decay-scale-km", type=float, default=1.0)
    parser.add_argument("--road-geojson", type=str, default=None, help="Optional Roadway.geojson path")
    parser.add_argument("--output-csv", type=str, default=None, help="Optional path to save results as a CSV file.")
    # When argv is None, let argparse read from sys.argv (the real CLI).
    args = parser.parse_args(None if argv is None else argv)

    data_dir = resolve_data_dir()
    poi_files = [p for p in data_dir.glob("*.csv")]
    # prefer canonical names if present
    preferred = ["cafe_final.csv", "banks_final.csv", "education_final.csv", "health_final.csv", "temples_final.csv", "other_final.csv"]
    files_map: Dict[str, Path] = {}
    for name in preferred:
        p = data_dir / name
        if p.exists():
            files_map[name[:-4]] = p
    # include any extra csvs not in preferred
    for p in poi_files:
        key = p.stem
        if key not in files_map:
            files_map[key] = p

    # prepare road network if requested and available
    road_network = None
    road_geojson = None
    if args.road_geojson:
        road_geojson = Path(args.road_geojson)
    else:
        # look relative to backend/Data/Roadway.geojson
        cand = Path(__file__).resolve().parents[1] / "Data" / "Roadway.geojson"
        if cand.exists():
            road_geojson = cand
    if road_geojson and RoadNetwork is not None:
        cache_path = road_geojson.with_suffix(".graph.pkl")
        try:
            road_network = RoadNetwork.from_geojson(road_geojson, cache_path=cache_path, snap_tolerance_m=ROAD_SNAP_TOLERANCE_M)
        except Exception as exc:
            print(f"Warning: failed to load road network cache ({exc}); rebuilding from GeoJSON")
            try:
                road_network = RoadNetwork.from_geojson(road_geojson, cache_path=None, snap_tolerance_m=ROAD_SNAP_TOLERANCE_M)
            except Exception as exc2:
                print(f"Warning: failed to build road network ({exc2}); continuing without it")
                road_network = None
        if road_network is not None and road_network.node_count > 0:
            print(f"Loaded road network: {road_network.node_count} nodes / {road_network.edge_count} edges")
        elif road_network is not None:
            print("Warning: road network is empty; continuing without it")
            road_network = None

    out: Dict[str, Any] = {"center": {"lat": args.lat, "lon": args.lon}, "radius_km": args.radius_km, "decay_scale_km": args.decay_scale_km, "categories": {}}
    all_pois: List[Dict[str, Any]] = []

    for cat, ppath in files_map.items():
        try:
            df = pd.read_csv(ppath).reset_index(drop=True)
        except Exception as exc:
            print(f"Skipping {ppath}: failed to read ({exc})")
            continue
        # detect lat lon columns
        lat_col = None
        lon_col = None
        for c in df.columns:
            cl = c.lower()
            if cl in ("lat", "latitude", "y"):
                lat_col = c
            if cl in ("lon", "lng", "longitude", "x"):
                lon_col = c
        if lat_col is None or lon_col is None:
            # try numeric columns fallback
            num_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
            if len(num_cols) >= 2:
                lat_col, lon_col = num_cols[0], num_cols[1]
            else:
                continue

        poi_lats = pd.to_numeric(df[lat_col], errors="coerce").to_numpy(dtype=float)
        poi_lons = pd.to_numeric(df[lon_col], errors="coerce").to_numpy(dtype=float)

        # compute haversine distances (km)
        hav_km = [float(haversine_km(args.lat, args.lon, float(a), float(b))) if (math.isfinite(a) and math.isfinite(b)) else None for a, b in zip(poi_lats, poi_lons)]

        # compute roadway distances (km) if network available
        road_km_map: Dict[int, float] = {}
        if road_network is not None:
            in_radius_indices = [
                i for i, h in enumerate(hav_km)
                if h is not None and math.isfinite(h) and h <= args.radius_km
            ]
            for idx in in_radius_indices:
                plat = float(poi_lats[idx])
                plon = float(poi_lons[idx])
                road_km = road_distance_km_with_fallback(road_network, args.lat, args.lon, plat, plon)
                if road_km is not None:
                    road_km_map[idx] = road_km

        items: List[Dict[str, Any]] = []
        for idx, row in df.iterrows():
            try:
                plat = float(poi_lats[idx])
                plon = float(poi_lons[idx])
            except Exception:
                continue
            if not math.isfinite(plat) or not math.isfinite(plon):
                continue
            name = None
            for k in ("name", "Name", "NAME"):
                if k in row:
                    name = row[k]
                    break
            h = hav_km[idx]
            base_h = None
            dec_h = None
            if h is not None and h <= args.radius_km:
                try:
                    base_h = max(0.0, 1.0 - (h / args.radius_km))
                    dec_h = base_h * math.exp(-(h / float(args.decay_scale_km)))
                except Exception:
                    base_h = base_h or 0.0
                    dec_h = base_h

            r = road_km_map.get(idx)
            base_r = None
            dec_r = None
            if r is not None and r <= args.radius_km:
                try:
                    base_r = max(0.0, 1.0 - (r / args.radius_km))
                    dec_r = base_r * math.exp(-(r / float(args.decay_scale_km)))
                except Exception:
                    base_r = base_r or 0.0
                    dec_r = base_r

            # Only include POIs that are within the radius for at least one distance metric
            if base_h is not None or base_r is not None:
                poi_data = {
                    "category": cat,
                    "name": name,
                    "lat": plat,
                    "lon": plon,
                    "haversine_km": h,
                    "road_km": r if r is not None else None,
                    "base_weight_haversine": None if base_h is None else round(base_h, 6),
                    "decayed_weight_haversine": None if dec_h is None else round(dec_h, 6),
                    "base_weight_road": None if base_r is None else round(base_r, 6),
                    "decayed_weight_road": None if dec_r is None else round(dec_r, 6),
                }
                items.append(poi_data)
                all_pois.append(poi_data)

        out["categories"][cat] = items

    if args.output_csv:
        if all_pois:
            df_out = pd.DataFrame(all_pois)
            df_out.to_csv(args.output_csv, index=False)
            print(f"Saved {len(all_pois)} POIs to {args.output_csv}")
        else:
            print("No POIs found to save.")
    else:
        # For stdout, ensure we are using utf-8
        if sys.stdout.encoding.lower() != 'utf-8':
            sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)
        print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
