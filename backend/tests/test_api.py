from __future__ import annotations

import json
import sys
from pathlib import Path

from fastapi.testclient import TestClient

# Ensure the backend package is importable when running pytest from repo root
BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
	sys.path.insert(0, str(BACKEND_ROOT))

from backend import app  # type: ignore  # noqa: E402


client = TestClient(app)


def test_root_returns_welcome_message() -> None:
	response = client.get("/")
	assert response.status_code == 200
	payload = response.json()
	assert payload["message"] == "Welcome to the Cafe Suitability API!"


def test_process_cafes_endpoint_flattens_payload() -> None:
	sample_payload = {
		"data": [
			{
				"title": "Cafe Boh",
				"categoryName": "Cafe",
				"categories": ["Cafe", "Coffee"],
				"address": "123 Bean Street",
				"city": "Kathmandu",
				"postalCode": "12345",
				"countryCode": "NP",
				"phone": "+9770000000",
				"placeId": "abc123",
				"cid": "cid-123",
				"url": "https://example.com",
				"searchString": "cafes near me",
				"totalScore": 4.5,
				"reviewsCount": 120,
				"location": {"lat": 27.7, "lng": 85.3},
				"openingHours": {"monday": "09:00-17:00"},
				"additionalInfo": {
					"Service options": [{"Dine-in": True}, {"Takeout": True}],
					"Offerings": [{"Coffee": True}, {"Alcohol": False}],
					"Dining options": [{"Breakfast": True}],
					"Amenities": [{"Wi-Fi": True}],
					"Atmosphere": [{"Casual": True}],
					"Crowd": [{"Family-friendly": True}],
					"Planning": [{"Accepts reservations": True}],
					"Payments": [{"Credit cards": True}],
				},
			}
		]
	}

	response = client.post("/api/v1/process-cafes/", json=sample_payload)
	assert response.status_code == 200

	processed = response.json()
	assert isinstance(processed, list)
	assert len(processed) == 1

	cafe = processed[0]
	assert cafe["name"] == "Cafe Boh"
	assert cafe["dine_in"] is True
	assert cafe["takeout"] is True
	assert cafe["wifi"] is True
	assert cafe["cash_only"] is False
	assert cafe["lat"] == 27.7
	assert cafe["lng"] == 85.3
	assert json.loads(cafe["weekly_hours"]) == sample_payload["data"][0]["openingHours"]
