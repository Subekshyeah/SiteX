import pickle
import os

path = 'Data/road_graph_cache_osmnx_osmnx_valley.pkl'
if os.path.exists(path):
    with open(path, 'rb') as f:
        g = pickle.load(f)
    node = list(g.nodes())[0]
    print(f"Node: {node}, Type: {type(node)}")
else:
    print("Graph not found")
