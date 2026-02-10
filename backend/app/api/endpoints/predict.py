from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from app.services.prediction_service import PredictionService

router = APIRouter()

class Location(BaseModel):
    lat: float
    lon: float

class PredictionRequest(BaseModel):
    locations: List[Location]

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
            prediction = service.predict(loc.lat, loc.lon)
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

