from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List

import math

from fastapi import APIRouter, HTTPException, Query

from app.lib.road_type_network import ROAD_TYPE_WEIGHTS, RoadTypeNetwork

router = APIRouter(prefix="/road-types")

DATA_ROOT = Path(__file__).resolve().parents[3]
ROAD_GEOJSON = DATA_ROOT / "Data" / "Roadway.geojson"
ROAD_CACHE = ROAD_GEOJSON.with_suffix(".roadtypes.pkl")
ROAD_SNAP_TOLERANCE_M = 120.0
SECONDARY_SNAP_TOLERANCE_M = 300.0
DEFAULT_SNAP_WEIGHT_SHARE = 0.9


@lru_cache(maxsize=1)
def _get_road_type_network() -> RoadTypeNetwork:
    if not ROAD_GEOJSON.exists():
        raise FileNotFoundError(f"Roadway GeoJSON not found at {ROAD_GEOJSON}")
    return RoadTypeNetwork.from_geojson(
        ROAD_GEOJSON,
        cache_path=ROAD_CACHE,
        snap_tolerance_m=ROAD_SNAP_TOLERANCE_M,
    )


@router.get("/")
def get_road_types(
    lat: float = Query(..., description="Latitude of center"),
    lon: float = Query(..., description="Longitude of center"),
    radius_km: float = Query(1.0, gt=0, description="Search radius in kilometers (default 1.0 km)."),
    decay_scale_km: float = Query(0.3, gt=0, description="Exponential decay scale in kilometers for weighting (default 0.3 km)."),
) -> Any:
    try:
        road_network = _get_road_type_network()
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to load road network: {exc}")

    decay_scale_km = float(radius_km)
    radius_m = float(radius_km) * 1000.0
    result = road_network.road_type_distance_map(
        lat,
        lon,
        radius_m,
        secondary_snap_tolerance_m=SECONDARY_SNAP_TOLERANCE_M,
    )
    if result is None:
        raise HTTPException(status_code=400, detail="Unable to snap point to road network")

    start_types = result["start_types"]
    distances = result["distances"]
    points = result.get("points", {})
    reachable: List[Dict[str, Any]] = []
    total_decayed_weight = 0.0
    total_normalized_score = 0.0
    for road_type, dist_m in distances.items():
        if road_type in start_types:
            continue
        point = points.get(road_type)
        distance_km = round(float(dist_m) / 1000.0, 4)
        normalized_score = max(0.0, 1.0 - (distance_km / float(radius_km)))
        weight = ROAD_TYPE_WEIGHTS.get(road_type, 1.0)
        try:
            decayed_weight = weight * math.exp(-float(distance_km) / float(decay_scale_km))
        except Exception:
            decayed_weight = weight
        total_decayed_weight += decayed_weight
        total_normalized_score += normalized_score
        reachable.append(
            {
                "road_type": road_type,
                "distance_km": distance_km,
                "normalized_score": round(normalized_score, 6),
                "weight": weight,
                "decayed_weight": round(decayed_weight, 6),
                "point": point,
            }
        )
    reachable.sort(key=lambda item: item["distance_km"])

    return {
        "center": {"lat": lat, "lon": lon},
        "radius_km": radius_km,
        "decay_scale_km": decay_scale_km,
        "snap": {
            "node_id": result["node_id"],
            "snap_distance_m": round(result["snap_distance_m"], 2),
            "road_types": start_types,
        },
        "reachable": reachable,
        "total_decayed_weight": round(total_decayed_weight, 6),
        "total_normalized_score": round(total_normalized_score, 6),
    }


def _normalize_weight(weight: float, min_weight: float, max_weight: float) -> float:
    if max_weight <= min_weight:
        return 0.0
    return max(0.0, min(1.0, (weight - min_weight) / (max_weight - min_weight)))


@router.get("/summary-accessibility")
def get_summary_accessibility(
    lat: float = Query(..., description="Latitude of center"),
    lon: float = Query(..., description="Longitude of center"),
    radius_km: float = Query(1.0, gt=0, description="Search radius in kilometers (default 1.0 km)."),
    decay_scale_km: float = Query(0.3, gt=0, description="Exponential decay scale in kilometers for weighting (default 0.3 km)."),
    snap_weight_share: float = Query(
        DEFAULT_SNAP_WEIGHT_SHARE,
        ge=0.0,
        le=1.0,
        description="Share of the final score driven by the initial snap road type.",
    ),
) -> Any:
    try:
        road_network = _get_road_type_network()
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to load road network: {exc}")

    decay_scale_km = float(radius_km)
    radius_m = float(radius_km) * 1000.0
    result = road_network.road_type_distance_map(
        lat,
        lon,
        radius_m,
        secondary_snap_tolerance_m=SECONDARY_SNAP_TOLERANCE_M,
    )
    if result is None:
        raise HTTPException(status_code=400, detail="Unable to snap point to road network")

    start_types = result["start_types"]
    distances = result["distances"]

    weights = list(ROAD_TYPE_WEIGHTS.values())
    min_weight = min(weights) if weights else 0.0
    max_weight = max(weights) if weights else 1.0

    start_weight = 0.0
    for road_type in start_types:
        start_weight = max(start_weight, float(ROAD_TYPE_WEIGHTS.get(road_type, 1.0)))
    snap_score = _normalize_weight(start_weight, min_weight, max_weight)

    reachable_scores: List[float] = []
    for road_type, dist_m in distances.items():
        if road_type in start_types:
            continue
        distance_km = float(dist_m) / 1000.0
        normalized_score = max(0.0, 1.0 - (distance_km / float(radius_km)))
        weight = float(ROAD_TYPE_WEIGHTS.get(road_type, 1.0))
        weighted_score = _normalize_weight(weight, min_weight, max_weight) * normalized_score
        reachable_scores.append(weighted_score)

    reachable_score = (sum(reachable_scores) / len(reachable_scores)) if reachable_scores else 0.0
    snap_share = float(snap_weight_share)
    score = (snap_score * snap_share) + (reachable_score * (1.0 - snap_share))
    score_0_100 = round(max(0.0, min(100.0, score * 100.0)), 2)

    return {
        "center": {"lat": lat, "lon": lon},
        "radius_km": radius_km,
        "decay_scale_km": decay_scale_km,
        "snap": {
            "node_id": result["node_id"],
            "snap_distance_m": round(result["snap_distance_m"], 2),
            "road_types": start_types,
        },
        "score": score_0_100,
        "score_breakdown": {
            "snap_score": round(snap_score, 6),
            "reachable_score": round(reachable_score, 6),
            "snap_weight_share": snap_share,
        },
    }
