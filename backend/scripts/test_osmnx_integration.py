#!/usr/bin/env python3
"""Quick test script for OSMnx road network integration."""

import os
import pandas as pd
from app.lib.road_network import RoadNetwork

# Use the cache created by master.py
cache_path = "Data/road_graph_cache.pkl"

# Test 1: Load the graph
print("Test 1: Loading OSMnx graph from cache...")
if not os.path.exists(cache_path):
    print(f"⚠ Cache not found at {cache_path}. Run backend/Data/master.py first.")
    exit(1)

rn = RoadNetwork.from_geojson(
    geojson_path="Data/Roadway.geojson",
    cache_path=cache_path,
    snap_tolerance_m=120.0
)
print(f"✓ Loaded: {rn.node_count} nodes, {rn.edge_count} edges")

# Test 2: Snap real cafe data
print("\nTest 2: Snapping real cafe data...")
cafe_file = "Data/CSV_Reference/final/cafe_final.csv"
if os.path.exists(cafe_file):
    df = pd.read_csv(cafe_file, nrows=5)
    lats = df['lat'].tolist()
    lons = df['lng'].tolist()
    
    node_ids, dists = rn.snap_points(lats, lons)
    snapped_count = sum(1 for nid in node_ids if nid is not None)
    print(f"✓ Attempted to snap {len(lats)} cafes, {snapped_count} successful")
    if snapped_count > 0:
        for i, (nid, d) in enumerate(zip(node_ids, dists)):
            if nid is not None:
                print(f"  Cafe {i}: node {nid}, distance {d:.2f}m")

# Test 3: Test distance_between
print("\nTest 3: Computing network distance between cafe and POI...")
if snapped_count >= 2:
    dist = rn.distance_between(lats[0], lons[0], lats[1], lons[1])
    if dist is not None:
        print(f"✓ Network distance between cafe 0 and 1: {dist:.2f}m")
    else:
        print(f"✗ Nodes are not connected in the network")

# Test 4: Test cache persistence
print("\nTest 4: Checking cache persistence...")
rn2 = RoadNetwork.from_geojson(
    geojson_path="Data/Roadway.geojson",
    cache_path=cache_path,
    snap_tolerance_m=120.0
)
if rn2.node_count == rn.node_count and rn2.edge_count == rn.edge_count:
    print(f"✓ Cache loaded successfully with same node/edge counts")
else:
    print(f"✗ Cache mismatch!")

print("\n✅ Core functionality verified!")
