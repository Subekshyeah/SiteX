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
  const [lat, setLat] = useState<number>(27.7172); // Kathmandu
  const [lng, setLng] = useState<number>(85.3240);
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [address, setAddress] = useState("");
  const [sheetOpen, setSheetOpen] = useState(false);
  const [geoDataList, setGeoDataList] = useState<Array<{ id: string; name: string; data: any }>>([]);
  const [showPlaces, setShowPlaces] = useState(false);
  const [geoLoading, setGeoLoading] = useState(false);
  const [selectedFeatureId, setSelectedFeatureId] = useState<string | number | null>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log({ name, email, address, lat, lng });
    alert(`Submitted!\nLat: ${lat}\nLng: ${lng}`);
  };

  useEffect(() => {
    // load geojson files only when the user requests (showPlaces)
    if (!showPlaces) return;
    if (geoDataList.length > 0) return; // already loaded

    const files = ["/data/cafe.geojson"];
    setGeoLoading(true);
    Promise.all(
      files.map((path) =>
        fetch(path)
          .then((r) => {
            if (!r.ok) throw new Error("not found");
            return r.json();
          })
          .then((json) => ({ id: path, name: json.name || path.split("/").pop() || path, data: json }))
          .catch(() => null)
      )
    ).then((results) => {
      const filtered = results.filter(Boolean) as Array<{ id: string; name: string; data: any }>;
      if (filtered.length > 0) setGeoDataList((prev) => [...prev, ...filtered]);
    })
    .finally(() => setGeoLoading(false));
  }, [showPlaces]);

  useEffect(() => {
    if (!showPlaces) {
      // hide selection when user turns off places
      setSelectedFeatureId(null);
    }
  }, [showPlaces]);

  return (
    <div className="min-h-screen flex flex-col md:flex-row bg-gray-50">
      {/* ---------- LEFT SIDE – FORM (desktop) ---------- */}
      <div className="hidden md:block w-full md:w-96 bg-white shadow-lg overflow-y-auto p-8 md:p-10 flex-shrink-0 border-r">
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
          <div className="mx-auto max-w-3xl bg-white rounded-t-xl shadow-xl p-6 h-[70vh] overflow-auto">
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
                <div className="flex items-center gap-3 mt-3">
                  <input
                    id="show-places-toggle-mobile"
                    type="checkbox"
                    checked={showPlaces}
                    onChange={(e) => setShowPlaces(e.target.checked)}
                    className="w-4 h-4 rounded"
                  />
                  <Label htmlFor="show-places-toggle-mobile">Show data points</Label>
                </div>
              </form>
            </CardContent>
          </Card>
          </div>
        </div>
      )}

      {/* Floating toggle button (mobile) */}
      <button
        className="fixed bottom-6 right-4 z-50 md:hidden bg-white rounded-full p-3 shadow-lg border"
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
          <div className="absolute top-4 right-4 z-[9999]">
            <div className="bg-white/90 backdrop-blur-sm rounded-md p-2 shadow max-w-xs">
              <button
                className="px-3 py-1 bg-primary text-white rounded-md"
                onClick={() => setShowPlaces((s) => !s)}
              >
                {showPlaces ? "Close Places" : "Places"}
              </button>
              {showPlaces && (
                <div className="mt-2 max-h-60 overflow-auto">
                  {geoLoading && <div className="text-sm text-muted-foreground p-2">Loading...</div>}
                  {!geoLoading && geoDataList.length === 0 && <div className="text-sm text-muted-foreground p-2">No places loaded</div>}
                  {geoDataList.map((item) => (
                    <div key={item.id} className="mb-2">
                      <div className="text-sm font-semibold">{item.name}</div>
                      <ul className="text-sm">
                        {(item.data?.features || []).map((f: any, idx: number) => {
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
                                  setShowPlaces(false);
                                }}
                              >
                                {label}
                              </button>
                            </li>
                          );
                        })}
                      </ul>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
      </div>
    </div>
  );
}