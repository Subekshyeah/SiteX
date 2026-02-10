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


def test_pois_decay_param_changes_weights() -> None:
    # Use a known center where data exists (Kathmandu sample)
    # use a denser sample center and larger radius to ensure POIs are returned
    params_small = {"lat": 27.6742856, "lon": 85.4327744, "radius_km": 1.0, "decay_scale_km": 0.1}
    params_large = {"lat": 27.6742856, "lon": 85.4327744, "radius_km": 1.0, "decay_scale_km": 10.0}

    r1 = client.get("/api/v1/pois", params=params_small)
    assert r1.status_code == 200
    payload1 = r1.json()

    r2 = client.get("/api/v1/pois", params=params_large)
    assert r2.status_code == 200
    payload2 = r2.json()

    # find first category and first item in each payload
    def first_weight(payload):
        pois = payload.get("pois", {})
        for cat, items in pois.items():
            if items:
                return items[0].get("weight")
        return None

    w1 = first_weight(payload1)
    w2 = first_weight(payload2)

    assert w1 is not None and w2 is not None
    # With a larger decay scale, the decayed weight should be larger (less decay)
    assert float(w2) >= float(w1)
