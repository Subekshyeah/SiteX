import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.api.endpoints.pois import get_pois_with_paths


if __name__ == '__main__':
    res = get_pois_with_paths(lat=27.6742856, lon=85.4327744, radius_km=1.0)
    import json
    print(json.dumps(res, ensure_ascii=False)[:4000])
