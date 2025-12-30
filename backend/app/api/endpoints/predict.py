from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from app.services.prediction_service import PredictionService

router = APIRouter()

class PredictionRequest(BaseModel):
    lat: float
    lng: float

class PredictionResponse(BaseModel):
    predicted_score: float
    risk_level: str
    estimated_features: Dict[str, float]

@router.post("/predict-score/", response_model=PredictionResponse)
def predict_score(request: PredictionRequest):
    """
    Predict the success score for a new cafe location based on latitude and longitude.
    Uses k-Nearest Neighbors to estimate local POI density from the training dataset.
    """
    service = PredictionService.get_instance()
    try:
        result = service.predict(request.lat, request.lng)
        return result
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
