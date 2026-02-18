from typing import Any, Literal, Optional

from fastapi import APIRouter, HTTPException, Query

from app.services.prediction_service import PredictionService


router = APIRouter(prefix="/model-input")


def _parse_float_param(value: Any, name: str) -> float:
    if isinstance(value, bool):
        raise HTTPException(status_code=422, detail=f"'{name}' must be a number")
    if isinstance(value, (int, float)):
        return float(value)
    if value is None:
        raise HTTPException(status_code=422, detail=f"'{name}' must be a number")
    s = str(value).strip().replace(",", ".")
    if not s:
        raise HTTPException(status_code=422, detail=f"'{name}' must be a number")
    try:
        return float(s)
    except Exception:
        raise HTTPException(status_code=422, detail=f"'{name}' must be a number")


@router.get("/")
def model_input(
    lat: str = Query(..., description="Latitude of center", examples=["27.672782"]),
    lon: str = Query(..., description="Longitude of center", examples=["85.431941"]),
    radius_km: Optional[float] = Query(None, gt=0, description="Radius for POI metrics (km)"),
    decay_scale_km: Optional[float] = Query(None, gt=0, description="Decay scale (km) for weights"),
    include_network: bool = Query(True, description="Use road-network distances when available"),
    sort_by: Literal["auto", "haversine", "network"] = Query(
        "auto", description="Distance mode: auto prefers network when available"
    ),
    include_road_metrics: bool = Query(True, description="Include road accessibility metrics"),
    road_radius_km: Optional[float] = Query(None, gt=0, description="Override radius for road metrics"),
) -> Any:
    svc = PredictionService.get_instance()
    try:
        lat_f = _parse_float_param(lat, "lat")
        lon_f = _parse_float_param(lon, "lon")

        payload = svc.build_feature_payload(
            lat_f,
            lon_f,
            radius_km=radius_km,
            decay_scale_km=decay_scale_km,
            include_network=include_network,
            sort_by=sort_by,
            include_road_metrics=include_road_metrics,
            road_radius_km=road_radius_km,
        )
        feature_names = payload.get("feature_names") or []
        features = payload.get("features") or {}
        ordered = {name: float(features.get(name, 0.0)) for name in feature_names}

        return {
            "center": {"lat": lat_f, "lon": lon_f},
            "radius_km": payload.get("primary_radius_km"),
            "feature_names": feature_names,
            "feature_vector": ordered,
            "road_accessibility": payload.get("road_accessibility"),
        }
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
