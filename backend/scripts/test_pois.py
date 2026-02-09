from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

resp = client.get('/api/v1/pois/detailed?lat=27.6742856&lon=85.4327744&radius_km=1.0')
print('status_code:', resp.status_code)
try:
    j = resp.json()
    import json
    print(json.dumps(j, indent=2, ensure_ascii=False)[:4000])
except Exception as e:
    print('failed to parse json:', e)
    print(resp.text)
