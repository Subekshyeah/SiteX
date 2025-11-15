#!/usr/bin/env python3
import os, json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / 'data'
OUT = DATA_DIR / 'datasets.json'

geo_files = sorted(DATA_DIR.glob('*.geojson'))
items = []
for p in geo_files:
    name = p.stem
    # human-friendly name: capitalize words
    pretty = ' '.join([w.capitalize() for w in name.replace('_',' ').split()])
    items.append({
        'id': name,
        'name': pretty,
        'path': f'/data/{p.name}'
    })

OUT.write_text(json.dumps(items, indent=2), encoding='utf-8')
print(f'Wrote {OUT} with {len(items)} entries')
