import requests
import json

base_url = "http://127.0.0.1:8000/api/v1/pois/"
# Coordinates from the screenshot (Bhaktapur area)
params = {
    "lat": 27.672,
    "lon": 85.420,
    "radius_km": 0.3
}

try:
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    data = response.json()
    
    if "pois" in data:
        all_categories = data["pois"]
        total_pois = 0
        pois_with_paths = 0
        
        for cat, items in all_categories.items():
            total_pois += len(items)
            for item in items:
                if "path" in item and item["path"]:
                    pois_with_paths += 1
                else:
                    # Log some names that don't have paths
                    if len(items) < 5:
                         print(f"No path for {item.get('name')} in {cat}")
        
        print(f"Total POIs: {total_pois}")
        print(f"POIs with paths: {pois_with_paths}")
    else:
        print("No 'pois' key in response")
except Exception as e:
    print(f"Error: {e}")
