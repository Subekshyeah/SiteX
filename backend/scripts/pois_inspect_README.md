# pois_inspect.py

Usage example:

```bash
python backend/scripts/pois_inspect.py --lat 27.6742856 --lon 85.4327744 --radius-km 1.0 --decay-scale-km 1.0
```

The script prints JSON with per-category POI lists. Each POI entry includes:
- `haversine_km`: straight-line distance in kilometers (or `null`)
- `road_km`: roadway shortest-path distance in kilometers (if available)
- `base_weight_haversine` and `decayed_weight_haversine`
- `base_weight_road` and `decayed_weight_road`

If `backend/Data/CSV` is present the script will use those CSVs; otherwise it will look in `backend/Data/CSV_Reference/final`.

To force a specific road network file, pass `--road-geojson path/to/Roadway.geojson`.
