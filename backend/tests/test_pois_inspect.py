import importlib.util
import math
from pathlib import Path


def _load_haversine():
    p = Path(__file__).resolve().parents[1] / "scripts" / "pois_inspect.py"
    spec = importlib.util.spec_from_file_location("pois_inspect", str(p))
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)  # type: ignore
    return module.haversine_km


def test_haversine_basic():
    # Approx distance between (0,0) and (0,1) is ~111.32 km
    haversine_km = _load_haversine()
    d = haversine_km(0.0, 0.0, 0.0, 1.0)
    assert math.isfinite(d)
    assert abs(d - 111.319) < 0.5
