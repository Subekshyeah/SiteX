#!/usr/bin/env python3
"""
Convert CSV files with lat/lng columns into GeoJSON FeatureCollections.
Usage:
  python3 scripts/csv2geo.py data/temples.csv data/compact_summary_images.csv
This will create `data/temples.geojson` and `data/compact_summary_images.geojson`.
"""
import csv
import json
import sys
import os
from typing import Optional, Dict, Any

LAT_KEYS = {'lat', 'latitude', 'y', 'lat_dd', 'lat_deg'}
LON_KEYS = {'lng', 'lon', 'longitude', 'x', 'lng_dd', 'lon_deg'}


def find_coord_keys(header_row):
    lower = [h.lower() for h in header_row]
    lat_key = None
    lon_key = None
    for i, h in enumerate(lower):
        if h in LAT_KEYS and lat_key is None:
            lat_key = header_row[i]
        if h in LON_KEYS and lon_key is None:
            lon_key = header_row[i]
    # also try common pairs
    if lat_key is None:
        # try 'latitude' substring
        for i, h in enumerate(lower):
            if 'lat' in h and lat_key is None:
                lat_key = header_row[i]
    if lon_key is None:
        for i, h in enumerate(lower):
            if 'lon' in h or 'lng' in h and lon_key is None:
                lon_key = header_row[i]
    return lat_key, lon_key


def to_float(v: Optional[str]) -> Optional[float]:
    if v is None:
        return None
    v = v.strip()
    if v == '':
        return None
    try:
        return float(v)
    except Exception:
        # try removing stray characters
        cleaned = v.replace('\u00a0','').replace(',', '')
        try:
            return float(cleaned)
        except Exception:
            return None


def csv_to_geojson(inpath: str, outpath: str) -> Dict[str, Any]:
    features = []
    with open(inpath, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []
        lat_key, lon_key = find_coord_keys(fieldnames)
        for row in reader:
            # copy properties as-is
            props = {k: (v if v is not None else '') for k, v in row.items()}
            lat = None
            lon = None
            if lat_key and lon_key:
                lat = to_float(row.get(lat_key))
                lon = to_float(row.get(lon_key))
            else:
                # try guessing from common keys in row
                for k, v in row.items():
                    lk = (k or '').lower()
                    if lk in LAT_KEYS and lat is None:
                        lat = to_float(v)
                    if lk in LON_KEYS and lon is None:
                        lon = to_float(v)
            if lat is None or lon is None:
                # try alternative keys
                for k, v in row.items():
                    lk = (k or '').lower()
                    if (('lat' in lk) or ('latitude' in lk)) and lat is None:
                        lat = to_float(v)
                    if (('lon' in lk) or ('lng' in lk) or ('longitude' in lk)) and lon is None:
                        lon = to_float(v)

            if lat is None or lon is None:
                # skip rows without coordinates
                continue
            feat = {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [lon, lat]},
                "properties": props
            }
            features.append(feat)
    fc = {"type": "FeatureCollection", "features": features}
    with open(outpath, 'w', encoding='utf-8') as out:
        json.dump(fc, out, ensure_ascii=False, indent=2)
    return fc


def main(argv):
    if len(argv) < 2:
        print("Usage: csv2geo.py input.csv [other.csv ...]")
        return 1
    for inpath in argv[1:]:
        if not os.path.exists(inpath):
            print(f"Input not found: {inpath}")
            continue
        base = os.path.splitext(os.path.basename(inpath))[0]
        outdir = os.path.join(os.path.dirname(inpath))
        outpath = os.path.join(outdir, f"{base}.geojson")
        print(f"Converting {inpath} -> {outpath} ...")
        fc = csv_to_geojson(inpath, outpath)
        print(f"Wrote {len(fc['features'])} features to {outpath}")
    return 0

if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
