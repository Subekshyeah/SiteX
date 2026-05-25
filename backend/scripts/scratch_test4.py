import requests
import json

url = "http://127.0.0.1:8000/api/v1/pois/?lat=27.7172&lon=85.3240&radius_km=0.3"
try:
    response = requests.get(url)
    data = response.json()
    # Check if 'path' exists in the first POI of the first category
    pois = data.get("pois", {})
    if not pois:
        print("No POIs found in response")
    else:
        for cat, items in pois.items():
            if items:
                print(f"Category: {cat}")
                print(f"First item keys: {items[0].keys()}")
                if 'path' in items[0]:
                    print(f"Path has {len(items[0]['path'])} points. First 2 points:")
                    print(items[0]['path'][:2])
                else:
                    print("No 'path' key found in item!")
                break
except Exception as e:
    print(f"Error: {e}")
