#!/usr/bin/env python3
import csv
import json
from pathlib import Path

# Prefer merged file if present
base = Path('comp/csv')
merged = base / 'compact_summary_merged.csv'
orig = base / 'compact_summary.csv'
out = base / 'compact_summary.geojson'

infile = merged if merged.exists() else orig
if not infile.exists():
    raise SystemExit(f'Missing input CSV: {infile}')

features = []
with infile.open('r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        # Parse lat/lng
        lat_raw = row.get('lat','').strip()
        lng_raw = row.get('lng','').strip()
        try:
            lat = float(lat_raw)
            lng = float(lng_raw)
        except Exception:
            continue
        # skip invalid coords
        if lat==0.0 and lng==0.0:
            continue
        # properties requested by user
        def to_float(x):
            try:
                return float(x)
            except Exception:
                return None
        def to_int(x):
            try:
                return int(float(x))
            except Exception:
                return None
        properties = {}
        properties['name'] = row.get('name','')
        r = to_float(row.get('rating',''))
        if r is not None:
            properties['rating'] = r
        else:
            properties['rating'] = None
        rc = to_int(row.get('reviews_count',''))
        properties['reviews_count'] = rc if rc is not None else None
        wh = to_float(row.get('weekly_hours',''))
        properties['weekly_hours'] = wh if wh is not None else None

        feature = {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [lng, lat]
            },
            'properties': properties
        }
        features.append(feature)

fc = {
    'type': 'FeatureCollection',
    'features': features
}

with out.open('w', encoding='utf-8') as f:
    json.dump(fc, f, ensure_ascii=False, indent=2)

print(f'Wrote {len(features)} features to {out}')
