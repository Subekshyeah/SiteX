from typing import List, Literal, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from app.services.prediction_service import PredictionService

router = APIRouter()

class Location(BaseModel):
    lat: float
    lon: float

class PredictionRequest(BaseModel):
    locations: List[Location]
    radius_km: Optional[float] = Field(None, gt=0, description="Radius to compute POI metrics (defaults to model radius)")
    decay_scale_km: Optional[float] = Field(None, gt=0, description="Decay scale for POI weights (defaults to radius_km)")
    include_network: bool = Field(True, description="Use road-network distances when available")
    sort_by: Literal["auto", "haversine", "network"] = Field(
        "auto", description="Distance mode: auto prefers network when available"
    )
    include_road_metrics: bool = Field(
        False, description="If true, compute road accessibility metrics for model inputs"
    )
    road_radius_km: Optional[float] = Field(
        None, gt=0, description="Override radius for road accessibility metrics (km)"
    )

class PredictionResponseItem(BaseModel):
    lat: float
    lon: float
    score: float
    risk_level: str

class PredictionResponse(BaseModel):
    predictions: List[PredictionResponseItem]


@router.post("/predict/", response_model=PredictionResponse)
def predict_score(request: PredictionRequest):
    """
    Predict success scores for multiple new cafe locations.
    """
    service = PredictionService.get_instance()
    results = []
    errors = []
    for loc in request.locations:
        try:
            prediction = service.predict(
                loc.lat,
                loc.lon,
                radius_km=request.radius_km,
                decay_scale_km=request.decay_scale_km,
                include_network=request.include_network,
                sort_by=request.sort_by,
                include_road_metrics=request.include_road_metrics,
                road_radius_km=request.road_radius_km,
            )
            results.append({
                "lat": loc.lat,
                "lon": loc.lon,
                "score": prediction['predicted_score'],
                "risk_level": prediction['risk_level']
            })
        except Exception as e:
            errors.append({
                "lat": loc.lat,
                "lon": loc.lon,
                "error": str(e)
            })

    if not results:
        raise HTTPException(status_code=500, detail={
            "message": "Prediction failed for all locations.",
            "errors": errors
        })

    return {"predictions": results}

