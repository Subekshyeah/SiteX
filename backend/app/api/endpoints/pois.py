from collections import defaultdict
from functools import lru_cache
from typing import Any, Dict, List, Optional

import math
from pathlib import Path

import pandas as pd
from fastapi import APIRouter, Query, HTTPException

from app.lib.road_network import RoadNetwork

router = APIRouter(prefix="/pois", tags=["pois"])

DATA_ROOT = Path(__file__).resolve().parents[3]
ROAD_GEOJSON = DATA_ROOT / "Data" / "Roadway.geojson"
ROAD_CACHE = ROAD_GEOJSON.with_suffix(".graph.pkl")
ROAD_SNAP_TOLERANCE_M = 120.0


def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0  # Earth radius in km
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


@lru_cache(maxsize=1)
def _get_road_network() -> Optional[RoadNetwork]:
    if not ROAD_GEOJSON.exists():
        return None
    try:
        return RoadNetwork.from_geojson(
            ROAD_GEOJSON,
            cache_path=ROAD_CACHE,
            snap_tolerance_m=ROAD_SNAP_TOLERANCE_M,
        )
    except Exception as exc:
        print(f"Warning: Failed to load road network for POI endpoint ({exc})")
        return None


def _network_distance_map(
    road_net: RoadNetwork,
    center_lat: float,
    center_lon: float,
    poi_lats: pd.Series,
    poi_lons: pd.Series,
    radius_m: float,
) -> Dict[int, float]:
    center_node, center_offset = road_net.snap_point(
        center_lat,
        center_lon,
        max_snap_m=ROAD_SNAP_TOLERANCE_M,
    )
    if center_node is None:
        return {}
    poi_nodes, poi_offsets = road_net.snap_points(
        poi_lats.to_numpy(),
        poi_lons.to_numpy(),
        max_snap_m=ROAD_SNAP_TOLERANCE_M,
    )
    node_to_indices: Dict[int, List[int]] = defaultdict(list)
    for idx, node_id in enumerate(poi_nodes):
        if node_id is not None and math.isfinite(poi_offsets[idx]):
            node_to_indices[int(node_id)].append(idx)
    if not node_to_indices:
        return {}
    lengths = road_net.shortest_paths_from(center_node, cutoff=radius_m)
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


@router.get("/")
def get_pois(
    lat: float = Query(..., description="Latitude of center"),
    lon: float = Query(..., description="Longitude of center"),
    radius_km: float = Query(1.0, gt=0, description="Search radius in kilometers"),
) -> Dict[str, Any]:
    # locate project CSV folder relative to this file
    data_dir = Path(__file__).resolve().parents[3] / "Data" / "CSV"
    if not data_dir.exists():
        raise HTTPException(status_code=500, detail=f"Data folder not found at {data_dir}")

    road_network = _get_road_network()
    radius_m = radius_km * 1000.0

    poi_files = {
        "cafes": "cafes.csv",
        "banks": "banks.csv",
        "education": "education.csv",
        "health": "health.csv",
        "temples": "temples.csv",
        "other": "other.csv",
    }

    results: Dict[str, Any] = {}
    for typ, fname in poi_files.items():
        fpath = data_dir / fname
        if not fpath.exists():
            continue
        df = pd.read_csv(fpath).reset_index(drop=True)

        # try to detect latitude/longitude columns
        lat_col = None
        lon_col = None
        for c in df.columns:
            cl = c.lower()
            if cl in ("lat", "latitude", "y"):
                lat_col = c
            if cl in ("lon", "lng", "longitude", "x"):
                lon_col = c

        if lat_col is None or lon_col is None:
            # fallback: pick first two numeric columns
            num_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
            if len(num_cols) >= 2:
                lat_col, lon_col = num_cols[0], num_cols[1]
            else:
                continue

        df[lat_col] = pd.to_numeric(df[lat_col], errors="coerce")
        df[lon_col] = pd.to_numeric(df[lon_col], errors="coerce")

        network_dist_map: Dict[int, float] = {}
        if road_network is not None:
            try:
                network_dist_map = _network_distance_map(
                    road_network,
                    lat,
                    lon,
                    df[lat_col],
                    df[lon_col],
                    radius_m,
                )
            except Exception as exc:
                print(f"Warning: road distance calculation failed for {typ}: {exc}")
                network_dist_map = {}

        items = []
        for idx, row in df.iterrows():
            try:
                rlat = float(row[lat_col])
                rlon = float(row[lon_col])
            except Exception:
                continue
            if not math.isfinite(rlat) or not math.isfinite(rlon):
                continue
            d = network_dist_map.get(idx)
            if d is None:
                d = haversine(lat, lon, rlat, rlon)
            if d <= radius_km:
                name = None
                for name_key in ("name", "Name", "NAME"):
                    if name_key in row:
                        name = row[name_key]
                        break
                items.append({"name": name, "lat": rlat, "lon": rlon, "distance_km": round(d, 4)})

        if items:
            results[typ] = sorted(items, key=lambda x: x["distance_km"])

    return {"center": {"lat": lat, "lon": lon}, "radius_km": radius_km, "pois": results}