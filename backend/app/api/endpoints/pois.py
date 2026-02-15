from collections import defaultdict
from functools import lru_cache
from typing import Any, Dict, List, Optional

import math
from pathlib import Path

import pandas as pd
import numpy as np
from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import StreamingResponse
import json
import networkx as nx

from app.lib.road_network import RoadNetwork

router = APIRouter(prefix="/pois")

DATA_ROOT = Path(__file__).resolve().parents[3]
ROAD_GEOJSON = DATA_ROOT / "Data" / "Roadway.geojson"
ROAD_CACHE = ROAD_GEOJSON.with_suffix(".graph.pkl")
ROAD_SNAP_TOLERANCE_M = 120.0
SECONDARY_SNAP_TOLERANCE_M = 300.0


def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0  # Earth radius in km
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def _haversine_vec_km(center_lat: float, center_lon: float, lats: np.ndarray, lons: np.ndarray) -> np.ndarray:
    r = 6371.0
    phi1 = math.radians(center_lat)
    phi2 = np.radians(lats)
    dphi = phi2 - phi1
    dlambda = np.radians(lons - center_lon)
    a = np.sin(dphi / 2.0) ** 2 + np.cos(phi1) * np.cos(phi2) * np.sin(dlambda / 2.0) ** 2
    c = 2.0 * np.arctan2(np.sqrt(a), np.sqrt(1.0 - a))
    return r * c


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
    # If center failed to snap at default tolerance, retry with a larger
    # tolerance and finally with a nearest-node fallback so we can still
    # compute paths where possible.
    if center_node is None:
        center_node, center_offset = road_net.snap_point(
            center_lat, center_lon, max_snap_m=SECONDARY_SNAP_TOLERANCE_M
        )
    if center_node is None:
        center_node, center_offset = road_net.snap_point(
            center_lat, center_lon, max_snap_m=float("inf")
        )
        if center_node is not None:
            print("Info: using nearest-node fallback for center snapping to improve coverage")
    if center_node is None:
        return {}
    # coerce NaN/inf values to None so RoadNetwork.snap_points skips them
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

    poi_nodes, poi_offsets = road_net.snap_points(
        safe_lats,
        safe_lons,
        max_snap_m=ROAD_SNAP_TOLERANCE_M,
    )
    # If some POIs failed to snap, retry with a larger tolerance to increase coverage.
    # We run a secondary snap for all points and only replace the failed entries so
    # that any already-good snaps are preserved.
    if any(n is None or not math.isfinite(o) for n, o in zip(poi_nodes, poi_offsets)):
        sec_nodes, sec_offsets = road_net.snap_points(
            safe_lats,
            safe_lons,
            max_snap_m=SECONDARY_SNAP_TOLERANCE_M,
        )
        for i, (n, o) in enumerate(zip(poi_nodes, poi_offsets)):
            if (n is None or not math.isfinite(o)) and (sec_nodes[i] is not None and math.isfinite(sec_offsets[i])):
                poi_nodes[i] = sec_nodes[i]
                poi_offsets[i] = sec_offsets[i]
    node_to_indices: Dict[int, List[int]] = defaultdict(list)
    for idx, node_id in enumerate(poi_nodes):
        if node_id is not None and math.isfinite(poi_offsets[idx]):
            node_to_indices[int(node_id)].append(idx)
    # If still no valid snaps for some points, force a nearest-node fallback
    # for remaining failed indices by snapping again with infinite tolerance.
    if any(n is None or not math.isfinite(o) for n, o in zip(poi_nodes, poi_offsets)):
        inf_nodes, inf_offsets = road_net.snap_points(
            safe_lats, safe_lons, max_snap_m=float("inf")
        )
        for i, (n, o) in enumerate(zip(poi_nodes, poi_offsets)):
            if (n is None or not math.isfinite(o)) and (inf_nodes[i] is not None and math.isfinite(inf_offsets[i])):
                poi_nodes[i] = inf_nodes[i]
                poi_offsets[i] = inf_offsets[i]
        # rebuild node_to_indices from potentially-updated poi_nodes/poi_offsets
        node_to_indices = defaultdict(list)
        for idx, node_id in enumerate(poi_nodes):
            if node_id is not None and math.isfinite(poi_offsets[idx]):
                node_to_indices[int(node_id)].append(idx)
        if node_to_indices:
            print("Info: using nearest-node fallback for POI snapping to improve coverage")
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


def _network_path_map(
    road_net: RoadNetwork,
    center_lat: float,
    center_lon: float,
    poi_lats: pd.Series,
    poi_lons: pd.Series,
    radius_m: float,
) -> Dict[int, List[Dict[str, float]]]:
    """Return mapping of poi index -> path coordinate list (lat/lon) from center to POI.

    Paths include the provided center coordinate as the first point and the POI's
    original coordinate as the last point. If a path cannot be determined or the
    POI is outside the radius, it will not be present in the returned dict.
    """
    center_node, center_offset = road_net.snap_point(
        center_lat,
        center_lon,
        max_snap_m=ROAD_SNAP_TOLERANCE_M,
    )
    # If center failed to snap at default tolerance, retry with larger
    # tolerances and finally use nearest-node fallback.
    if center_node is None:
        center_node, center_offset = road_net.snap_point(
            center_lat, center_lon, max_snap_m=SECONDARY_SNAP_TOLERANCE_M
        )
    if center_node is None:
        center_node, center_offset = road_net.snap_point(
            center_lat, center_lon, max_snap_m=float("inf")
        )
        if center_node is not None:
            print("Info: using nearest-node fallback for center snapping to improve coverage")
    if center_node is None:
        return {}
    # coerce NaN/inf values to None so RoadNetwork.snap_points skips them
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

    poi_nodes, poi_offsets = road_net.snap_points(
        safe_lats,
        safe_lons,
        max_snap_m=ROAD_SNAP_TOLERANCE_M,
    )
    # If some POIs failed to snap, retry with a larger tolerance and only
    # replace the failed entries so previously good snaps remain.
    if any(n is None or not math.isfinite(o) for n, o in zip(poi_nodes, poi_offsets)):
        sec_nodes, sec_offsets = road_net.snap_points(
            safe_lats,
            safe_lons,
            max_snap_m=SECONDARY_SNAP_TOLERANCE_M,
        )
        for i, (n, o) in enumerate(zip(poi_nodes, poi_offsets)):
            if (n is None or not math.isfinite(o)) and (sec_nodes[i] is not None and math.isfinite(sec_offsets[i])):
                poi_nodes[i] = sec_nodes[i]
                poi_offsets[i] = sec_offsets[i]
    node_to_indices: Dict[int, List[int]] = defaultdict(list)
    for idx, node_id in enumerate(poi_nodes):
        if node_id is not None and math.isfinite(poi_offsets[idx]):
            node_to_indices[int(node_id)].append(idx)
    # If some points still failed to snap, use an infinite tolerance nearest-node
    # fallback for those remaining so we can build paths for as many POIs as
    # possible.
    if any(n is None or not math.isfinite(o) for n, o in zip(poi_nodes, poi_offsets)):
        inf_nodes, inf_offsets = road_net.snap_points(
            safe_lats, safe_lons, max_snap_m=float("inf")
        )
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
    # Build a path for every snapped POI node (no cutoff). This ensures that
    # any POI which was snapped to the graph receives a path following the
    # roadway geometry. We still catch graph exceptions and skip unreachable
    # nodes, but we attempt nearest-node fallbacks above so coverage is high.
    paths: Dict[int, List[Dict[str, float]]] = {}
    for node_id, poi_indices in node_to_indices.items():
        if not poi_indices:
            continue
        for poi_idx in poi_indices:
            try:
                if center_node == node_id:
                    node_path = [center_node]
                else:
                    node_path = nx.shortest_path(road_net.graph, source=center_node, target=node_id, weight="weight")
            except (nx.NetworkXNoPath, nx.NodeNotFound):
                # skip this POI if no path exists in the graph
                continue
            coords = []
            # include original center coordinate as first
            coords.append({"lat": float(center_lat), "lon": float(center_lon)})
            for n in node_path:
                lat_val, lon_val = road_net.node_coords[int(n)]
                coords.append({"lat": float(lat_val), "lon": float(lon_val)})
            # include original poi coordinate as final point
            try:
                plat = float(poi_lats.iloc[poi_idx])
                plon = float(poi_lons.iloc[poi_idx])
                coords.append({"lat": plat, "lon": plon})
            except Exception:
                pass
            # Ensure we return at least three coordinates (center, at least one
            # node coordinate, poi). If node_path contained only center_node,
            # the above still appends that node's coords so we produce three
            # points rather than a bare two-point direct line.
            if len(coords) >= 3:
                paths[poi_idx] = coords
            else:
                # as a last resort, include the node coords even if duplicates
                # to guarantee a path structure.
                paths[poi_idx] = coords
    return paths


def get_pois_with_paths(
    lat: float,
    lon: float,
    radius_km: float = 0.3,
    decay_scale_km: Optional[float] = None,
) -> Dict[str, Any]:
    """Programmatic helper used by scripts/tests: return mapping of categories->items including path geometry.

    This mirrors the behavior of the / API route but is callable directly from Python code.
    """
    # locate project CSV folder relative to this file
    data_dir = Path(__file__).resolve().parents[3] / "Data" / "CSV"
    if not data_dir.exists():
        alt = Path(__file__).resolve().parents[3] / "Data" / "CSV_Reference" / "final"
        if alt.exists():
            data_dir = alt
        else:
            raise RuntimeError(f"Data folder not found at {data_dir} or {alt}")

    road_network = _get_road_network()
    radius_m = float(radius_km) * 1000.0
    effective_decay_km = radius_km if decay_scale_km is None else float(decay_scale_km)

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
        lat_col = None
        lon_col = None
        for c in df.columns:
            cl = c.lower()
            if cl in ("lat", "latitude", "y"):
                lat_col = c
            if cl in ("lon", "lng", "longitude", "x"):
                lon_col = c
        if lat_col is None or lon_col is None:
            continue

        df[lat_col] = pd.to_numeric(df[lat_col], errors="coerce")
        df[lon_col] = pd.to_numeric(df[lon_col], errors="coerce")

        lat_arr = df[lat_col].to_numpy(dtype=np.float64, copy=False)
        lon_arr = df[lon_col].to_numpy(dtype=np.float64, copy=False)
        valid_mask = np.isfinite(lat_arr) & np.isfinite(lon_arr)
        if not np.any(valid_mask):
            continue
        valid_idx = np.nonzero(valid_mask)[0]
        dists_km = _haversine_vec_km(lat, lon, lat_arr[valid_mask], lon_arr[valid_mask])
        within_mask = dists_km <= radius_km
        if not np.any(within_mask):
            continue
        candidate_idx = valid_idx[within_mask]
        candidate_dists = dists_km[within_mask]
        subset = df.iloc[candidate_idx].copy()
        orig_idx = subset.index.to_numpy()
        subset = subset.reset_index(drop=True)

        network_dist_map: Dict[int, float] = {}
        paths_map: Dict[int, List[Dict[str, float]]] = {}
        if road_network is not None:
            try:
                network_dist_map = _network_distance_map(
                    road_network, lat, lon, subset[lat_col], subset[lon_col], radius_m
                )
                paths_map = _network_path_map(
                    road_network, lat, lon, subset[lat_col], subset[lon_col], radius_m
                )
            except Exception:
                network_dist_map = {}

        items = []
        for pos, row in subset.iterrows():
            _ = orig_idx[pos]
            try:
                rlat = float(row[lat_col])
                rlon = float(row[lon_col])
            except Exception:
                continue
            if not math.isfinite(rlat) or not math.isfinite(rlon):
                continue
            d = network_dist_map.get(pos)
            if d is None:
                d = float(candidate_dists[pos])
            if d <= radius_km:
                name = None
                for name_key in ("name", "Name", "NAME"):
                    if name_key in row:
                        name = row[name_key]
                        break
                try:
                    base_weight = max(0.0, 1.0 - (d / radius_km))
                except Exception:
                    base_weight = 0.0
                try:
                    weight_val = base_weight * math.exp(-float(d) / float(effective_decay_km))
                except Exception:
                    weight_val = base_weight
                item: Dict[str, Any] = {"name": name, "lat": rlat, "lon": rlon, "distance_km": round(d, 4), "weight": round(weight_val, 4)}
                path = paths_map.get(pos)
                if path:
                    item["path"] = path
                items.append(item)
        if items:
            results[typ] = items
    return results


@router.get("/")
def get_pois(
    lat: float = Query(..., description="Latitude of center"),
    lon: float = Query(..., description="Longitude of center"),
    radius_km: float = Query(0.3, gt=0, description="Search radius in kilometers (default 0.3 km). Use smaller radius for denser areas"),
    decay_scale_km: Optional[float] = Query(None, gt=0, description="Exponential decay scale in kilometers for distance weighting (defaults to radius_km)"),
    stream: bool = Query(False, description="If true, return a streaming (chunked) JSON response with categories as they become available"),
) -> Any:
    # locate project CSV folder relative to this file
    data_dir = Path(__file__).resolve().parents[3] / "Data" / "CSV"
    # fallback to CSV_Reference if CSV doesn't exist (some repos use that)
    if not data_dir.exists():
        alt = Path(__file__).resolve().parents[3] / "Data" / "CSV_Reference" / "final"
        if alt.exists():
            data_dir = alt
        else:
            raise HTTPException(status_code=500, detail=f"Data folder not found at {data_dir} or {alt}")

    road_network = _get_road_network()
    radius_m = radius_km * 1000.0
    effective_decay_km = radius_km if decay_scale_km is None else float(decay_scale_km)

    poi_files = {
        "cafes": "cafes.csv",
        "banks": "banks.csv",
        "education": "education.csv",
        "health": "health.csv",
        "temples": "temples.csv",
        "other": "other.csv",
    }

    def process_one_category(typ: str, fname: str):
        fpath = data_dir / fname
        if not fpath.exists():
            base = fname[:-4].lower()
            alt_file = None
            for p in data_dir.glob("*.csv"):
                pn = p.name.lower()
                if base in pn or (base.endswith("s") and base[:-1] in pn) or (base.endswith("es") and base[:-2] in pn):
                    alt_file = p
                    break
            if alt_file is None:
                return typ, []
            fpath = alt_file
        df = pd.read_csv(fpath).reset_index(drop=True)

        lat_col = None
        lon_col = None
        for c in df.columns:
            cl = c.lower()
            if cl in ("lat", "latitude", "y"):
                lat_col = c
            if cl in ("lon", "lng", "longitude", "x"):
                lon_col = c
        if lat_col is None or lon_col is None:
            num_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
            if len(num_cols) >= 2:
                lat_col, lon_col = num_cols[0], num_cols[1]
            else:
                return typ, []

        df[lat_col] = pd.to_numeric(df[lat_col], errors="coerce")
        df[lon_col] = pd.to_numeric(df[lon_col], errors="coerce")

        lat_arr = df[lat_col].to_numpy(dtype=np.float64, copy=False)
        lon_arr = df[lon_col].to_numpy(dtype=np.float64, copy=False)
        valid_mask = np.isfinite(lat_arr) & np.isfinite(lon_arr)
        if not np.any(valid_mask):
            return typ, []
        valid_idx = np.nonzero(valid_mask)[0]
        dists_km = _haversine_vec_km(lat, lon, lat_arr[valid_mask], lon_arr[valid_mask])
        within_mask = dists_km <= radius_km
        if not np.any(within_mask):
            return typ, []
        candidate_idx = valid_idx[within_mask]
        candidate_dists = dists_km[within_mask]
        subset = df.iloc[candidate_idx].copy()
        orig_idx = subset.index.to_numpy()
        subset = subset.reset_index(drop=True)

        network_dist_map: Dict[int, float] = {}
        paths_map: Dict[int, List[Dict[str, float]]] = {}
        if road_network is not None:
            try:
                network_dist_map = _network_distance_map(
                    road_network, lat, lon, subset[lat_col], subset[lon_col], radius_m
                )
                paths_map = _network_path_map(
                    road_network, lat, lon, subset[lat_col], subset[lon_col], radius_m
                )
            except Exception as exc:
                print(f"Warning: road distance calculation failed for {typ}: {exc}")
                network_dist_map = {}

        items = []
        for pos, row in subset.iterrows():
            _ = orig_idx[pos]
            try:
                rlat = float(row[lat_col])
                rlon = float(row[lon_col])
            except Exception:
                continue
            if not math.isfinite(rlat) or not math.isfinite(rlon):
                continue
            d = network_dist_map.get(pos)
            if d is None:
                d = float(candidate_dists[pos])
            if d <= radius_km:
                name = None
                for name_key in ("name", "Name", "NAME"):
                    if name_key in row:
                        name = row[name_key]
                        break
                item: Dict[str, Any] = {"name": name, "lat": rlat, "lon": rlon, "distance_km": round(d, 4)}
                try:
                    # base linear weight (keeps compatibility)
                    base_weight = max(0.0, 1.0 - (d / radius_km))
                except Exception:
                    base_weight = 0.0
                try:
                    # apply exponential decay based on distance (km)
                    decayed = base_weight * math.exp(-float(d) / float(effective_decay_km))
                    weight_val = decayed
                except Exception:
                    weight_val = base_weight
                item["weight"] = round(weight_val, 4)
                path = paths_map.get(pos)
                if path:
                    item["path"] = path
                items.append(item)
        # ensure we always return a tuple (category, items)
        return typ, items
    # determine streaming flag
    is_stream = isinstance(stream, bool) and stream
    if is_stream:
        def iter_response_ndjson():
            for typ, fname in poi_files.items():
                cat, items = process_one_category(typ, fname)
                if not items:
                    continue
                obj = {"category": cat, "items": items}
                yield (json.dumps(obj, default=str) + "\n").encode()

        return StreamingResponse(iter_response_ndjson(), media_type='application/x-ndjson')

    # Non-streaming (original) behavior: compute all categories and return
    results: Dict[str, Any] = {}
    for typ, fname in poi_files.items():
        cat, items = process_one_category(typ, fname)
        if items:
            results[typ] = items

    return {"center": {"lat": lat, "lon": lon}, "radius_km": radius_km, "pois": results}


@router.get("/detailed")
def get_pois_detailed(
    lat: float = Query(..., description="Latitude of center"),
    lon: float = Query(..., description="Longitude of center"),
    radius_km: float = Query(0.3, gt=0, description="Search radius in kilometers (default 0.3 km)."),
    decay_scale_km: Optional[float] = Query(None, gt=0, description="Exponential decay scale in kilometers for distance weighting (defaults to radius_km)"),
) -> Any:
    try:
        pois = get_pois_with_paths(lat=lat, lon=lon, radius_km=radius_km, decay_scale_km=decay_scale_km)
        return {"center": {"lat": lat, "lon": lon}, "radius_km": radius_km, "pois": pois}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))