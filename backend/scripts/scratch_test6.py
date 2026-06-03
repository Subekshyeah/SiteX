import os
import pickle
import networkx as nx
import pandas as pd
import time
from app.lib.road_network import RoadNetwork
from app.api.endpoints.pois import _network_path_map, _network_distance_map

cache_path = "Data/road_graph_cache_osmnx_osmnx_valley.pkl"
if os.path.exists(cache_path):
    with open(cache_path, "rb") as fh:
        graph = pickle.load(fh)
    road_net = RoadNetwork(graph)
else:
    print("Cache not found")
    exit()

lat, lon = 27.696, 85.377
radius_km = 0.3
radius_m = radius_km * 1000.0

poi_df = pd.read_csv("Data/CSV_Reference/final/cafe_final.csv")
# Filter to 300m using haversine first to match get_pois behavior
from app.api.endpoints.pois import _haversine_vec_km
dists_km = _haversine_vec_km(lat, lon, poi_df["lat"].values, poi_df["lng"].values)
subset = poi_df[dists_km <= radius_km].copy().reset_index(drop=True)
print(f"Found {len(subset)} candidate POIs within {radius_km}km")

center_node, _ = road_net.snap_point(lat, lon)
print(f"Center node: {center_node}")

if center_node is not None:
    print("Computing distance map...")
    dist_map = _network_distance_map(road_net, lat, lon, subset["lat"], subset["lng"], radius_m)
    print(f"Distance map found {len(dist_map)} POIs")
    
    print("Computing path map...")
    path_map = _network_path_map(road_net, lat, lon, subset["lat"], subset["lng"], radius_m)
    print(f"Path map size: {len(path_map)}")
    
    if not path_map and len(subset) > 0:
        print("Debugging why path map is empty...")
        # Get snapped nodes for these POIs
        safe_lats = subset["lat"].tolist()
        safe_lons = subset["lng"].tolist()
        poi_nodes, _ = road_net.snap_points(safe_lats, safe_lons)
        for i, node_id in enumerate(poi_nodes):
            print(f"POI {i} at ({safe_lats[i]}, {safe_lons[i]}) snaps to node {node_id}")
            if node_id:
                try:
                    path = nx.shortest_path(road_net.graph, source=center_node, target=node_id, weight="length")
                    print(f"  Path exists: {len(path)} nodes")
                except Exception as e:
                    print(f"  Path error: {type(e).__name__}: {e}")
                    # Try without weight
                    try:
                        path = nx.shortest_path(road_net.graph, source=center_node, target=node_id)
                        print(f"  Path exists (unweighted): {len(path)} nodes")
                    except Exception as e2:
                        print(f"  Unweighted path error: {type(e2).__name__}: {e2}")
