"use client";

import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import { MapContainer, TileLayer, Marker, Popup, useMapEvents, useMap, GeoJSON } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { ChartRadarLinesOnly } from "@/components/ui/chart-radar-lines-only";
import { MapPin, X } from "lucide-react";
import * as L from "leaflet";

// Coffee cup marker icon (divIcon with inline SVG)
const coffeeIcon = L.divIcon({
  className: "coffee-marker",
  html: `<div style="display:inline-flex;align-items:center;justify-content:center;background:white;border-radius:9999px;padding:4px;box-shadow:0 1px 4px rgba(0,0,0,0.3);border:1px solid rgba(0,0,0,0.08)"><svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#1f2937" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M18 8h1a3 3 0 0 1 0 6h-1"></path><path d="M3 8h13v6a4 4 0 0 1-4 4H7a4 4 0 0 1-4-4V8z"></path></svg></div>`,
  iconSize: [24, 24],
  iconAnchor: [12, 24],
});

// Generic POI icon: small circle with type initial
const poiIcon = (type: string) => {
  const colorMap: Record<string, string> = {
    cafes: '#d97706',
    banks: '#0ea5e9',
    education: '#10b981',
    health: '#ef4444',
    temples: '#7c3aed',
    other: '#64748b',
  };
  const c = colorMap[type] || '#111827';
  return L.divIcon({
    className: 'poi-marker',
    html: `<div style="width:20px;height:20px;border-radius:9999px;background:${c};display:flex;align-items:center;justify-content:center;color:white;font-size:11px;font-weight:600;border:2px solid white">${(type||'?').charAt(0).toUpperCase()}</div>`,
    iconSize: [20, 20],
    iconAnchor: [10, 10],
  });
};

// Fix Leaflet default icons
delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl:
    "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png",
  iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
  shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
});

function MapPicker({
  lat,
  lng,
  setLat,
  setLng,
}: {
  lat: number;
  lng: number;
  setLat: (v: number) => void;
  setLng: (v: number) => void;
}) {
  function MapEvents() {
    useMapEvents({
      click(e) {
        setLat(Number(e.latlng.lat.toFixed(6)));
        setLng(Number(e.latlng.lng.toFixed(6)));
      },
    });
    return null;
  }

  return (
    <>
      <MapEvents />
      {lat && lng && <Marker position={[lat, lng]} />}
    </>
  );
}

// We'll replace MapFeatures with a version that accepts a datasetId and uses per-dataset icons.
function getDatasetIcon(type: string) {
  // common wrapper style
  const wrapperStart = '<div style="display:inline-flex;align-items:center;justify-content:center;background:white;border-radius:9999px;padding:4px;box-shadow:0 1px 4px rgba(0,0,0,0.3);border:1px solid rgba(0,0,0,0.08)">';
  const wrapperEnd = '</div>';
  let svg = '';
  switch (type) {
    case 'cafes':
      svg = '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#92400e" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M18 8h1a3 3 0 0 1 0 6h-1"/><path d="M3 8h13v6a4 4 0 0 1-4 4H7a4 4 0 0 1-4-4V8z"/></svg>';
      break;
    case 'temples':
      svg = '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#6d28d9" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M6 7C9 6 12 3 12 3C12 3 15 6 18 7"/><path d="M8 6.0729V9M8 9C8 9 7 11 4 12H20C17 11 16 9 16 9M6 12V15M6 15C6 15 5 17 2 18H22C19 17 18 15 18 15M5 18V21M19 18V21M12 18V21"/></svg>';
      break;
    case 'banks':
      svg = '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#0ea5e9" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M3 10.5L12 5l9 5.5"/><path d="M4 11v6a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-6"/><path d="M10 16v-4"/><path d="M14 16v-4"/></svg>';
      break;
    case 'education':
      svg = '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#059669" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2l7 4-7 4-7-4 7-4z"/><path d="M5 10v6a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-6"/></svg>';
      break;
    case 'health':
      svg = '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#ef4444" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 7v10"/><path d="M7 12h10"/><path d="M5 3h14v4H5z"/></svg>';
      break;
    default:
      svg = '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#374151" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/></svg>';
  }
  const html = wrapperStart + svg + wrapperEnd;
  return L.divIcon({ className: `${type}-icon`, html, iconSize: [24, 24], iconAnchor: [12, 24] });
}

function MapFeatures({
  geoData,
  selectedFeatureId,
  onFeatureClick,
  datasetId,
}: {
  geoData: any | null;
  selectedFeatureId: string | number | null;
  onFeatureClick: (feature: any, layer: L.Layer) => void;
  datasetId: string;
}) {
  const map = useMap();
  const layerMap = useRef<Record<string | number, L.Layer>>({});

  useEffect(() => {
    if (!geoData) return;
    setTimeout(() => {
      try {
        map.invalidateSize();
      } catch (e) {}
    }, 200);
  }, [geoData, map]);

  useEffect(() => {
    if (!geoData || selectedFeatureId == null) return;
    const layer = layerMap.current[selectedFeatureId as any];
    if (layer) {
      try {
        const latlng = (layer.getLatLng && layer.getLatLng()) || null;
        if (latlng) {
          map.flyTo(latlng, 16, { animate: true });
          layer.openPopup && (layer as any).openPopup();
        } else if ((layer as any).getBounds && (layer as any).getBounds()) {
          map.fitBounds((layer as any).getBounds());
        }
      } catch (e) {}
    }
  }, [selectedFeatureId, geoData, map]);

  if (!geoData) return null;
  const onEachFeature = (feature: any, layer: L.Layer) => {
    const id = feature.id ?? feature.properties?.id ?? feature.properties?.name ?? Math.random().toString(36).slice(2, 9);
    layerMap.current[id] = layer;
    const name = feature.properties?.name || id;
    layer.bindPopup(`<strong>${name}</strong>`);
    layer.on("click", () => onFeatureClick(feature, layer));
  };

  const pointToLayer = (feature: any, latlng: L.LatLng) => {
    // choose an icon based on datasetId
    try {
      return L.marker(latlng, { icon: getDatasetIcon(datasetId) as any });
    } catch (e) {
      return L.marker(latlng, { icon: coffeeIcon as any });
    }
  };

  return <GeoJSON data={geoData} onEachFeature={onEachFeature as any} pointToLayer={pointToLayer as any} />;
}

function MapResizeHandler({ sheetOpen }: { sheetOpen: boolean }) {
  const map = useMap();

  useEffect(() => {
    const handle = () => {
      setTimeout(() => {
        try {
          map.invalidateSize();
        } catch (e) {
          // swallow
        }
      }, 120);
    };

    window.addEventListener("resize", handle);
    window.addEventListener("orientationchange", handle);
    const t0 = setTimeout(() => {
      try {
        map.invalidateSize();
      } catch (e) {}
    }, 200);

    return () => {
      window.removeEventListener("resize", handle);
      window.removeEventListener("orientationchange", handle);
      clearTimeout(t0);
    };
  }, [map]);

  useEffect(() => {
    const t = setTimeout(() => {
      try {
        map.invalidateSize();
      } catch (e) {}
    }, sheetOpen ? 350 : 120);
    return () => clearTimeout(t);
  }, [sheetOpen, map]);

  return null;
}

function MapRefSetter({ mapRef }: { mapRef: React.MutableRefObject<L.Map | null> }) {
  const map = useMap();
  useEffect(() => {
    mapRef.current = map;
    return () => {
      mapRef.current = null;
    };
  }, [map, mapRef]);
  return null;
}

export default function LocationForm() {
  const [lat, setLat] = useState<number>(27.670587); // Kathmandu
  const [lng, setLng] = useState<number>(85.420868);
  const [radiusKm, setRadiusKm] = useState<number>(0.3);
  const [poisData, setPoisData] = useState<any | null>(null);
  const [poisFlat, setPoisFlat] = useState<Array<any>>([]);
  const [poiLoading, setPoiLoading] = useState(false);
  const [lastSubmitted, setLastSubmitted] = useState<{ lat: number; lng: number; at: number } | null>(null);
  const mapRef = useRef<L.Map | null>(null);
  const poiMarkersRef = useRef<Record<string, L.Marker>>({});
  const [expandedPoi, setExpandedPoi] = useState<string | null>(null);
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [address, setAddress] = useState("");
  const [sheetOpen, setSheetOpen] = useState(false);
  const [geoDataList, setGeoDataList] = useState<Array<{ id: string; name: string; data: any }>>([]);
  const DATASETS = [
    { id: 'none', name: 'None', path: '', },
    { id: 'cafes', name: 'Cafes', path: '/data/cafes.geojson' },
    { id: 'temples', name: 'Temples', path: '/data/temples.geojson' },
    { id: 'banks', name: 'Banks', path: '/data/banks.geojson' },
    { id: 'education', name: 'Education', path: '/data/education.geojson' },
    { id: 'health', name: 'Health', path: '/data/health.geojson' },
    { id: 'other', name: 'Other', path: '/data/other.geojson' },
  ];
  const [datasetId, setDatasetId] = useState<string>(DATASETS[0].id);
  const [showPlaces, setShowPlaces] = useState(false);
  const [geoLoading, setGeoLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedFeatureId, setSelectedFeatureId] = useState<string | number | null>(null);
  const [csvRows, setCsvRows] = useState<Array<Record<string, string>> | null>(null);
  const [selectedCsvRow, setSelectedCsvRow] = useState<Record<string, string> | null>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log({ name, email, address, lat, lng });
    setLastSubmitted({ lat, lng, at: Date.now() });
    // also fetch POIs on submit so user sees nearby places immediately
    fetchPois();
  };

  async function fetchPois() {
    setPoiLoading(true);
    try {
      const params = new URLSearchParams({
        lat: String(lat),
        lon: String(lng),
        radius_km: String(radiusKm),
      });
      // call explicit backend URL (use full origin to avoid dev-server proxy returning HTML)
      const url = `http://127.0.0.1:8000/api/v1/pois/?${params.toString()}`;
      const res = await axios.get(url, { timeout: 10000 });
      const data = res.data;
      console.log(data);
      setPoisData(data);
      // Ensure geoDataList contains datasets for all returned POI categories
      try {
        const neededTypes = Object.keys((data.pois || {}));
        const missing = neededTypes.filter((t) => !geoDataList.find((g) => g.id === t));
        if (missing.length > 0) {
          const loaders = missing.map(async (tid) => {
            const ds = DATASETS.find((d) => d.id === tid);
            if (!ds || !ds.path) return null;
            try {
              const r = await fetch(ds.path);
              if (!r.ok) return null;
              const json = await r.json();
              return { id: ds.id, name: ds.name, data: json };
            } catch (e) {
              return null;
            }
          });
          const loaded = (await Promise.all(loaders)).filter(Boolean) as any[];
          if (loaded.length > 0) {
            setGeoDataList((prev) => {
              const map = new Map(prev.map((p) => [p.id, p]));
              for (const l of loaded) map.set(l.id, l);
              return Array.from(map.values());
            });
          }
        }
      } catch (e) {
        // non-fatal
      }
      const flat: any[] = [];
      for (const [type, items] of Object.entries(data.pois || {})) {
        (items as any[]).forEach((it) => flat.push({ ...it, type }));
      }
      // Try to match each POI to a feature in the loaded geoDataList (by dataset id)
      const matchThreshold = 0.0001; // ~11m
      const findGeoFeatureForPoi = (type: string, poi: any) => {
        try {
          const ds = geoDataList.find((g) => g.id === type);
          if (!ds) return null;
          const features = (ds.data?.features || []) as any[];
          // attempt match by name first
          if (poi.name) {
            const byName = features.find((f) => (f.properties?.name || '').toString().trim() === poi.name.toString().trim());
            if (byName) return byName;
          }
          // attempt match by coordinates
          for (const f of features) {
            const coords = f.geometry?.coordinates;
            if (!coords || coords.length < 2) continue;
            const flon = Number(coords[0]);
            const flat = Number(coords[1]);
            if (!Number.isFinite(flon) || !Number.isFinite(flat)) continue;
            if (Math.abs(flat - Number(poi.lat)) <= matchThreshold && Math.abs(flon - Number(poi.lon)) <= matchThreshold) {
              return f;
            }
          }
          return null;
        } catch (e) {
          return null;
        }
      };
      // augment each flat item with matchedFeature when possible
      for (const item of flat) {
        try {
          item.matchedFeature = findGeoFeatureForPoi(item.type, item);
        } catch (e) {
          item.matchedFeature = null;
        }
      }
      // sort by distance
      flat.sort((a, b) => (a.distance_km ?? 0) - (b.distance_km ?? 0));
      setPoisFlat(flat);
      // fly map to center? MapContainer center is controlled by lat/lng already via state
    } catch (e: any) {
      if (axios.isAxiosError(e)) {
        console.error('POIs request failed', e.response?.data ?? e.message);
      } else {
        console.error('Failed to fetch POIs', e);
      }
      setPoisData(null);
      setPoisFlat([]);
    } finally {
      setPoiLoading(false);
    }
  }

  function openPoi(type: string, idx: number, item: any) {
    const key = `${type}-${idx}`;
    const marker = poiMarkersRef.current[key];
    try {
      if (marker && mapRef.current) {
        const latlng = (marker as any).getLatLng();
        mapRef.current.flyTo(latlng, 16, { animate: true });
        (marker as any).openPopup && (marker as any).openPopup();
        return;
      }
    } catch (e) {}
    if (item?.lat && item?.lon) {
      setLat(Number(item.lat));
      setLng(Number(item.lon));
      setTimeout(() => {
        try {
          mapRef.current && mapRef.current.flyTo([Number(item.lat), Number(item.lon)], 16, { animate: true });
        } catch (e) {}
      }, 120);
    }
  }

  // Load selected dataset (prefer geojson files in /data)
  useEffect(() => {
    let mounted = true;
    const ds = DATASETS.find((d) => d.id === datasetId);
    if (!ds) {
      setGeoDataList([]);
      setSelectedFeatureId(null);
      setGeoLoading(false);
      setShowPlaces(false);
      return;
    }

    // special-case: "None" — clear any loaded data and hide places
    if (ds.id === 'none') {
      setGeoDataList([]);
      setSelectedFeatureId(null);
      setShowPlaces(false);
      setGeoLoading(false);
      return;
    }

    setGeoLoading(true);
    fetch(ds.path)
      .then((r) => {
        if (!r.ok) throw new Error('not found');
        return r.json();
      })
      .then((json) => {
        if (!mounted) return;
        setGeoDataList([{ id: ds.id, name: ds.name, data: json }]);
        setSelectedFeatureId(null);
        // auto-show places when a valid dataset is loaded
        setShowPlaces(true);
      })
      .catch(() => {
        if (!mounted) return;
        setGeoDataList([]);
        setShowPlaces(false);
      })
      .finally(() => mounted && setGeoLoading(false));

    return () => {
      mounted = false;
    };
  }, [datasetId]);

  // --- CSV parsing and matching ---
  const parseCsvLine = (line: string) => {
    const out: string[] = [];
    let cur = "";
    let inQuotes = false;
    for (let i = 0; i < line.length; i++) {
      const ch = line[i];
      if (ch === '"') {
        if (inQuotes && i + 1 < line.length && line[i + 1] === '"') {
          // escaped quote
          cur += '"';
          i++;
        } else {
          inQuotes = !inQuotes;
        }
      } else if (ch === ',' && !inQuotes) {
        out.push(cur);
        cur = "";
      } else {
        cur += ch;
      }
    }
    out.push(cur);
    return out;
  };

  const parseCsv = (text: string) => {
    const lines = text.split(/\r?\n/).filter((l) => l.trim().length > 0);
    if (lines.length === 0) return [];
    const headers = parseCsvLine(lines[0]).map((h) => h.trim());
    const rows: Array<Record<string, string>> = [];
    for (let i = 1; i < lines.length; i++) {
      const cols = parseCsvLine(lines[i]);
      if (cols.length === 0) continue;
      const row: Record<string, string> = {};
      for (let j = 0; j < headers.length; j++) {
        row[headers[j]] = (cols[j] ?? "").trim();
      }
      rows.push(row);
    }
    return rows;
  };

  const loadCsvIfNeeded = async () => {
    if (csvRows) return csvRows;
    try {
      const res = await fetch('/data/compact_summary_images.csv');
      if (!res.ok) return null;
      const txt = await res.text();
      const parsed = parseCsv(txt);
      setCsvRows(parsed);
      return parsed;
    } catch (e) {
      return null;
    }
  };

  const findNearestRow = (lat: number, lng: number, rows: Array<Record<string, string>> | null) => {
    if (!rows || rows.length === 0) return null;
    let best: Record<string, string> | null = null;
    let bestDist = Infinity;
    for (const r of rows) {
      const rl = parseFloat((r['lat'] ?? r['Lat'] ?? '').toString());
      const rln = parseFloat((r['lng'] ?? r['Lng'] ?? r['lon'] ?? '').toString());
      if (Number.isFinite(rl) && Number.isFinite(rln)) {
        const dx = rl - lat;
        const dy = rln - lng;
        const dist = dx * dx + dy * dy; // squared degrees
        if (dist < bestDist) {
          bestDist = dist;
          best = r;
        }
      }
    }
    // threshold: within ~0.0005 degrees (~50m) squared -> 2.5e-7
    if (best && bestDist < 0.0005 * 0.0005) return best;
    return null;
  };

  // watch lat/lng and try to find CSV row
  useEffect(() => {
    let mounted = true;
    // find nearest feature in loaded geoDataList for the selected dataset
    (async () => {
      try {
        if (!geoDataList || geoDataList.length === 0) {
          setSelectedCsvRow(null);
          return;
        }
        const ds = geoDataList.find((g) => g.id === datasetId) || geoDataList[0];
        const features = (ds.data?.features || []) as any[];
        let best: any = null;
        let bestDist = Infinity;
        for (const f of features) {
          const coords = f.geometry?.coordinates;
          if (!coords || coords.length < 2) continue;
          const fx = parseFloat(coords[1]);
          const fy = parseFloat(coords[0]);
          if (!Number.isFinite(fx) || !Number.isFinite(fy)) continue;
          const dx = fx - lat;
          const dy = fy - lng;
          const dist = dx * dx + dy * dy;
          if (dist < bestDist) {
            bestDist = dist;
            best = f;
          }
        }
        if (best && bestDist < 0.0005 * 0.0005) setSelectedCsvRow(best.properties || null);
        else setSelectedCsvRow(null);
      } catch (e) {
        setSelectedCsvRow(null);
      }
    })();
    return () => {
      mounted = false;
    };
  }, [lat, lng]);

  useEffect(() => {
    if (!showPlaces) {
      // hide selection when user turns off places
      setSelectedFeatureId(null);
    }
  }, [showPlaces]);

  return (
    <div className="min-h-screen flex flex-col md:flex-row bg-gray-50">
      {/* ---------- LEFT SIDE – FORM (desktop) ---------- */}
      <div className="hidden md:block w-full md:w-96 liquid-glass shadow-lg overflow-y-auto p-8 md:p-10 flex-shrink-0 border-r">
        <Card className="border-0 shadow-none">
          <CardHeader className="pb-4">
            <CardTitle className="flex items-center gap-3 text-2xl font-semibold">
              <MapPin className="w-6 h-6" />
              Location Analysis
            </CardTitle>
          </CardHeader>

          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-6">
              <div>
                <Label htmlFor="name">Cafe Name</Label>
                <Input
                  id="name"
                  placeholder="Napang Chussa Tonewa"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  required
                  className="mt-1"
                />
              </div>

              {/* <div>
                <Label htmlFor="email">Email</Label>
                <Input
                  id="email"
                  type="email"
                  placeholder="john@example.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  className="mt-1"
                />
              </div> */}

        

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="lat">Latitude</Label>
                  <Input
                    id="lat"
                    value={lat.toFixed(6)}
                    readOnly
                    className="mt-1 bg-muted font-mono text-sm"
                  />
                </div>
                <div>
                  <Label htmlFor="lng">Longitude</Label>
                  <Input
                    id="lng"
                    value={lng.toFixed(6)}
                    readOnly
                    className="mt-1 bg-muted font-mono text-sm"
                  />
                </div>
              </div>

              <div>
                <Label htmlFor="radius">Radius (km)</Label>
                <Input
                  id="radius"
                  type="number"
                  value={radiusKm}
                  onChange={(e) => setRadiusKm(Number(e.target.value) || 0)}
                  step="0.1"
                  className="mt-1 w-full"
                />
              </div>

              <div className="space-y-2">
                <Button type="submit" className="w-full py-3">
                  Submit Location
                </Button>
              </div>
              <div>
                <Label htmlFor="dataset">Dataset</Label>
                <select
                  id="dataset"
                  value={datasetId}
                  onChange={(e) => setDatasetId(e.target.value)}
                  className="mt-1 w-full px-2 py-1 rounded border text-sm"
                >
                  {DATASETS.map((d) => (
                    <option key={d.id} value={d.id}>{d.name}</option>
                  ))}
                </select>
              </div>
              <div className="flex items-center gap-3 mt-3">
                <input
                  id="show-places-toggle-desktop"
                  type="checkbox"
                  checked={showPlaces}
                  onChange={(e) => setShowPlaces(e.target.checked)}
                  className="w-4 h-4 rounded"
                />
                <Label htmlFor="show-places-toggle-desktop">Show data points</Label>
              </div>
            </form>
          </CardContent>
        </Card>
        <ChartRadarLinesOnly/>
      </div>

      {/* ---------- MOBILE BOTTOM SHEET ---------- */}
      {/* Backdrop */}
      {sheetOpen && (
        <div
          className="fixed inset-0 bg-black/40 z-40 md:hidden"
          onClick={() => setSheetOpen(false)}
          aria-hidden
        />
      )}

      {sheetOpen && (
        <div
          className={
            "fixed inset-x-0 bottom-0 z-50 md:hidden transform transition-transform duration-300 translate-y-0"
          }
          aria-hidden={!sheetOpen}
        >
          <div className="mx-auto max-w-3xl liquid-glass rounded-t-xl shadow-xl p-6 h-[70vh] overflow-auto">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-3 text-lg font-semibold">
              <MapPin className="w-5 h-5" />
              Location Analysis
            </div>
            <button
              className="rounded-md p-2 hover:bg-gray-100"
              onClick={() => setSheetOpen(false)}
              aria-label="Close"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          <Card className="border-0 shadow-none">
            <CardContent>
              <form onSubmit={handleSubmit} className="space-y-6">
                <div>
                  <Label htmlFor="name">Cafe Name</Label>
                  <Input
                    id="name"
                    placeholder="Napang Chussa Tonewa"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    required
                    className="mt-1"
                  />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="lat">Latitude</Label>
                    <Input
                      id="lat"
                      value={lat.toFixed(6)}
                      readOnly
                      className="mt-1 bg-muted font-mono text-sm"
                    />
                  </div>
                  <div>
                    <Label htmlFor="lng">Longitude</Label>
                    <Input
                      id="lng"
                      value={lng.toFixed(6)}
                      readOnly
                      className="mt-1 bg-muted font-mono text-sm"
                    />
                  </div>
                </div>

                <div>
                  <Label htmlFor="radius-mobile">Radius (km)</Label>
                  <Input
                    id="radius-mobile"
                    type="number"
                    value={radiusKm}
                    onChange={(e) => setRadiusKm(Number(e.target.value) || 0)}
                    step="0.1"
                    className="mt-1 w-full"
                  />
                </div>

                <div className="space-y-2">
                  <Button type="submit" className="w-full py-3">
                    Submit Location
                  </Button>
                </div>
                <div>
                  <Label htmlFor="dataset-mobile">Dataset</Label>
                  <select
                    id="dataset-mobile"
                    value={datasetId}
                    onChange={(e) => setDatasetId(e.target.value)}
                    className="mt-1 w-full px-2 py-1 rounded border text-sm"
                  >
                    {DATASETS.map((d) => (
                      <option key={d.id} value={d.id}>{d.name}</option>
                    ))}
                  </select>
                </div>
                
              </form>
            </CardContent>
          </Card>
          </div>
        </div>
      )}

      {/* Floating toggle button (mobile) */}
      <button
        className="fixed bottom-6 right-4 z-50 md:hidden liquid-btn rounded-full p-3 shadow-lg border"
        onClick={() => setSheetOpen(true)}
        aria-label="Open location form"
        title="Open location form"
      >
        <MapPin className="w-5 h-5 text-slate-700" />
      </button>

      {/* ---------- RIGHT SIDE – FULL-SCREEN MAP ---------- */}
      <div className="flex-1 relative min-h-[480px] bg-transparent z-100">
        <MapContainer center={[lat, lng]} zoom={13} className="h-full w-full bg-transparent" scrollWheelZoom>
          <TileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            attribution='&copy; <a href="https://osm.org/copyright">OpenStreetMap</a>'
          />
            <MapRefSetter mapRef={mapRef} />
            <MapPicker lat={lat} lng={lng} setLat={setLat} setLng={setLng} />
            {showPlaces && geoDataList.map((item) => (
              <MapFeatures
                key={item.id}
                datasetId={item.id}
                geoData={item.data}
                selectedFeatureId={selectedFeatureId}
                onFeatureClick={(feature, layer) => {
                  try {
                    const coords = feature.geometry.type === "Point" ? feature.geometry.coordinates : feature.geometry.coordinates[0];
                    setLat(coords[1]);
                    setLng(coords[0]);
                  } catch (e) {}
                  setSelectedFeatureId(feature.properties?.name ?? feature.id ?? null);
                }}
              />
            ))}
            {/* POI markers from augmented poisFlat grouped by category (keeps index in sync with panel) */}
            {Object.entries(poisFlat.reduce((acc: Record<string, any[]>, p: any) => { (acc[p.type] = acc[p.type] || []).push(p); return acc; }, {})).map(([type, items]: any) => (
              (items as any[]).map((p: any, idx: number) => {
                const key = `${type}-${idx}`;
                return (
                  <Marker
                    key={key}
                    position={[Number(p.lat), Number(p.lon)]}
                    icon={poiIcon(type)}
                    ref={(r) => {
                      try {
                        if (r) poiMarkersRef.current[key] = (r as unknown) as L.Marker;
                        else delete poiMarkersRef.current[key];
                      } catch (e) {}
                    }}
                  >
                    <Popup>
                      <div className="text-sm">
                        <div style={{ fontWeight: 600 }}>{p.name ?? 'Unnamed'}</div>
                        <div className="text-xs">{type} — {p.distance_km ?? ''} km</div>
                      </div>
                    </Popup>
                  </Marker>
                );
              })
            ))}
          </MapContainer>

          {/* Places panel (toggle) */}
          {showPlaces && (
              <div className="absolute top-4 right-4 z-[9999]">
                <div className="liquid-glass rounded-md p-2 max-w-xs">
                <div className="px-2 pb-2">
                  <input
                    type="search"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    placeholder="Search places..."
                    className="w-full px-2 py-1 rounded border text-sm"
                  />
                </div>
                <div className="mt-2 max-h-60 overflow-auto">
                  {geoLoading && <div className="text-sm text-muted-foreground p-2">Loading...</div>}
                  {!geoLoading && geoDataList.length === 0 && <div className="text-sm text-muted-foreground p-2">No places loaded</div>}
                  {geoDataList.map((item) => {
                    const features = (item.data?.features || []) as any[];
                    const q = searchQuery.trim().toLowerCase();
                    const hasQuery = q.length > 0;
                    const filtered = hasQuery
                      ? features.filter((f) => {
                          const label = (f.properties?.name ?? '').toString().toLowerCase();
                          return label.includes(q) || item.name.toLowerCase().includes(q);
                        })
                      : features;

                    if (filtered.length === 0) return null;

                    return (
                      <div key={item.id} className="mb-2">
                        <div className="text-sm font-semibold">{item.name}</div>
                        <ul className="text-sm">
                          {filtered.map((f: any, idx: number) => {
                            const fid = f.id ?? f.properties?.id ?? f.properties?.name ?? `${item.id}-${idx}`;
                            const label = f.properties?.name ?? fid;
                            return (
                              <li key={fid} className="py-1">
                                <button
                                  className="text-left w-full text-slate-700 hover:underline"
                                  onClick={() => {
                                    try {
                                      const coords = f.geometry.type === "Point" ? f.geometry.coordinates : f.geometry.coordinates[0];
                                      setLat(coords[1]);
                                      setLng(coords[0]);
                                    } catch (e) {}
                                    setSelectedFeatureId(f.properties?.name ?? f.id ?? fid);
                                  }}
                                >
                                  {label}
                                </button>
                              </li>
                            );
                          })}
                        </ul>
                      </div>
                    );
                  })}
                </div>
              </div>
            </div>
          )}
          {/* POIs concise panel */}
          {poisData && (
            <div className="absolute bottom-4 right-4 z-[9999]">
              <div className="liquid-glass rounded-md p-3 w-72">
                <div className="flex items-start justify-between">
                  <div>
                    <div className="text-sm text-muted-foreground">Center</div>
                    <div className="font-mono text-sm">{Number(poisData?.center?.lat ?? lat).toFixed(6)}</div>
                    <div className="font-mono text-sm">{Number(poisData?.center?.lon ?? lng).toFixed(6)}</div>
                  </div>
                  <div className="text-right">
                    <div className="text-sm text-muted-foreground">Radius</div>
                    <div className="font-semibold">{(poisData.radius_km ?? radiusKm)} km</div>
                  </div>
                </div>

                <div className="mt-2 text-sm">
                  <div className="font-semibold">Categories</div>
                  <div className="mt-1">
                    {Object.entries(poisData.pois || {}).map(([k, v]: any) => (
                      <div key={k} className="text-xs">{k}: {(v as any[]).length}</div>
                    ))}
                  </div>
                </div>

                <div className="mt-2">
                  <div className="text-sm font-semibold">Nearby by Category</div>
                  <div className="mt-1 max-h-48 overflow-auto text-xs">
                    {
                      // build grouped map from augmented flat list so we can access matchedFeature
                      Object.entries(poisFlat.reduce((acc: Record<string, any[]>, p: any) => {
                        (acc[p.type] = acc[p.type] || []).push(p);
                        return acc;
                      }, {})).map(([cat, items]: any) => (
                        <div key={cat} className="mb-2">
                          <div className="font-medium">{cat} <span className="text-muted-foreground">({(items as any[]).length})</span></div>
                          <ul className="mt-1">
                            {(items as any[]).slice(0, 5).map((it: any, idx: number) => (
                              <li key={`${cat}-${idx}`} className="py-0.5">
                                <div className="flex items-start justify-between gap-2">
                                  <button
                                    className="text-left w-full hover:underline"
                                    onClick={() => { openPoi(cat, idx, it); }}
                                  >
                                    {it.name ?? 'Unnamed'} <span className="text-muted-foreground">— {it.distance_km} km</span>
                                  </button>
                                  <button
                                    className="text-xs text-slate-500 hover:underline"
                                    onClick={() => setExpandedPoi(expandedPoi === `${cat}-${idx}` ? null : `${cat}-${idx}`)}
                                  >
                                    details
                                  </button>
                                </div>
                                {expandedPoi === `${cat}-${idx}` && (
                                  <div className="mt-1 text-[11px] text-slate-700 bg-white/5 p-2 rounded">
                                    {it.matchedFeature ? (
                                      <div>
                                        {Object.entries(it.matchedFeature.properties || {}).map(([k, v]: any) => (
                                          <div key={k}><strong>{k}</strong>: {String(v)}</div>
                                        ))}
                                      </div>
                                    ) : (
                                      <div className="text-muted-foreground">No matching dataset feature found.</div>
                                    )}
                                  </div>
                                )}
                              </li>
                            ))}
                            {(items as any[]).length === 0 && <li className="text-muted-foreground">No items</li>}
                          </ul>
                        </div>
                      ))
                    }
                  </div>
                </div>
              </div>
            </div>
          )}
          {/* CSV info overlay for matched location */}
          {selectedCsvRow && (
            <div className="absolute bottom-6 left-4 z-[9999]">
              <div
                className="w-80 h-44 rounded-lg overflow-hidden shadow-lg text-white"
                style={{
                  backgroundSize: 'cover',
                  backgroundPosition: 'center',
                  backgroundImage: selectedCsvRow['imageUrl'] ? `url(${selectedCsvRow['imageUrl']})` : undefined,
                }}
              >
                <div className="w-full h-full bg-black/30 p-3 flex flex-col justify-end">
                  <div className="text-lg font-bold leading-tight">{selectedCsvRow['name'] || selectedCsvRow['place_id'] || 'Place'}</div>
                  <div className="text-sm mt-1">{selectedCsvRow['address']}</div>
                  <div className="flex items-center justify-between mt-2">
                    <div className="text-sm">{selectedCsvRow['phone'] ? selectedCsvRow['phone'] : ''}</div>
                    {selectedCsvRow['url'] && (
                      <a
                        href={selectedCsvRow['url']}
                        target="_blank"
                        rel="noreferrer"
                        className="text-xs bg-white/20 px-2 py-1 rounded-md hover:bg-white/30"
                      >
                        Open in Maps
                      </a>
                    )}
                  </div>
                </div>
              </div>
            </div>
          )}
      </div>
    </div>
  );
}