from typing import Any, Literal, Optional

from fastapi import APIRouter, HTTPException, Query

from app.services.prediction_service import PredictionService


router = APIRouter(prefix="/poi-metrics")


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
def poi_metrics(
    lat: str = Query(..., description="Latitude of center", examples=["27.672782"]),
    lon: str = Query(..., description="Longitude of center", examples=["85.431941"]),
    radius_km: Optional[float] = Query(None, gt=0, description="Radius for POI metrics (km)"),
    decay_scale_km: Optional[float] = Query(None, gt=0, description="Decay scale (km) for weights"),
    include_network: bool = Query(True, description="Use road-network distances when available"),
    sort_by: Literal["auto", "haversine", "network"] = Query(
        "auto", description="Distance mode: auto prefers network when available"
    ),
    include_road_metrics: bool = Query(False, description="Include road accessibility metrics"),
    road_radius_km: Optional[float] = Query(None, gt=0, description="Override radius for road metrics"),
) -> Any:
    svc = PredictionService.get_instance()
    try:
        lat_f = _parse_float_param(lat, "lat")
        lon_f = _parse_float_param(lon, "lon")

        if radius_km is None:
            payload = svc.build_feature_payload(
                lat_f,
                lon_f,
                decay_scale_km=decay_scale_km,
                include_network=include_network,
                sort_by=sort_by,
                include_road_metrics=include_road_metrics,
                road_radius_km=road_radius_km,
            )
            return {
                "center": {"lat": lat_f, "lon": lon_f},
                "radius_km": payload.get("primary_radius_km"),
                "features": payload.get("features"),
                "rings": payload.get("rings"),
                "road_accessibility": payload.get("road_accessibility"),
            }

        metrics = svc.build_metrics_for_radius(
            lat_f,
            lon_f,
            radius_km=float(radius_km),
            decay_scale_km=decay_scale_km,
            include_network=include_network,
            sort_by=sort_by,
        )
        road_payload = None
        if include_road_metrics:
            payload = svc.build_feature_payload(
                lat_f,
                lon_f,
                radius_km=float(radius_km),
                decay_scale_km=decay_scale_km,
                include_network=include_network,
                sort_by=sort_by,
                include_road_metrics=True,
                road_radius_km=road_radius_km,
            )
            road_payload = payload.get("road_accessibility")
        return {
            "center": {"lat": lat_f, "lon": lon_f},
            "radius_km": metrics.get("radius_km"),
            "features": metrics.get("features"),
            "ring": metrics.get("ring"),
            "road_accessibility": road_payload,
        }
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
