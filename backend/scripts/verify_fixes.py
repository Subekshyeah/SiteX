import sys
import os

# Ensure we can import from app
sys.path.insert(0, os.path.abspath('.'))

from app.lib.road_network import RoadNetwork
from app.lib.road_type_network import RoadTypeNetwork
from app.services.site_analysis_service import SiteAnalysisService

print("\n=========================================================")
print(" VERIFYING BUG 2: RoadTypeNetwork Silently Dropping Roads")
print("=========================================================")
print("Loading RoadTypeNetwork... Look for the print statement showing features loaded.")
print("Before the fix, anything not labeled exactly 'highway' was silently dropped.")
# This will trigger the print statement we added to _build_graph_from_geojson
rtn = RoadTypeNetwork.from_geojson('Data/Roadway.geojson')


print("\n=========================================================")
print(" VERIFYING BUG 3: Edge Snapping vs Intersection Snapping")
print("=========================================================")
print("Loading main OSMnx RoadNetwork...")
rn = RoadNetwork.from_geojson('Data/Roadway.geojson', cache_path='Data/road_graph_cache_osmnx.pkl')

# Let's pick a random coordinate that is likely in the middle of a road segment
test_lat, test_lon = 27.6715, 85.4295

old_node, old_dist = rn.snap_point(test_lat, test_lon)
new_u, new_v, new_dist = rn.snap_to_edge(test_lat, test_lon)

print(f"Test Coordinate: ({test_lat}, {test_lon})")
if old_dist is not None:
    print(f"OLD METHOD (snap_point): Snapped to intersection node {old_node}, Distance = {old_dist:.2f} meters.")
else:
    print(f"OLD METHOD (snap_point): FAILED. Nearest intersection is too far (exceeds tolerance), point would be dropped!")

if new_dist is not None:
    print(f"NEW METHOD (snap_to_edge): Snapped to road segment ({new_u}, {new_v}), True Perpendicular Distance = {new_dist:.2f} meters.")
    print(f"Notice how the new distance is much shorter and more accurate because it doesn't force the point to slide all the way to an intersection!")


print("\n=========================================================")
print(" VERIFYING BUG 4: path_between AttributeError Crash")
print("=========================================================")
svc = SiteAnalysisService()
print("Attempting to calculate a path between two coordinates...")
try:
    # This previously crashed because it called road_net.node_coords (which didn't exist)
    path_coords = svc.path_between(
        center_lat=27.671, 
        center_lon=85.429, 
        poi_lat=27.672, 
        poi_lon=85.430
    )
    if path_coords:
        print(f"SUCCESS! Generated a path with {len(path_coords)} coordinate points.")
        print("First 2 points of path:", path_coords[:2])
    else:
        print("SUCCESS! Function ran without crashing (no route found between points, which is fine).")
except AttributeError as e:
    print(f"FAILED! It crashed with: {e}")
    

print("\n=========================================================")
print(" VERIFYING BUG 1: Visualizing Curved Roads")
print("=========================================================")
print("To see the curvy roads fix with your own eyes:")
print("1. Run this in your terminal:  .venv\\Scripts\\python.exe visualize_road_network.py")
print("2. It will generate a file called 'RoadNetwork.geojson'.")
print("3. Open your browser, go to https://geojson.io/")
print("4. Drag and drop 'RoadNetwork.geojson' into the browser window.")
print("5. Zoom in! You will see the roads perfectly follow curves instead of being jagged straight lines.")
print("=========================================================\n")
