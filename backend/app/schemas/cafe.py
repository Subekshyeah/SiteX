# app/schemas/cafe.py
from typing import List, Dict, Any

from pydantic import BaseModel, ConfigDict


class CafeDataPayload(BaseModel):
    """The expected structure for the incoming raw data."""

    model_config = ConfigDict(
        json_schema_extra={
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
    )

    data: List[Dict[str, Any]]