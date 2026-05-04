#!/usr/bin/env python3
"""Visualize the OSMnx road network as an interactive Folium map."""

import folium
import osmnx as ox
from app.lib.road_network import RoadNetwork

# Load the cached graph
print("Loading road network...")
rn = RoadNetwork.from_geojson(
    geojson_path="Data/Roadway.geojson",
    cache_path="Data/road_graph_cache.pkl"
)

print(f"Graph loaded: {rn.node_count} nodes, {rn.edge_count} edges")

# Convert OSMnx graph to GeoJSON edges
print("Converting to GeoJSON...")
gdf_edges = ox.graph_to_gdfs(rn.graph)[1]

# Calculate center of the map
center_lat = gdf_edges.geometry.centroid.y.mean()
center_lng = gdf_edges.geometry.centroid.x.mean()

print(f"Map center: ({center_lat:.4f}, {center_lng:.4f})")

# Create Folium map
m = folium.Map(
    location=[center_lat, center_lng],
    zoom_start=14,
    tiles="OpenStreetMap"
)

# Add road network edges
print("Adding edges to map...")
for idx, row in gdf_edges.iterrows():
    coords = [(lat, lng) for lng, lat in zip(row.geometry.xy[0], row.geometry.xy[1])]
    folium.PolyLine(
        coords,
        color='blue',
        weight=2,
        opacity=0.7
    ).add_to(m)

# Save map
output_file = "road_network_interactive.html"
m.save(output_file)
print(f"✓ Saved to: {output_file}")
print(f"Open in browser: file://{__file__.replace(chr(92), '/')}")
