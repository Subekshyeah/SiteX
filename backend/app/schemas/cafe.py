# app/schemas/cafe.py
from pydantic import BaseModel
from typing import List, Dict, Any

class CafeDataPayload(BaseModel):
    """ The expected structure for the incoming raw data. """
    data: List[Dict[str, Any]]

    class Config:
        # Example to show how to handle example data in OpenAPI docs
        schema_extra = {
            "example": {
                "data": [
                    {
                        "title": "Cafe Boh",
                        "location": {"lat": 27.67, "lng": 85.39},
                        # ... other raw fields
                    }
                ]
            }
        }