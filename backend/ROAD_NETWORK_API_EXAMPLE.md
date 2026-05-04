#!/usr/bin/env python3
"""
Optional FastAPI endpoint to serve the road network as GeoJSON.
Add this to your backend/app/main.py to expose the road network to your React frontend.
"""

# Add these imports to your main.py:
# from app.core.road_network_service import get_road_network_geojson

# Add this endpoint to your FastAPI app:
"""
@app.get("/api/road-network")
async def get_road_network():
    '''Return the OSMnx road network as GeoJSON for Leaflet.'''
    try:
        geojson = get_road_network_geojson()
        return {"status": "success", "data": geojson}
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500
"""

# Then create backend/app/core/road_network_service.py:

"""
import osmnx as ox
import json
from app.lib.road_network import RoadNetwork

def get_road_network_geojson() -> dict:
    '''Convert cached OSMnx graph to GeoJSON.'''
    rn = RoadNetwork.from_geojson(
        geojson_path='backend/Data/Roadway.geojson',
        cache_path='backend/Data/road_graph_cache.pkl'
    )
    
    # Convert to GeoDataFrame
    gdf_edges = ox.graph_to_gdfs(rn.graph)[1]
    
    # Convert to GeoJSON
    geojson = json.loads(gdf_edges.to_json())
    
    return geojson
"""

# Usage in React (pseudocode):
"""
fetch('/api/road-network')
    .then(r => r.json())
    .then(data => {
        // Add GeoJSON layer to Leaflet map
        L.geoJSON(data.data, {
            style: { color: 'blue', weight: 1, opacity: 0.7 }
        }).addTo(map);
    });
"""
