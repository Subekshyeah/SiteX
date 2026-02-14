#!/usr/bin/env python3
import argparse
import csv
import json
import math
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd
import numpy as np

# Ensure backend package dir is on sys.path so we can import app modules.
SCRIPT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = SCRIPT_DIR.parent
sys.path.insert(0, os.fspath(BACKEND_DIR))

from app.api.endpoints.pois import (
    _get_road_network,
    _network_distance_map,
    _network_path_map,
)


# DEFAULT_RADIUS_KM = 0.3
DEFAULT_RADIUS_KM = 1
DEFAULT_DECAY_SCALE_KM = 1.0

G_CAFE_DF: Optional[pd.DataFrame] = None
G_CAFE_LAT_COL: Optional[str] = None
G_CAFE_LON_COL: Optional[str] = None
G_DATASETS: Optional[Dict[str, Tuple[pd.DataFrame, str, str]]] = None
G_RADIUS_KM: float = DEFAULT_RADIUS_KM
G_DECAY_SCALE_KM: float = DEFAULT_DECAY_SCALE_KM
G_OUTPUT_DIR: Optional[Path] = None
G_RESUME: bool = True
G_ROAD_NET = None
G_RADIUS_SUFFIX: str = ""


def _slugify(value: str) -> str:
    if not value:
        return ""
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return value.strip("_")


def _find_lat_lon_cols(df: pd.DataFrame) -> Tuple[Optional[str], Optional[str]]:
    lat_col = None
    lon_col = None
    for c in df.columns:
        cl = c.lower()
        if cl in ("lat", "latitude", "y"):
            lat_col = c
        if cl in ("lon", "lng", "longitude", "x"):
            lon_col = c
    if lat_col is None or lon_col is None:
        num_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
        if len(num_cols) >= 2:
            lat_col = lat_col or num_cols[0]
            lon_col = lon_col or num_cols[1]
    return lat_col, lon_col


def _get_name(row: pd.Series) -> Optional[str]:
    for name_key in ("name", "Name", "NAME"):
        if name_key in row:
            val = row.get(name_key)
            if isinstance(val, str):
                return val
            if pd.notna(val):
                return str(val)
    return None


def _get_weight(row: pd.Series, typ: str) -> Optional[float]:
    if typ == "cafes":
        val = row.get("cafe_individual_score")
    else:
        val = row.get("final_weight")
    try:
        weight = float(val)
    except Exception:
        return None
    if not math.isfinite(weight):
        return None
    return weight


def _decay_weight(distance_km: float, radius_km: float, decay_scale_km: float) -> float:
    try:
        base_weight = max(0.0, 1.0 - (float(distance_km) / float(radius_km)))
    except Exception:
        base_weight = 0.0
    try:
        return base_weight * math.exp(-float(distance_km) / float(decay_scale_km))
    except Exception:
        return base_weight


def _load_poi_csv(path: Path) -> Tuple[pd.DataFrame, str, str]:
    df = pd.read_csv(path).reset_index(drop=True)
    lat_col, lon_col = _find_lat_lon_cols(df)
    if lat_col is None or lon_col is None:
        raise ValueError(f"No latitude/longitude columns found in {path}")
    df[lat_col] = pd.to_numeric(df[lat_col], errors="coerce")
    df[lon_col] = pd.to_numeric(df[lon_col], errors="coerce")
    return df, lat_col, lon_col


def _path_to_linestring(path_coords: List[Dict[str, float]]) -> List[List[float]]:
    coords = []
    for pt in path_coords:
        try:
            lat = float(pt["lat"])
            lon = float(pt["lon"])
        except Exception:
            continue
        if math.isfinite(lat) and math.isfinite(lon):
            coords.append([lon, lat])
    return coords


def _direct_linestring(cafe_lat: float, cafe_lon: float, poi_lat: float, poi_lon: float) -> List[List[float]]:
    return [[float(cafe_lon), float(cafe_lat)], [float(poi_lon), float(poi_lat)]]


def _haversine_vec_km(center_lat: float, center_lon: float, lats: np.ndarray, lons: np.ndarray) -> np.ndarray:
    r = 6371.0
    phi1 = np.radians(center_lat)
    phi2 = np.radians(lats)
    dphi = phi2 - phi1
    dlambda = np.radians(lons - center_lon)
    a = np.sin(dphi / 2.0) ** 2 + np.cos(phi1) * np.cos(phi2) * np.sin(dlambda / 2.0) ** 2
    c = 2.0 * np.arctan2(np.sqrt(a), np.sqrt(1.0 - a))
    return r * c


def _cafe_output_path(output_dir: Path, cafe_idx: int, cafe_name: str) -> Path:
    slug = _slugify(cafe_name or "")
    if slug:
        filename = f"cafe_{cafe_idx}_{slug}.geojson"
    else:
        filename = f"cafe_{cafe_idx}.geojson"
    return output_dir / filename


def _iter_geojson_files(input_dir: Path) -> List[Path]:
        return sorted(
                p
                for p in input_dir.glob("*.geojson")
                if p.is_file() and not p.name.endswith("_paths.geojson")
        )


def _append_bounds(bounds: List[float], coords: List[List[float]]) -> None:
        # bounds: [min_lon, min_lat, max_lon, max_lat]
        for lon, lat in coords:
                if len(bounds) == 0:
                        bounds[:] = [lon, lat, lon, lat]
                        continue
                bounds[0] = min(bounds[0], lon)
                bounds[1] = min(bounds[1], lat)
                bounds[2] = max(bounds[2], lon)
                bounds[3] = max(bounds[3], lat)


def _build_combined_paths(input_dir: Path) -> Tuple[Dict[str, Any], List[float]]:
        combined_features: List[Dict[str, Any]] = []
        bounds: List[float] = []

        for path in _iter_geojson_files(input_dir):
                try:
                        obj = json.loads(path.read_text(encoding="utf-8"))
                except Exception:
                        continue
                features = obj.get("features", []) if isinstance(obj, dict) else []
                for feat in features:
                        geom = feat.get("geometry", {}) if isinstance(feat, dict) else {}
                        coords = geom.get("coordinates") if isinstance(geom, dict) else None
                        if not isinstance(coords, list):
                                continue
                        combined_features.append(feat)
                        _append_bounds(bounds, coords)

        combined = {"type": "FeatureCollection", "features": combined_features}
        return combined, bounds


def _build_summary_row(
    cafe_df: pd.DataFrame,
    cafe_idx: int,
    decay_stats: Dict[str, Tuple[int, float]],
    radius_label: str,
    category_order: List[str],
    composite_lookup: Dict[Tuple[str, float, float], float],
    category_lookup: Dict[Tuple[str, float, float], str],
    lat_col: str,
    lon_col: str,
) -> Dict[str, Any]:
    row_data = cafe_df.iloc[cafe_idx]
    name_val = _get_name(row_data) or ""
    try:
        lat_val = float(row_data[lat_col])
    except Exception:
        lat_val = float("nan")
    try:
        lon_val = float(row_data[lon_col])
    except Exception:
        lon_val = float("nan")
    if not name_val or not math.isfinite(lat_val) or not math.isfinite(lon_val):
        return None
    try:
        cafe_weight = float(row_data.get("cafe_weight"))
    except Exception:
        cafe_weight = ""

    key = (name_val, round(lat_val, 6), round(lon_val, 6))
    poi_composite = composite_lookup.get(key, "")
    category_val = category_lookup.get(key, "")

    row = {
        "name": name_val,
        "lat": lat_val,
        "lng": lon_val,
        "category": category_val,
    }
    for cat in category_order:
        cnt, total = decay_stats.get(cat, (0, 0.0))
        avg = (total / cnt) if cnt else 0.0
        row[f"{cat}_count_{radius_label}"] = cnt
        row[f"{cat}_weight_{radius_label}"] = round(avg, 6)
    row["cafe_weight"] = cafe_weight
    row["poi_composite_score"] = poi_composite
    return row


def _render_map_html(title: str, geojson_name: str, bounds: List[float]) -> str:
        bounds_js = "null"
        if len(bounds) == 4:
                bounds_js = f"[[{bounds[1]}, {bounds[0]}], [{bounds[3]}, {bounds[2]}]]"
        return f"""<!doctype html>
<html lang=\"en\">
<head>
    <meta charset=\"utf-8\" />
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
    <title>{title}</title>
    <link
        rel=\"stylesheet\"
        href=\"https://unpkg.com/leaflet@1.9.4/dist/leaflet.css\"
        integrity=\"sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=\"
        crossorigin=\"\"
    />
    <style>
        html, body, #map {{ height: 100%; margin: 0; }}
        .panel {{
            position: absolute;
            top: 12px;
            left: 12px;
            background: #ffffff;
            padding: 10px 12px;
            z-index: 1000;
            border-radius: 8px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.15);
            font-family: Arial, sans-serif;
            width: 300px;
        }}
        .panel h1 {{ font-size: 14px; margin: 0 0 8px 0; }}
        .panel label {{ display: block; font-size: 12px; margin: 6px 0 4px 0; color: #333; }}
        .panel select {{ width: 100%; padding: 6px; font-size: 12px; }}
        .panel .muted {{ color: #666; font-size: 12px; margin-top: 6px; }}
    </style>
</head>
<body>
    <div id=\"map\"></div>
    <div class=\"panel\">
        <h1>{title}</h1>
        <label for=\"modeSelect\">Mode</label>
        <select id=\"modeSelect\">
            <option value=\"all\">All cafes</option>
            <option value=\"cafe\">Single cafe</option>
            <option value=\"poi\">Single cafe + POI</option>
        </select>
        <label for="allPartSelect">All mode part</label>
        <select id="allPartSelect"></select>
        <label for=\"cafeSelect\">Cafe</label>
        <select id=\"cafeSelect\"></select>
        <label for=\"poiSelect\">POI</label>
        <select id=\"poiSelect\"></select>
        <div id=\"status\" class=\"muted\">Loading paths...</div>
    </div>
    <script src=\"https://unpkg.com/leaflet@1.9.4/dist/leaflet.js\" integrity=\"sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=\" crossorigin=\"\"></script>
    <script>
        const map = L.map('map');
        const bounds = {bounds_js};
        if (bounds) {{
            map.fitBounds(bounds);
        }} else {{
            map.setView([27.7, 85.4], 12);
        }}
        L.tileLayer('https://tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
            maxZoom: 19,
            attribution: '&copy; OpenStreetMap'
        }}).addTo(map);

        const modeSelect = document.getElementById('modeSelect');
        const allPartSelect = document.getElementById('allPartSelect');
        const cafeSelect = document.getElementById('cafeSelect');
        const poiSelect = document.getElementById('poiSelect');
        const statusEl = document.getElementById('status');
        let allData = null;
        let layer = null;
        const markerLayer = L.layerGroup().addTo(map);
        const cafeIndex = new Map();
        const partIndex = new Map();
        const partBounds = new Map();
        const gridRows = 4;
        const gridCols = 4;

        function formatLabel(name, lat, lon) {{
            const labelName = name && String(name).trim() ? String(name).trim() : 'Unnamed';
            const latStr = Number.isFinite(lat) ? lat.toFixed(5) : 'n/a';
            const lonStr = Number.isFinite(lon) ? lon.toFixed(5) : 'n/a';
            return `${{labelName}} (${{latStr}}, ${{lonStr}})`;
        }}

        function buildIndex(features) {{
            cafeIndex.clear();
            partIndex.clear();
            partBounds.clear();
            let minLat = Infinity;
            let maxLat = -Infinity;
            let minLon = Infinity;
            let maxLon = -Infinity;
            features.forEach((feat, idx) => {{
                const props = feat && feat.properties ? feat.properties : {{}};
                const cafeName = props.cafe_name || '';
                const cafeLat = Number(props.cafe_lat);
                const cafeLon = Number(props.cafe_lon);
                const cafeId = `${{cafeName}}||${{cafeLat}}||${{cafeLon}}`;
                if (!cafeIndex.has(cafeId)) {{
                    cafeIndex.set(cafeId, {{
                        id: cafeId,
                        name: cafeName,
                        lat: cafeLat,
                        lon: cafeLon,
                        label: formatLabel(cafeName, cafeLat, cafeLon),
                        pois: new Map(),
                        featureIndexes: []
                    }});
                }}
                const cafeEntry = cafeIndex.get(cafeId);
                cafeEntry.featureIndexes.push(idx);

                const poiName = props.poi_name || '';
                const poiType = props.poi_type || '';
                const poiLat = Number(props.poi_lat);
                const poiLon = Number(props.poi_lon);
                const poiId = `${{poiType}}||${{poiName}}||${{poiLat}}||${{poiLon}}`;
                if (!cafeEntry.pois.has(poiId)) {{
                    cafeEntry.pois.set(poiId, {{
                        id: poiId,
                        name: poiName,
                        type: poiType,
                        lat: poiLat,
                        lon: poiLon,
                        label: `${{poiType ? poiType + ': ' : ''}}${{formatLabel(poiName, poiLat, poiLon)}}`,
                        featureIndexes: []
                    }});
                }}
                cafeEntry.pois.get(poiId).featureIndexes.push(idx);

                const geom = feat && feat.geometry ? feat.geometry : null;
                const coords = geom && geom.type === 'LineString' ? geom.coordinates : null;
                if (Array.isArray(coords) && coords.length >= 2) {{
                    const start = coords[0];
                    const end = coords[coords.length - 1];
                    const midLon = (Number(start[0]) + Number(end[0])) / 2;
                    const midLat = (Number(start[1]) + Number(end[1])) / 2;
                    if (Number.isFinite(midLat) && Number.isFinite(midLon)) {{
                        minLat = Math.min(minLat, midLat);
                        maxLat = Math.max(maxLat, midLat);
                        minLon = Math.min(minLon, midLon);
                        maxLon = Math.max(maxLon, midLon);
                    }}
                }}
            }});

            if (!Number.isFinite(minLat) || !Number.isFinite(maxLat) || !Number.isFinite(minLon) || !Number.isFinite(maxLon)) {{
                return;
            }}
            const latSpan = Math.max(1e-6, maxLat - minLat);
            const lonSpan = Math.max(1e-6, maxLon - minLon);
            features.forEach((feat, idx) => {{
                const geom = feat && feat.geometry ? feat.geometry : null;
                const coords = geom && geom.type === 'LineString' ? geom.coordinates : null;
                if (!Array.isArray(coords) || coords.length < 2) {{
                    return;
                }}
                const start = coords[0];
                const end = coords[coords.length - 1];
                const midLon = (Number(start[0]) + Number(end[0])) / 2;
                const midLat = (Number(start[1]) + Number(end[1])) / 2;
                if (!Number.isFinite(midLat) || !Number.isFinite(midLon)) {{
                    return;
                }}
                const row = Math.min(gridRows - 1, Math.max(0, Math.floor(((midLat - minLat) / latSpan) * gridRows)));
                const col = Math.min(gridCols - 1, Math.max(0, Math.floor(((midLon - minLon) / lonSpan) * gridCols)));
                const partId = `${{row}}-${{col}}`;
                if (!partIndex.has(partId)) {{
                    partIndex.set(partId, []);
                }}
                partIndex.get(partId).push(idx);

                const boundsEntry = partBounds.get(partId) || [Infinity, Infinity, -Infinity, -Infinity];
                coords.forEach(pt => {{
                    const lon = Number(pt[0]);
                    const lat = Number(pt[1]);
                    if (!Number.isFinite(lat) || !Number.isFinite(lon)) {{
                        return;
                    }}
                    boundsEntry[0] = Math.min(boundsEntry[0], lon);
                    boundsEntry[1] = Math.min(boundsEntry[1], lat);
                    boundsEntry[2] = Math.max(boundsEntry[2], lon);
                    boundsEntry[3] = Math.max(boundsEntry[3], lat);
                }});
                partBounds.set(partId, boundsEntry);
            }});
        }}

        function setSelectOptions(selectEl, options, placeholder) {{
            selectEl.innerHTML = '';
            const placeholderOption = document.createElement('option');
            placeholderOption.value = '';
            placeholderOption.textContent = placeholder;
            selectEl.appendChild(placeholderOption);
            options.forEach(option => {{
                const opt = document.createElement('option');
                opt.value = option.id;
                opt.textContent = option.label;
                selectEl.appendChild(opt);
            }});
        }}

        function updatePoiOptions() {{
            const cafeId = cafeSelect.value;
            if (!cafeId || !cafeIndex.has(cafeId)) {{
                setSelectOptions(poiSelect, [], 'Select a cafe first');
                poiSelect.disabled = true;
                return;
            }}
            const cafeEntry = cafeIndex.get(cafeId);
            const pois = Array.from(cafeEntry.pois.values()).sort((a, b) => a.label.localeCompare(b.label));
            setSelectOptions(poiSelect, pois, 'All POIs for this cafe');
            poiSelect.disabled = false;
        }}

        function updateAllPartOptions() {{
            const options = [];
            partIndex.forEach((indexes, partId) => {{
                const [row, col] = partId.split('-');
                options.push({{
                    id: partId,
                    label: 'Part ' + (Number(row) + 1) + ',' + (Number(col) + 1) + ' (' + indexes.length + ' paths)'
                }});
            }});
            options.sort((a, b) => a.label.localeCompare(b.label));
            setSelectOptions(allPartSelect, options, 'All paths (slow)');
            if (options.length > 0) {{
                allPartSelect.value = options[0].id;
            }}
        }}

        function applyFilters() {{
            if (!allData) {{
                return;
            }}
            const mode = modeSelect.value;
            let indexes = [];
            let cafeEntry = null;
            let poiEntry = null;
            if (mode === 'all') {{
                const partId = allPartSelect.value;
                if (partId && partIndex.has(partId)) {{
                    indexes = partIndex.get(partId);
                }} else {{
                    indexes = allData.features.map((_, idx) => idx);
                }}
            }} else if (mode === 'cafe') {{
                const cafeId = cafeSelect.value;
                if (cafeId && cafeIndex.has(cafeId)) {{
                    cafeEntry = cafeIndex.get(cafeId);
                    indexes = cafeEntry.featureIndexes;
                }}
            }} else if (mode === 'poi') {{
                const cafeId = cafeSelect.value;
                const poiId = poiSelect.value;
                if (cafeId && cafeIndex.has(cafeId)) {{
                    cafeEntry = cafeIndex.get(cafeId);
                    if (poiId && cafeEntry.pois.has(poiId)) {{
                        poiEntry = cafeEntry.pois.get(poiId);
                        indexes = poiEntry.featureIndexes;
                    }} else {{
                        indexes = cafeEntry.featureIndexes;
                    }}
                }}
            }}

            const filtered = {{
                type: 'FeatureCollection',
                features: indexes.map(i => allData.features[i])
            }};
            if (layer) {{
                map.removeLayer(layer);
            }}
            layer = L.geoJSON(filtered, {{
                style: {{ color: '#1b6ef3', weight: 2, opacity: 0.65 }}
            }}).addTo(map);

            if (filtered.features.length > 0) {{
                map.fitBounds(layer.getBounds(), {{ padding: [24, 24] }});
            }} else if (bounds) {{
                map.fitBounds(bounds);
            }}
            markerLayer.clearLayers();
            if (mode !== 'all' && cafeEntry && Number.isFinite(cafeEntry.lat) && Number.isFinite(cafeEntry.lon)) {{
                L.marker([cafeEntry.lat, cafeEntry.lon])
                    .bindPopup(cafeEntry.label)
                    .addTo(markerLayer);
            }}
            if (mode === 'cafe' && cafeEntry) {{
                cafeEntry.pois.forEach(poi => {{
                    if (Number.isFinite(poi.lat) && Number.isFinite(poi.lon)) {{
                        L.circleMarker([poi.lat, poi.lon], {{
                            radius: 4,
                            color: '#d24b4b',
                            fillColor: '#d24b4b',
                            fillOpacity: 0.85,
                            weight: 1
                        }})
                            .bindPopup(poi.label)
                            .addTo(markerLayer);
                    }}
                }});
            }}
            if (mode === 'poi' && poiEntry && Number.isFinite(poiEntry.lat) && Number.isFinite(poiEntry.lon)) {{
                L.circleMarker([poiEntry.lat, poiEntry.lon], {{
                    radius: 6,
                    color: '#d24b4b',
                    fillColor: '#d24b4b',
                    fillOpacity: 0.9,
                    weight: 2
                }})
                    .bindPopup(poiEntry.label)
                    .addTo(markerLayer);
            }}
            statusEl.textContent = `Showing ${{filtered.features.length}} paths`;
        }}

        function updateModeUI() {{
            const mode = modeSelect.value;
            const cafeEnabled = mode !== 'all';
            cafeSelect.disabled = !cafeEnabled;
            poiSelect.disabled = mode !== 'poi';
            allPartSelect.disabled = mode !== 'all';
            if (mode === 'all') {{
                cafeSelect.value = '';
                poiSelect.value = '';
            }} else if (mode === 'cafe') {{
                poiSelect.value = '';
                updatePoiOptions();
            }} else if (mode === 'poi') {{
                updatePoiOptions();
            }}
            applyFilters();
        }}

        modeSelect.addEventListener('change', updateModeUI);
        allPartSelect.addEventListener('change', applyFilters);
        cafeSelect.addEventListener('change', () => {{
            updatePoiOptions();
            applyFilters();
        }});
        poiSelect.addEventListener('change', applyFilters);

        fetch('{geojson_name}')
            .then(r => r.json())
            .then(data => {{
                allData = data;
                buildIndex(data.features || []);
                const cafes = Array.from(cafeIndex.values()).sort((a, b) => {{
                    const diff = (b.featureIndexes.length || 0) - (a.featureIndexes.length || 0);
                    if (diff !== 0) {{
                        return diff;
                    }}
                    return a.label.localeCompare(b.label);
                }});
                setSelectOptions(cafeSelect, cafes, 'Select a cafe');
                updateAllPartOptions();
                updatePoiOptions();
                updateModeUI();
            }})
            .catch(err => {{
                statusEl.textContent = 'Failed to load GeoJSON. Serve this folder with a local web server.';
                console.error(err);
            }});
    </script>
</body>
</html>
"""


def _build_features_for_cafe(
    cafe_idx: int,
    cafe_row: pd.Series,
    cafe_lat_col: str,
    cafe_lon_col: str,
    datasets: Dict[str, Tuple[pd.DataFrame, str, str]],
    radius_km: float,
    decay_scale_km: float,
    road_net,
) -> Tuple[List[Dict[str, Any]], Dict[str, int], Dict[str, Tuple[int, float]]]:
    try:
        cafe_lat = float(cafe_row[cafe_lat_col])
        cafe_lon = float(cafe_row[cafe_lon_col])
    except Exception:
        return [], {}, {}
    if not math.isfinite(cafe_lat) or not math.isfinite(cafe_lon):
        return [], {}, {}

    cafe_name = _get_name(cafe_row)
    radius_m = float(radius_km) * 1000.0

    features: List[Dict[str, Any]] = []
    counts: Dict[str, int] = {}
    decay_stats: Dict[str, Tuple[int, float]] = {}
    for typ, (df, lat_col, lon_col) in datasets.items():
        if df.empty:
            continue
        lat_arr = df[lat_col].to_numpy(dtype=np.float64, copy=False)
        lon_arr = df[lon_col].to_numpy(dtype=np.float64, copy=False)
        valid_mask = np.isfinite(lat_arr) & np.isfinite(lon_arr)
        if not np.any(valid_mask):
            continue
        valid_idx = np.nonzero(valid_mask)[0]
        dists_km = _haversine_vec_km(cafe_lat, cafe_lon, lat_arr[valid_mask], lon_arr[valid_mask])
        within_mask = dists_km <= radius_km
        if not np.any(within_mask):
            continue
        candidate_idx = valid_idx[within_mask]
        candidate_dists = dists_km[within_mask]
        subset = df.iloc[candidate_idx].copy()
        orig_idx = subset.index.to_numpy()
        subset = subset.reset_index(drop=True)
        network_dist_map: Dict[int, float] = {}
        paths_map: Dict[int, List[Dict[str, float]]] = {}
        if road_net is not None:
            try:
                network_dist_map = _network_distance_map(
                    road_net, cafe_lat, cafe_lon, subset[lat_col], subset[lon_col], radius_m
                )
                paths_map = _network_path_map(
                    road_net, cafe_lat, cafe_lon, subset[lat_col], subset[lon_col], radius_m
                )
            except Exception:
                network_dist_map = {}
                paths_map = {}

        for pos, row in subset.iterrows():
            source_idx = int(orig_idx[pos])
            if typ == "cafes" and source_idx == cafe_idx:
                continue
            try:
                poi_lat = float(row[lat_col])
                poi_lon = float(row[lon_col])
            except Exception:
                continue
            if not math.isfinite(poi_lat) or not math.isfinite(poi_lon):
                continue
            d = network_dist_map.get(pos)
            if d is None:
                d = float(candidate_dists[pos])
            if d > radius_km:
                continue
            decay_val = _decay_weight(d, radius_km, decay_scale_km)
            weight_val = _get_weight(row, typ)
            if weight_val is None:
                try:
                    base_weight = max(0.0, 1.0 - (d / radius_km))
                except Exception:
                    base_weight = 0.0
                try:
                    weight_val = base_weight * math.exp(-float(d) / float(decay_scale_km))
                except Exception:
                    weight_val = base_weight

            poi_name = _get_name(row)
            path_coords = paths_map.get(pos)
            if path_coords:
                line_coords = _path_to_linestring(path_coords)
            else:
                line_coords = _direct_linestring(cafe_lat, cafe_lon, poi_lat, poi_lon)

            if len(line_coords) < 2:
                continue

            features.append(
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "LineString",
                        "coordinates": line_coords,
                    },
                    "properties": {
                        "cafe_name": cafe_name,
                        "cafe_lat": float(cafe_lat),
                        "cafe_lon": float(cafe_lon),
                        "poi_type": typ,
                        "poi_name": poi_name,
                        "poi_lat": float(poi_lat),
                        "poi_lon": float(poi_lon),
                        "distance_km": round(float(d), 4),
                        "weight": round(float(weight_val), 4),
                    },
                }
            )
            counts[typ] = counts.get(typ, 0) + 1
            prev_count, prev_sum = decay_stats.get(typ, (0, 0.0))
            decay_stats[typ] = (prev_count + 1, prev_sum + float(decay_val))
    return features, counts, decay_stats


def _stats_from_features(
    features: List[Dict[str, Any]],
    radius_km: float,
    decay_scale_km: float,
) -> Dict[str, Tuple[int, float]]:
    stats: Dict[str, Tuple[int, float]] = {}
    for feat in features:
        props = feat.get("properties", {}) if isinstance(feat, dict) else {}
        typ = props.get("poi_type")
        if not typ:
            continue
        try:
            d = float(props.get("distance_km"))
        except Exception:
            continue
        if not math.isfinite(d):
            continue
        decay_val = _decay_weight(d, radius_km, decay_scale_km)
        prev_count, prev_sum = stats.get(typ, (0, 0.0))
        stats[typ] = (prev_count + 1, prev_sum + float(decay_val))
    return stats


def _init_worker() -> None:
    global G_ROAD_NET
    if G_ROAD_NET is None:
        G_ROAD_NET = _get_road_network()


def _process_cafe(cafe_idx: int) -> Tuple[int, str, Dict[str, int], Dict[str, Tuple[int, float]], str]:
    assert G_CAFE_DF is not None
    assert G_CAFE_LAT_COL is not None
    assert G_CAFE_LON_COL is not None
    assert G_DATASETS is not None
    assert G_OUTPUT_DIR is not None

    cafe_row = G_CAFE_DF.iloc[cafe_idx]
    cafe_name = _get_name(cafe_row) or ""
    out_path = _cafe_output_path(G_OUTPUT_DIR, cafe_idx, cafe_name)
    if G_RESUME and out_path.exists():
        try:
            obj = json.loads(out_path.read_text(encoding="utf-8"))
            feats = obj.get("features", []) if isinstance(obj, dict) else []
        except Exception:
            feats = []
        decay_stats = _stats_from_features(feats, G_RADIUS_KM, G_DECAY_SCALE_KM)
        return cafe_idx, cafe_name, {}, decay_stats, "skipped"

    features, counts, decay_stats = _build_features_for_cafe(
        cafe_idx,
        cafe_row,
        G_CAFE_LAT_COL,
        G_CAFE_LON_COL,
        G_DATASETS,
        G_RADIUS_KM,
        G_DECAY_SCALE_KM,
        G_ROAD_NET,
    )
    if not features:
        return cafe_idx, cafe_name, counts, decay_stats, "empty"

    collection = {"type": "FeatureCollection", "features": features}
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(collection, fh, ensure_ascii=False)
    return cafe_idx, cafe_name, counts, decay_stats, "written"


def main() -> int:
    parser = argparse.ArgumentParser(description="Export cafe->POI path GeoJSONs")
    parser.add_argument(
        "--input-dir",
        default="/home/rise/projects/SiteX/backend/Data/CSV_Reference/final",
        help="Directory containing the CSV files",
    )
    parser.add_argument(
        "--output-dir",
        default="/home/rise/projects/SiteX/backend/Data/poi_paths_geojson",
        help="Directory to write outputs",
    )
    parser.add_argument("--radius-km", type=float, default=DEFAULT_RADIUS_KM, help="Search radius in kilometers")
    parser.add_argument("--decay-scale-km", type=float, default=DEFAULT_DECAY_SCALE_KM, help="Exponential decay scale in kilometers")
    parser.add_argument("--workers", type=int, default=max(os.cpu_count() - 1, 1), help="Number of worker processes")
    parser.add_argument("--no-resume", action="store_false", dest="resume", help="Disable resume behavior")
    parser.add_argument("--map-base-name", default=None, help="Base name for combined paths + map")
    parser.add_argument(
        "--keep-per-cafe",
        action="store_true",
        help="Keep per-cafe GeoJSON files after combined outputs are written",
    )
    parser.add_argument(
        "--summary-csv",
        default=None,
        help="Write per-cafe category counts and average decay weights to CSV",
    )

    args = parser.parse_args()
    input_dir = Path(args.input_dir).resolve()
    output_dir = Path(args.output_dir).resolve()
    radius_label = f"{args.radius_km:g}_km"
    if not output_dir.name.endswith(f"_{radius_label}"):
        output_dir = output_dir.with_name(f"{output_dir.name}_{radius_label}")
    if not args.map_base_name:
        args.map_base_name = f"poi_paths_geojson_{radius_label}"
    if not args.summary_csv:
        args.summary_csv = f"{args.map_base_name}.csv"
    output_dir.mkdir(parents=True, exist_ok=True)

    cafe_csv = input_dir / "cafe_final.csv"
    if not cafe_csv.exists():
        raise FileNotFoundError(f"Missing cafe CSV: {cafe_csv}")

    datasets: Dict[str, Tuple[pd.DataFrame, str, str]] = {}
    cafe_df, cafe_lat_col, cafe_lon_col = _load_poi_csv(cafe_csv)
    datasets["cafes"] = (cafe_df, cafe_lat_col, cafe_lon_col)

    other_files = {
        "banks": "banks_final.csv",
        "education": "education_final.csv",
        "health": "health_final.csv",
        "other": "other_final.csv",
        "temples": "temples_final.csv",
    }
    for typ, filename in other_files.items():
        path = input_dir / filename
        if not path.exists():
            raise FileNotFoundError(f"Missing CSV: {path}")
        df, lat_col, lon_col = _load_poi_csv(path)
        datasets[typ] = (df, lat_col, lon_col)

    global G_CAFE_DF, G_CAFE_LAT_COL, G_CAFE_LON_COL, G_DATASETS, G_RADIUS_KM, G_DECAY_SCALE_KM, G_OUTPUT_DIR, G_RESUME
    G_CAFE_DF = cafe_df
    G_CAFE_LAT_COL = cafe_lat_col
    G_CAFE_LON_COL = cafe_lon_col
    G_DATASETS = datasets
    G_RADIUS_KM = float(args.radius_km)
    G_DECAY_SCALE_KM = float(args.decay_scale_km)
    G_OUTPUT_DIR = output_dir
    G_RESUME = bool(args.resume)

    total_cafes = int(len(cafe_df))
    category_order = list(datasets.keys())
    summary_rows: List[Dict[str, Any]] = []
    composite_lookup: Dict[Tuple[str, float, float], float] = {}
    category_lookup: Dict[Tuple[str, float, float], str] = {}
    master_min_path = input_dir / "master_cafes_minimal.csv"
    if master_min_path.exists():
        try:
            master_min = pd.read_csv(master_min_path)
            min_lat_col, min_lon_col = _find_lat_lon_cols(master_min)
            name_col = None
            for c in ("name", "Name", "NAME"):
                if c in master_min.columns:
                    name_col = c
                    break
            category_col = None
            for c in ("category", "categoryName", "main_category"):
                if c in master_min.columns:
                    category_col = c
                    break
            if min_lat_col and min_lon_col and name_col:
                for _, row in master_min.iterrows():
                    try:
                        nval = str(row.get(name_col))
                        latv = float(row.get(min_lat_col))
                        lonv = float(row.get(min_lon_col))
                        pscore = float(row.get("poi_composite_score"))
                    except Exception:
                        continue
                    composite_lookup[(nval, round(latv, 6), round(lonv, 6))] = pscore
                    if category_col is not None:
                        try:
                            category_lookup[(nval, round(latv, 6), round(lonv, 6))] = row.get(category_col, "")
                        except Exception:
                            continue
        except Exception:
            composite_lookup = {}
    all_indices = list(range(total_cafes))
    if G_RESUME:
        pending = []
        skipped = 0
        for idx in all_indices:
            cafe_name = _get_name(cafe_df.iloc[idx]) or ""
            out_path = _cafe_output_path(output_dir, idx, cafe_name)
            if out_path.exists():
                skipped += 1
            else:
                pending.append(idx)
        if skipped:
            print(f"Skipping {skipped} cafes with existing output files")
    else:
        pending = all_indices

    work_indices = all_indices if args.summary_csv else pending
    if not work_indices:
        print("No cafes to process; building combined outputs from existing files")
    else:
        workers = max(int(args.workers), 1)
        if workers == 1:
            _init_worker()
            for idx in work_indices:
                cafe_idx, cafe_name, counts, decay_stats, status = _process_cafe(idx)
                print(f"Processing cafe {cafe_idx + 1}/{total_cafes}: {cafe_name} ({status})")
                if counts:
                    counts_str = ", ".join(f"{k}={v}" for k, v in sorted(counts.items()))
                    print(f"  POIs found: {counts_str}")
                else:
                    print("  POIs found: none")
                row = _build_summary_row(
                    cafe_df,
                    cafe_idx,
                    decay_stats,
                    radius_label,
                    category_order,
                    composite_lookup,
                    category_lookup,
                    cafe_lat_col,
                    cafe_lon_col,
                )
                if row:
                    summary_rows.append(row)
        else:
            import multiprocessing as mp

            try:
                ctx = mp.get_context("fork")
            except ValueError:
                ctx = mp.get_context()

            with ctx.Pool(processes=workers, initializer=_init_worker) as pool:
                completed = 0
                for cafe_idx, cafe_name, counts, decay_stats, status in pool.imap_unordered(_process_cafe, work_indices):
                    completed += 1
                    print(f"Processing cafe {cafe_idx + 1}/{total_cafes}: {cafe_name} ({status})")
                    if counts:
                        counts_str = ", ".join(f"{k}={v}" for k, v in sorted(counts.items()))
                        print(f"  POIs found: {counts_str}")
                    else:
                        print("  POIs found: none")
                    print(f"Progress: {completed}/{len(work_indices)} processed")
                    row = _build_summary_row(
                        cafe_df,
                        cafe_idx,
                        decay_stats,
                        radius_label,
                        category_order,
                        composite_lookup,
                        category_lookup,
                        cafe_lat_col,
                        cafe_lon_col,
                    )
                    if row:
                        summary_rows.append(row)
    combined, bounds = _build_combined_paths(output_dir)
    paths_path = output_dir / f"{args.map_base_name}_paths.geojson"
    map_path = output_dir / f"{args.map_base_name}_map.html"

    paths_path.write_text(json.dumps(combined, ensure_ascii=False), encoding="utf-8")
    html = _render_map_html(args.map_base_name, paths_path.name, bounds)
    map_path.write_text(html, encoding="utf-8")

    print(f"Wrote combined paths: {paths_path}")
    print(f"Wrote map: {map_path}")

    if args.summary_csv:
        summary_path = output_dir / args.summary_csv
        headers = [
            "name",
            "lat",
            "lng",
            "category",
        ]
        for cat in category_order:
            headers.append(f"{cat}_count_{radius_label}")
            headers.append(f"{cat}_weight_{radius_label}")
        headers.extend(["cafe_weight", "poi_composite_score"])
        with open(summary_path, "w", encoding="utf-8", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=headers)
            writer.writeheader()
            for row in sorted(summary_rows, key=lambda r: r.get("name", "")):
                writer.writerow({h: row.get(h, "") for h in headers})
        print(f"Wrote summary CSV: {summary_path}")

        final_copy = input_dir / "master_cafe_path_minimal.csv"
        try:
            with open(final_copy, "w", encoding="utf-8", newline="") as fh:
                writer = csv.DictWriter(fh, fieldnames=headers)
                writer.writeheader()
                for row in sorted(summary_rows, key=lambda r: r.get("name", "")):
                    writer.writerow({h: row.get(h, "") for h in headers})
            print(f"Wrote summary CSV copy: {final_copy}")
        except Exception:
            pass

    if not args.keep_per_cafe:
        removed = 0
        for path in _iter_geojson_files(output_dir):
            try:
                path.unlink()
                removed += 1
            except Exception:
                continue
        print(f"Removed {removed} per-cafe GeoJSON files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
