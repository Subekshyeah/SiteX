"use client";

import React, { useState, useEffect, useRef } from "react";
import { MapContainer, TileLayer, Marker, useMapEvents, useMap, GeoJSON } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { MapPin, X } from "lucide-react";
import * as L from "leaflet";

// Coffee cup marker icon (divIcon with inline SVG)
const coffeeIcon = L.divIcon({
  className: "coffee-marker",
  html: `<div style="display:inline-flex;align-items:center;justify-content:center;background:white;border-radius:9999px;padding:4px;box-shadow:0 1px 4px rgba(0,0,0,0.3);border:1px solid rgba(0,0,0,0.08)"><svg xmlns=\"http://www.w3.org/2000/svg\" width=\"18\" height=\"18\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"#1f2937\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M18 8h1a3 3 0 0 1 0 6h-1\"></path><path d=\"M3 8h13v6a4 4 0 0 1-4 4H7a4 4 0 0 1-4-4V8z\"></path></svg></div>`,
  iconSize: [24, 24],
  iconAnchor: [12, 24],
});

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

function MapFeatures({
  geoData,
  selectedFeatureId,
  onFeatureClick,
}: {
  geoData: any | null;
  selectedFeatureId: string | number | null;
  onFeatureClick: (feature: any, layer: L.Layer) => void;
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
        // if marker-like
        // @ts-ignore
        const latlng = (layer.getLatLng && layer.getLatLng()) || null;
        if (latlng) {
          map.flyTo(latlng, 16, { animate: true });
          // @ts-ignore
          layer.openPopup && layer.openPopup();
        } else if ((layer as any).getBounds && (layer as any).getBounds()) {
          // @ts-ignore
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
    // render point features as coffee icons
    return L.marker(latlng, { icon: coffeeIcon as any });
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

export default function LocationForm() {
  const [lat, setLat] = useState<number>(27.670587); // Kathmandu
  const [lng, setLng] = useState<number>(85.420868);
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [address, setAddress] = useState("");
  const [sheetOpen, setSheetOpen] = useState(false);
  const [geoDataList, setGeoDataList] = useState<Array<{ id: string; name: string; data: any }>>([]);
  const DATASETS = [
    { id: 'none', name: 'None', path: '' },
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
    alert(`Submitted!\nLat: ${lat}\nLng: ${lng}`);
  };

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

              <Button type="submit" className="w-full py-3">
                Submit Location
              </Button>
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

                <Button type="submit" className="w-full py-3">
                  Submit Location
                </Button>
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
            <MapPicker lat={lat} lng={lng} setLat={setLat} setLng={setLng} />
            {showPlaces && geoDataList.map((item) => (
              <MapFeatures
                key={item.id}
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