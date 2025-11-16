from fastapi import APIRouter, Query, HTTPException
from typing import Dict, Any
import pandas as pd
import math
from pathlib import Path

router = APIRouter(prefix="/pois", tags=["pois"])


def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0  # Earth radius in km
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


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
        df = pd.read_csv(fpath)

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

        items = []
        for _, row in df.iterrows():
            try:
                rlat = float(row[lat_col])
                rlon = float(row[lon_col])
            except Exception:
                continue
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