import os
import sys

sys.path.insert(0, r"D:\projects\SiteX\backend")

from app.services.site_analysis_service import SiteAnalysisService

def main():
    svc = SiteAnalysisService()
    lat1, lon1 = 27.672782, 85.431941
    lat2, lon2 = 27.672879, 85.424937
    
    path = svc.path_between(center_lat=lat1, center_lon=lon1, poi_lat=lat2, poi_lon=lon2)
    print("Path returned:", path)

if __name__ == "__main__":
    main()
