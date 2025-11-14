# app/api/endpoints/cafe_processing.py
from fastapi import APIRouter
from typing import List, Dict, Any
from app.schemas.cafe import CafeDataPayload
from app.services.data_preprocessor import process_single_cafe

router = APIRouter()

@router.post("/process-cafes/")
def process_cafes_endpoint(payload: CafeDataPayload) -> List[Dict[str, Any]]:
    """
    Receives a list of raw cafe JSON objects, flattens them based on
    pre-defined rules, and returns a clean, tabular dataset.
    """
    processed_list = [process_single_cafe(cafe) for cafe in payload.data]
    return processed_list