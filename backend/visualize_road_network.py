#!/usr/bin/env python3
"""Visualize the OSMnx road network using a lightweight GeoJSON + Leaflet approach."""

import json
import os
from app.lib.road_network import RoadNetwork

# Determine absolute cache path (use the newer OSMnx cache)
script_dir = os.path.dirname(os.path.abspath(__file__))
cache_path = os.path.join(script_dir, "Data", "road_graph_cache_osmnx.pkl")
print(f"Cache path: {cache_path}")
print(f"Cache exists: {os.path.exists(cache_path)}")

# Load the cached graph
print("Loading road network...")
rn = RoadNetwork.from_geojson(
    geojson_path="Data/Roadway.geojson",
    cache_path=cache_path
)

print(f"Graph loaded: {rn.node_count} nodes, {rn.edge_count} edges")

# Calculate center from nodes
print("Calculating map center...")
node_xs = [rn.graph.nodes[n]['x'] for n in rn.graph.nodes()]
node_ys = [rn.graph.nodes[n]['y'] for n in rn.graph.nodes()]
center_lat = sum(node_ys) / len(node_ys)
center_lng = sum(node_xs) / len(node_xs)
print(f"  Center: ({center_lat:.4f}, {center_lng:.4f})")

# Create GeoJSON from edges — use edge geometry when available to preserve curves
print("Building GeoJSON (all edges - may take a moment)...")
edges_data = list(rn.graph.edges(data=True))
total_edges = len(edges_data)

features = []
for idx, (u, v, data) in enumerate(edges_data):
    if idx % 5000 == 0:
        print(f"  Processing {idx}/{total_edges}...")

    geom = data.get("geometry")  # Shapely LineString with full curve points
    if geom is not None:
        # Extract all intermediate points to follow the road's actual shape
        coords = [[x, y] for x, y in geom.coords]
    else:
        # Fallback: straight line between the two endpoint nodes
        u_lng, u_lat = rn.graph.nodes[u]["x"], rn.graph.nodes[u]["y"]
        v_lng, v_lat = rn.graph.nodes[v]["x"], rn.graph.nodes[v]["y"]
        coords = [[u_lng, u_lat], [v_lng, v_lat]]

    features.append({
        "type": "Feature",
        "geometry": {
            "type": "LineString",
            "coordinates": coords,
        },
        "properties": {
            "type": "road",
            "highway": data.get("highway", ""),
            "length_m": data.get("length", 0),
            "oneway": data.get("oneway", False),
        }
    })

geojson = {
    "type": "FeatureCollection",
    "features": features
}

print(f"Created GeoJSON with {len(features)} features (sampled from {total_edges})")

# Create HTML with Leaflet
html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <title>Kathmandu Road Network</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <style>
        body {{ margin: 0; padding: 0; }}
        #map {{ position: absolute; top: 0; bottom: 0; width: 100%; }}
        .info {{ padding: 6px 8px; background: white; box-shadow: 0 0 15px rgba(0,0,0,0.2); border-radius: 5px; }}
    </style>
</head>
<body>
    <div id="map"></div>
    <script>
        const map = L.map('map').setView([{center_lat:.6f}, {center_lng:.6f}], 14);
        L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
            attribution: '© OpenStreetMap contributors',
            maxZoom: 19
        }}).addTo(map);
        
        const geojson = {json.dumps(geojson)};
        
        L.geoJSON(geojson, {{
            style: {{ color: 'blue', weight: 2, opacity: 0.7 }}
        }}).addTo(map);
        
        const info = document.createElement('div');
        info.className = 'info';
        info.innerHTML = '<h4>Kathmandu Road Network</h4><p>{len(features):,} roads shown (ALL segments)</p>';
        info.style.position = 'absolute';
        info.style.bottom = '10px';
        info.style.right = '10px';
        map._controlContainer.appendChild(info);
    </script>
</body>
</html>
"""

# Save HTML
output_file = "road_network_interactive.html"
print(f"Saving to {output_file}...")
with open(output_file, 'w') as f:
    f.write(html)

# Also save raw GeoJSON for geojson.io
geojson_output = "RoadNetwork_Export.geojson"
print(f"Saving raw GeoJSON to {geojson_output}...")
with open(geojson_output, 'w', encoding='utf-8') as f:
    json.dump({"type": "FeatureCollection", "features": features}, f)

print(f"✓ Saved HTML to: {output_file}")
print(f"✓ Saved GeoJSON to: {geojson_output}")
print(f"✓ Open in browser: file://{__file__.replace(chr(92), '/')}")
print(f"✓ Shows {len(features):,} roads (ALL edges, unsampled)")
