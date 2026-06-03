import os
import sys

sys.path.insert(0, r"D:\projects\SiteX\backend")

from app.services.site_analysis_service import SiteAnalysisService

def main():
    svc = SiteAnalysisService()
    lat1, lon1 = 27.672782, 85.431941 # Example center
    lat2, lon2 = 27.672879, 85.424937 # Cosmic Saving
    
    road_net = svc.get_road_network()
    if road_net is None:
        print("Road network is None")
        return

    center_node, _ = svc._resolve_center_node(road_net, float(lat1), float(lon1))
    poi_node, _ = svc._resolve_poi_node(road_net, float(lat2), float(lon2))
    
    print(f"Center node: {center_node}, POI node: {poi_node}")
    
    try:
        import networkx as nx
        node_path = nx.shortest_path(
            road_net.graph,
            source=int(center_node),
            target=int(poi_node),
            weight="weight",
        )
        print("Path found:", len(node_path))
    except Exception as e:
        print("Exception during shortest_path:", repr(e))

if __name__ == "__main__":
    main()
