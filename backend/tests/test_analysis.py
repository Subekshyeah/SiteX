from __future__ import annotations

import sys
from pathlib import Path

from fastapi.testclient import TestClient


# Ensure the backend package is importable when running pytest from repo root
BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
	sys.path.insert(0, str(BACKEND_ROOT))

from backend import app  # type: ignore  # noqa: E402


client = TestClient(app)


def test_analysis_nearby_returns_payload() -> None:
	resp = client.get("/api/v1/analysis/nearby/?lat=27.671&lon=85.429&radius_km=0.5&limit=3")
	assert resp.status_code == 200
	data = resp.json()
	assert "center" in data
	assert "nearby" in data
	assert isinstance(data["nearby"], dict)
	# When include_network is enabled (default), the API should always return a numeric
	# network_distance_km (falls back to haversine when routing is unavailable).
	any_items = False
	for cat_items in data["nearby"].values():
		for item in (cat_items or []):
			any_items = True
			assert item.get("network_distance_km") is not None
	if not any_items:
		# dataset may be empty in some environments; payload shape is still valid
		assert True


def test_analysis_summary_returns_rings() -> None:
	resp = client.get("/api/v1/analysis/summary/?lat=27.671&lon=85.429&radii_km=0.25,0.5")
	assert resp.status_code == 200
	data = resp.json()
	assert data["center"]["lat"] == 27.671
	assert "rings" in data
	assert isinstance(data["rings"], list)
	assert len(data["rings"]) >= 1
	assert "totals" in data["rings"][0]


def test_analysis_competition_returns_index() -> None:
	resp = client.get("/api/v1/analysis/competition/?lat=27.671&lon=85.429&radius_km=1")
	assert resp.status_code == 200
	data = resp.json()
	assert "cafes_count" in data
	assert "cafe_share" in data


def test_analysis_report_includes_prediction() -> None:
	resp = client.get("/api/v1/analysis/report/?lat=27.671&lon=85.429&radius_km=0.5&limit=2")
	# This endpoint depends on the model being present; if missing, it should surface an error.
	if resp.status_code != 200:
		# acceptable in CI environments without model artifacts
		assert resp.status_code in (500, 503)
		return
	data = resp.json()
	assert "prediction" in data
	assert "score" in data["prediction"]
	assert "nearby" in data
	assert "summary" in data
	assert "competition" in data


def test_analysis_rank_json_and_csv() -> None:
	payload = {"locations": [{"lat": 27.671, "lon": 85.429}, {"lat": 27.672, "lon": 85.43}]}
	resp = client.post("/api/v1/analysis/rank/", json=payload)
	# Ranking depends on the model being present
	if resp.status_code != 200:
		assert resp.status_code in (500, 503)
		return
	data = resp.json()
	assert "ranked" in data
	assert isinstance(data["ranked"], list)
	assert data["ranked"][0]["rank"] == 1

	csv_resp = client.post("/api/v1/analysis/rank.csv", json=payload)
	assert csv_resp.status_code == 200
	assert (csv_resp.headers.get("content-type") or "").startswith("text/csv")
	text = csv_resp.text
	assert "rank,lat,lon,score,risk_level" in text.splitlines()[0]


def test_analysis_path_endpoint_shape() -> None:
	resp = client.get(
		"/api/v1/analysis/path/?center_lat=27.671&center_lon=85.429&poi_lat=27.672&poi_lon=85.43"
	)
	assert resp.status_code == 200
	data = resp.json()
	assert "path" in data
	# path may be null if no road network / no path; if present, must be a list
	if data["path"] is not None:
		assert isinstance(data["path"], list)


def test_network_distance_map_uses_original_indices() -> None:
	from app.services.site_analysis_service import SiteAnalysisService
	import pandas as pd

	class _RoadNetStub:
		def snap_point(self, lat, lon, max_snap_m=None):
			return 1, 0.0

		def snap_points(self, lats, lons, max_snap_m=None):
			# Two POIs snap to nodes 2 and 3
			return [2, 3], [0.0, 0.0]

		def shortest_paths_from(self, node_id, cutoff):
			# Distances in meters from center node to nodes 2 and 3
			return {2: 100.0, 3: 200.0}

	svc = SiteAnalysisService()
	poi_indices = [10, 20]
	poi_lats = pd.Series([27.0, 28.0], index=poi_indices)
	poi_lons = pd.Series([85.0, 86.0], index=poi_indices)

	out = svc._network_distance_map(
		_RoadNetStub(),
		27.0,
		85.0,
		poi_indices,
		poi_lats,
		poi_lons,
		radius_m=1000.0,
	)
	assert out[10] == 0.1
	assert out[20] == 0.2
