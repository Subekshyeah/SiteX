from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional, Sequence

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import Response
from pydantic import BaseModel, Field

from app.services.prediction_service import PredictionService
from app.services.site_analysis_service import SiteAnalysisService


router = APIRouter(prefix="/analysis")


def _parse_float_param(value: Any, name: str) -> float:
    if isinstance(value, bool):
        raise HTTPException(status_code=422, detail=f"'{name}' must be a number")
    if isinstance(value, (int, float)):
        return float(value)
    if value is None:
        raise HTTPException(status_code=422, detail=f"'{name}' must be a number")
    s = str(value).strip()
    if not s:
        raise HTTPException(status_code=422, detail=f"'{name}' must be a number")
    # Accept common locale decimal separator.
    s = s.replace(",", ".")
    try:
        return float(s)
    except Exception:
        raise HTTPException(status_code=422, detail=f"'{name}' must be a number")


def _parse_categories(raw: Optional[str]) -> Optional[List[str]]:
    if not raw:
        return None
    parts = [p.strip().lower() for p in raw.split(",") if p.strip()]
    return parts or None


def _parse_radii(raw: Optional[str], default: Sequence[float] = (0.25, 0.5, 1.0)) -> List[float]:
    if not raw:
        return list(default)
    out: List[float] = []
    for p in raw.split(","):
        p = p.strip()
        if not p:
            continue
        try:
            v = float(p)
        except Exception:
            continue
        if v > 0:
            out.append(v)
    return out or list(default)


class RankLocation(BaseModel):
    lat: float
    lon: float


class RankRequest(BaseModel):
    locations: List[RankLocation] = Field(default_factory=list)


@router.get("/nearby/")
def nearby(
    lat: str = Query(..., description="Latitude of center", examples=["27.672782"]),
    lon: str = Query(..., description="Longitude of center", examples=["85.431941"]),
    radius_km: float = Query(1.0, gt=0, description="Search radius (km)"),
    limit: int = Query(10, ge=1, le=200, description="Max items per category"),
    categories: Optional[str] = Query(None, description="Comma-separated categories (cafes,banks,...)"),
    decay_scale_km: float = Query(1.0, gt=0, description="Decay scale (km) for weights"),
    include_network: bool = Query(True, description="If true, include road-network distance when available"),
    sort_by: Literal["auto", "haversine", "network"] = Query(
        "auto", description="Sorting distance: auto prefers network when available"
    ),
) -> Any:
    svc = SiteAnalysisService()
    try:
        lat_f = _parse_float_param(lat, "lat")
        lon_f = _parse_float_param(lon, "lon")
        cats = _parse_categories(categories)
        data = svc.nearby(
            lat_f,
            lon_f,
            radius_km=radius_km,
            limit=limit,
            categories=cats,
            decay_scale_km=decay_scale_km,
            include_network=include_network,
            sort_by=sort_by,
        )
        return {
            "center": {"lat": lat_f, "lon": lon_f},
            "radius_km": radius_km,
            "limit": limit,
            "categories": cats,
            "nearby": data,
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/summary/")
def ring_summary(
    lat: str = Query(..., description="Latitude of center", examples=["27.672782"]),
    lon: str = Query(..., description="Longitude of center", examples=["85.431941"]),
    radii_km: Optional[str] = Query("0.25,0.5,1.0", description="Comma-separated radii in km"),
    categories: Optional[str] = Query(None, description="Comma-separated categories"),
    decay_scale_km: float = Query(1.0, gt=0, description="Decay scale (km) for weights"),
    include_network: bool = Query(True, description="If true, use road-network distance when available"),
    sort_by: Literal["auto", "haversine", "network"] = Query(
        "auto", description="Distance mode: auto prefers network when available"
    ),
) -> Any:
    svc = SiteAnalysisService()
    try:
        lat_f = _parse_float_param(lat, "lat")
        lon_f = _parse_float_param(lon, "lon")
        cats = _parse_categories(categories)
        radii = _parse_radii(radii_km)
        data = svc.ring_summary(
            lat_f,
            lon_f,
            radii_km=radii,
            categories=cats,
            decay_scale_km=decay_scale_km,
            include_network=include_network,
            sort_by=sort_by,
        )
        data["radii_km"] = radii
        data["categories_filter"] = cats
        return data
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/competition/")
def competition(
    lat: str = Query(..., description="Latitude of center", examples=["27.672782"]),
    lon: str = Query(..., description="Longitude of center", examples=["85.431941"]),
    radius_km: float = Query(1.0, gt=0, description="Radius (km)"),
    decay_scale_km: float = Query(1.0, gt=0, description="Decay scale (km) for weights"),
    include_network: bool = Query(True, description="If true, use road-network distance when available"),
    sort_by: Literal["auto", "haversine", "network"] = Query(
        "auto", description="Distance mode: auto prefers network when available"
    ),
) -> Any:
    svc = SiteAnalysisService()
    try:
        lat_f = _parse_float_param(lat, "lat")
        lon_f = _parse_float_param(lon, "lon")
        return svc.competition_index(
            lat_f,
            lon_f,
            radius_km=radius_km,
            decay_scale_km=decay_scale_km,
            include_network=include_network,
            sort_by=sort_by,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/report/")
def report(
    lat: str = Query(..., description="Latitude", examples=["27.672782"]),
    lon: str = Query(..., description="Longitude", examples=["85.431941"]),
    radius_km: float = Query(1.0, gt=0, description="Radius for nearby/competition"),
    limit: int = Query(10, ge=1, le=200, description="Max nearby items per category"),
    radii_km: Optional[str] = Query("0.25,0.5,1.0", description="Comma-separated radii for summaries"),
    categories: Optional[str] = Query(None, description="Comma-separated categories"),
    decay_scale_km: float = Query(1.0, gt=0, description="Decay scale (km)"),
    include_network: bool = Query(True, description="If true, use road-network distance when available"),
    sort_by: Literal["auto", "haversine", "network"] = Query("auto"),
) -> Any:
    svc = SiteAnalysisService()
    try:
        lat_f = _parse_float_param(lat, "lat")
        lon_f = _parse_float_param(lon, "lon")
        cats = _parse_categories(categories)
        radii = _parse_radii(radii_km)
        pred_svc = PredictionService.get_instance()
        pred = pred_svc.predict(lat_f, lon_f)

        nearby_data = svc.nearby(
            lat_f,
            lon_f,
            radius_km=radius_km,
            limit=limit,
            categories=cats,
            decay_scale_km=decay_scale_km,
            include_network=include_network,
            sort_by=sort_by,
        )
        summary_data = svc.ring_summary(
            lat_f,
            lon_f,
            radii_km=radii,
            categories=cats,
            decay_scale_km=decay_scale_km,
            include_network=include_network,
            sort_by=sort_by,
        )
        comp = svc.competition_index(
            lat_f,
            lon_f,
            radius_km=radius_km,
            decay_scale_km=decay_scale_km,
            include_network=include_network,
            sort_by=sort_by,
        )

        return {
            "center": {"lat": lat_f, "lon": lon_f},
            "prediction": {
                "score": float(pred["predicted_score"]),
                "risk_level": pred.get("risk_level"),
            },
            "estimated_features": pred.get("estimated_features"),
            "nearby": {
                "radius_km": radius_km,
                "limit": limit,
                "data": nearby_data,
            },
            "summary": summary_data,
            "competition": comp,
            "params": {
                "categories": cats,
                "decay_scale_km": decay_scale_km,
                "include_network": include_network,
                "sort_by": sort_by,
            },
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/rank/")
def rank_locations(request: RankRequest) -> Any:
    if not request.locations:
        raise HTTPException(status_code=400, detail="No locations provided")

    svc = PredictionService.get_instance()
    rows: List[Dict[str, Any]] = []
    errors: List[Dict[str, Any]] = []

    for loc in request.locations:
        try:
            pred = svc.predict(loc.lat, loc.lon)
            rows.append(
                {
                    "lat": float(loc.lat),
                    "lon": float(loc.lon),
                    "score": float(pred["predicted_score"]),
                    "risk_level": pred.get("risk_level"),
                }
            )
        except Exception as exc:
            errors.append({"lat": float(loc.lat), "lon": float(loc.lon), "error": str(exc)})

    if not rows:
        raise HTTPException(status_code=500, detail={"message": "Ranking failed for all locations", "errors": errors})

    rows.sort(key=lambda r: float(r.get("score") or float("-inf")), reverse=True)
    for i, r in enumerate(rows, start=1):
        r["rank"] = i

    return {"ranked": rows, "errors": errors}


@router.post("/rank.csv")
def rank_locations_csv(request: RankRequest) -> Response:
    ranked = rank_locations(request)
    rows = ranked.get("ranked") or []
    if not rows:
        raise HTTPException(status_code=500, detail="No rows to export")
    fieldnames = ["rank", "lat", "lon", "score", "risk_level"]
    csv_text = SiteAnalysisService.to_csv(rows, fieldnames)
    return Response(
        content=csv_text,
        media_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="ranked_locations.csv"'},
    )


@router.get("/path/")
def path(
    center_lat: float = Query(..., description="Center latitude"),
    center_lon: float = Query(..., description="Center longitude"),
    poi_lat: float = Query(..., description="POI latitude"),
    poi_lon: float = Query(..., description="POI longitude"),
) -> Any:
    svc = SiteAnalysisService()
    try:
        coords = svc.path_between(
            center_lat=center_lat,
            center_lon=center_lon,
            poi_lat=poi_lat,
            poi_lon=poi_lon,
        )
        return {
            "center": {"lat": center_lat, "lon": center_lon},
            "poi": {"lat": poi_lat, "lon": poi_lon},
            "path": coords,
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
