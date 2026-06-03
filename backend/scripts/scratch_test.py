import os
import sys

# Add backend to path
sys.path.insert(0, r"D:\projects\SiteX\backend")

from app.services.site_analysis_service import SiteAnalysisService

def main():
    svc = SiteAnalysisService()
    # Test coordinates from the UI (e.g. center: 27.672782, 85.431941)
    # Let's use the ones from the screenshot:
    # POI: 27.672879, 85.424937 (Cosmic Saving & Credit)
    # Center: Let's guess from POI distance. Wait, distance is 0.278 km, so center is nearby.
    # Let's just use two nearby points in Bhaktapur.
    
    # Point 1 (Bhaktapur Durbar Square area roughly)
    lat1, lon1 = 27.672782, 85.424937
    # Point 2
    lat2, lon2 = 27.672692, 85.424983

    try:
        path = svc.path_between(center_lat=lat1, center_lon=lon1, poi_lat=lat2, poi_lon=lon2)
        print("Path length:", len(path) if path else "None")
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
