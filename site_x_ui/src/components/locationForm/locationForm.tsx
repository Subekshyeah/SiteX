"use client";

import React, { useState, useEffect, useRef, useMemo } from "react";
import axios from "axios";
import { MapContainer, TileLayer, Marker, useMapEvents, useMap, GeoJSON } from "react-leaflet";
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
    html: `<div style="width:20px;height:20px;border-radius:9999px;background:${c};display:flex;align-items:center;justify-content:center;color:white;font-size:11px;font-weight:600;border:2px solid white">${(type || '?').charAt(0).toUpperCase()}</div>`,
    iconSize: [20, 20],
    iconAnchor: [10, 10],
  });
};

// color helper used for selected marker styling
function getColorForType(type?: string) {
  const colorMap: Record<string, string> = {
    cafes: '#d97706',
    banks: '#0ea5e9',
    education: '#10b981',
    health: '#ef4444',
    temples: '#7c3aed',
    other: '#64748b',
  };
  return (type && colorMap[type]) || '#111827';
}

// selected POI icon: outer ring + inner colored circle
const selectedPoiIcon = (type?: string) => {
  const c = getColorForType(type);
  const html = `
    <div style="display:flex;align-items:center;justify-content:center;">
      <div style="width:36px;height:36px;border-radius:9999px;background:rgba(255,255,255,0.9);display:flex;align-items:center;justify-content:center;border:3px solid ${c};box-shadow:0 4px 10px rgba(0,0,0,0.15)">
        <div style="width:18px;height:18px;border-radius:9999px;background:${c};display:flex;align-items:center;justify-content:center;color:white;font-size:11px;font-weight:700;border:2px solid white">${(type || '?').charAt(0).toUpperCase()}</div>
      </div>
    </div>
  `;
  return L.divIcon({ className: 'poi-selected-marker', html, iconSize: [36, 36], iconAnchor: [18, 36] });
};

const DEFAULT_TOLET_POINTS: Array<{ lat: number; lng: number }> = [
  { lat: 27.670535, lng: 85.424404 },
  { lat: 27.672540, lng: 85.429875 },
  { lat: 27.672980, lng: 85.431220 },
  { lat: 27.671420, lng: 85.428640 },
  { lat: 27.673610, lng: 85.426980 },
  { lat: 27.669980, lng: 85.430540 },
  { lat: 27.670820, lng: 85.432180 },
  { lat: 27.671860, lng: 85.425960 },
];

const MAP_BOUNDS_SW = L.latLng(27.6164, 85.3459);
const MAP_BOUNDS_NE = L.latLng(27.7536, 85.4841);
const MAP_BOUNDS = L.latLngBounds(MAP_BOUNDS_SW, MAP_BOUNDS_NE);

function clampToBounds(lat: number, lng: number) {
  const clampedLat = Math.min(MAP_BOUNDS_NE.lat, Math.max(MAP_BOUNDS_SW.lat, lat));
  const clampedLng = Math.min(MAP_BOUNDS_NE.lng, Math.max(MAP_BOUNDS_SW.lng, lng));
  return { lat: clampedLat, lng: clampedLng };
}

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
  onPick,
}: {
  lat: number;
  lng: number;
  onPick: (lat: number, lng: number) => void;
}) {
  function MapEvents() {
    useMapEvents({
      click(e) {
        const clamped = clampToBounds(e.latlng.lat, e.latlng.lng);
        onPick(Number(clamped.lat.toFixed(6)), Number(clamped.lng.toFixed(6)));
      },
    });
    return null;
  }
  return (
    <>
      <MapEvents />
      {Number.isFinite(lat) && Number.isFinite(lng) && <Marker position={[lat, lng]} />}
    </>
  );
}

const pointPickIcon = L.divIcon({
  className: "point-pick-marker",
  html: `<div style="width:18px;height:18px;border-radius:9999px;background:#2563eb;border:2px solid white;box-shadow:0 2px 6px rgba(0,0,0,0.2)"></div>`,
  iconSize: [18, 18],
  iconAnchor: [9, 9],
});

const toLetPickIcon = L.divIcon({
  className: "tolet-pick-marker",
  html: `<div style="width:18px;height:18px;border-radius:9999px;background:#16a34a;border:2px solid white;box-shadow:0 2px 6px rgba(0,0,0,0.2)"></div>`,
  iconSize: [18, 18],
  iconAnchor: [9, 9],
});

const toLetHoverIcon = L.divIcon({
  className: "tolet-hover-marker",
  html: `<div style="width:18px;height:18px;border-radius:9999px;background:rgba(22,163,74,0.5);border:2px dashed #16a34a;box-shadow:0 2px 6px rgba(0,0,0,0.15)"></div>`,
  iconSize: [18, 18],
  iconAnchor: [9, 9],
});

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
      } catch (e) { }
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
          // layer.openPopup && (layer as any).openPopup();
        } else if ((layer as any).getBounds && (layer as any).getBounds()) {
          map.fitBounds((layer as any).getBounds());
        }
      } catch (e) { }
    }
  }, [selectedFeatureId, geoData, map]);

  if (!geoData) return null;
  const onEachFeature = (feature: any, layer: L.Layer) => {
    const id = feature.id ?? feature.properties?.id ?? feature.properties?.name ?? Math.random().toString(36).slice(2, 9);
    layerMap.current[id] = layer;
    const name = feature.properties?.name || id;
    // layer.bindPopup(`<strong>${name}</strong>`);
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
      } catch (e) { }
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
      } catch (e) { }
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
  const [lat, setLat] = useState<number>(27.670587);
  const [lng, setLng] = useState<number>(85.420868);
  const [analysisMode, setAnalysisMode] = useState<"point" | "tolet">("point");
  const [pointList, setPointList] = useState<Array<{ lat: number; lng: number }>>([]);
  const [toLetList, setToLetList] = useState<Array<{ lat: number; lng: number }>>(DEFAULT_TOLET_POINTS);
  const [toLetSelected, setToLetSelected] = useState<Record<string, boolean>>({});
  const [pointSelected, setPointSelected] = useState<Record<string, boolean>>({});
  const [hoverToLet, setHoverToLet] = useState<{ lat: number; lng: number } | null>(null);
  const [radiusKm, setRadiusKm] = useState<number>(0.5);
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
    { id: 'all', name: 'All', path: '' },
    { id: 'cafes', name: 'Cafes', path: '/data/cafes.geojson' },
    { id: 'temples', name: 'Temples', path: '/data/temples.geojson' },
    { id: 'banks', name: 'Banks', path: '/data/banks.geojson' },
    { id: 'education', name: 'Education', path: '/data/education.geojson' },
    { id: 'health', name: 'Health', path: '/data/health.geojson' },
    { id: 'other', name: 'Other', path: '/data/other.geojson' },
  ];
  const [datasetId, setDatasetId] = useState<string>(DATASETS[0].id);
  const [showPlaces, setShowPlaces] = useState(false);
  const [showWithinRadius, setShowWithinRadius] = useState(true);
  const [geoLoading, setGeoLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedFeatureId, setSelectedFeatureId] = useState<string | number | null>(null);
  const [poiLat, setPoiLat] = useState<number>(0);
  const [poiLng, setPoiLng] = useState<number>(0);
  const [hoverTempPoiLat, setHoverTempPoiLat] = useState<number>(0);
  const [hoverTempPoiLng, setHoverTempPoiLng] = useState<number>(0);
  const [csvRows, setCsvRows] = useState<Array<Record<string, string>> | null>(null);
  const [selectedCsvRow, setSelectedCsvRow] = useState<Record<string, string> | null>(null);
  const [overlayImageFailed, setOverlayImageFailed] = useState<boolean>(false);

  useEffect(() => {
    // reset image failure state when selected row changes
    setOverlayImageFailed(false);
  }, [selectedCsvRow]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log({ name, email, address, lat, lng });

    const activeList = analysisMode === "point"
      ? (selectedPointList.length > 0 ? selectedPointList : pointList)
      : selectedToLetList;
    if (analysisMode === "tolet" && activeList.length === 0) {
      alert("Select at least one to-let location.");
      return;
    }
    const list = activeList.length > 0 ? activeList : [{ lat, lng }];
    const listForSubmit: Array<{ lat: number; lng: number }> = list;
    const primary = listForSubmit[0] || { lat, lng };
    setLastSubmitted({ lat: primary.lat, lng: primary.lng, at: Date.now() });

    const pointsParam = listForSubmit
      .map((p: { lat: number; lng: number }) => `${Number(p.lat).toFixed(6)},${Number(p.lng).toFixed(6)}`)
      .join(";");

    // navigate to React result route (reads query params)
    const params = new URLSearchParams({
      name: String(name || ""),
      mode: analysisMode,
      pick: "multiple",
      lat: String(primary.lat),
      lng: String(primary.lng),
    });
    if (pointsParam) params.set("points", pointsParam);
    // navigate to /result so SPA can handle it; fallback to result.html if not routed
    try {
      window.location.href = `/result?${params.toString()}`;
    } catch {
      window.location.href = `/result.html?${params.toString()}`;
    }
  };

  const toKey = (p: { lat: number; lng: number }) => `${p.lat.toFixed(6)},${p.lng.toFixed(6)}`;
  const mergeUniquePoints = (base: Array<{ lat: number; lng: number }>, incoming: Array<{ lat: number; lng: number }>) => {
    const next = [...base];
    for (const p of incoming) {
      const exists = next.some((it) => Math.abs(it.lat - p.lat) < 1e-6 && Math.abs(it.lng - p.lng) < 1e-6);
      if (!exists) next.push(p);
    }
    return next;
  };

  useEffect(() => {
    try {
      const savedPointList = window.localStorage.getItem("siteX.pointList");
      const savedPointSelected = window.localStorage.getItem("siteX.pointSelected");
      const savedToLetList = window.localStorage.getItem("siteX.toLetList");
      const savedToLetSelected = window.localStorage.getItem("siteX.toLetSelected");

      if (savedPointList) {
        const parsed = JSON.parse(savedPointList) as Array<{ lat: number; lng: number }>;
        if (Array.isArray(parsed)) setPointList(parsed);
      }
      if (savedPointSelected) {
        const parsed = JSON.parse(savedPointSelected) as Record<string, boolean>;
        if (parsed && typeof parsed === "object") setPointSelected(parsed);
      }
      if (savedToLetList) {
        const parsed = JSON.parse(savedToLetList) as Array<{ lat: number; lng: number }>;
        if (Array.isArray(parsed)) setToLetList(mergeUniquePoints(DEFAULT_TOLET_POINTS, parsed));
      }
      if (savedToLetSelected) {
        const parsed = JSON.parse(savedToLetSelected) as Record<string, boolean>;
        if (parsed && typeof parsed === "object") setToLetSelected(parsed);
      }
    } catch {
      // ignore storage errors
    }
  }, []);

  useEffect(() => {
    try {
      window.localStorage.setItem("siteX.pointList", JSON.stringify(pointList));
      window.localStorage.setItem("siteX.pointSelected", JSON.stringify(pointSelected));
      window.localStorage.setItem("siteX.toLetList", JSON.stringify(toLetList));
      window.localStorage.setItem("siteX.toLetSelected", JSON.stringify(toLetSelected));
    } catch {
      // ignore storage errors
    }
  }, [pointList, pointSelected, toLetList, toLetSelected]);

  const selectedToLetList = useMemo(() => {
    return toLetList.filter((p) => toLetSelected[toKey(p)]);
  }, [toLetList, toLetSelected]);

  const selectedPointList = useMemo(() => {
    return pointList.filter((p) => pointSelected[toKey(p)]);
  }, [pointList, pointSelected]);

  useEffect(() => {
    if (selectedPointList.length === 0) return;
    setToLetList((prev) => mergeUniquePoints(prev, selectedPointList));
    setToLetSelected((prev) => {
      const next = { ...prev };
      for (const p of selectedPointList) next[toKey(p)] = true;
      return next;
    });
  }, [selectedPointList]);

  const mapPickList = useMemo(() => {
    if (analysisMode === "point") {
      return selectedPointList.length > 0 ? selectedPointList : pointList;
    }
    return selectedToLetList;
  }, [analysisMode, pointList, selectedPointList, selectedToLetList]);

  const addPointToActiveList = (p: { lat: number; lng: number }) => {
    setLat(p.lat);
    setLng(p.lng);
    if (analysisMode === "point") {
      setPointList((prev) => {
        const exists = prev.some((it) => Math.abs(it.lat - p.lat) < 1e-6 && Math.abs(it.lng - p.lng) < 1e-6);
        return exists ? prev : [...prev, p];
      });
      setPointSelected((prev) => ({ ...prev, [toKey(p)]: true }));
    } else {
      setToLetList((prev) => {
        const exists = prev.some((it) => Math.abs(it.lat - p.lat) < 1e-6 && Math.abs(it.lng - p.lng) < 1e-6);
        return exists ? prev : [...prev, p];
      });
      setToLetSelected((prev) => ({ ...prev, [toKey(p)]: true }));
    }
  };

  const removeFromPointList = (idx: number) => {
    setPointList((prev) => {
      const next = prev.filter((_, i) => i !== idx);
      return next;
    });
    setPointSelected((prev) => {
      const next = { ...prev };
      const p = pointList[idx];
      if (p) delete next[toKey(p)];
      return next;
    });
  };

  // Haversine distance utility (km)
  const distanceKm = (aLat: number, aLon: number, bLat: number, bLon: number) => {
    const toRad = (v: number) => (v * Math.PI) / 180;
    const R = 6371; // earth radius km
    const dLat = toRad(bLat - aLat);
    const dLon = toRad(bLon - aLon);
    const lat1 = toRad(aLat);
    const lat2 = toRad(bLat);
    const u = Math.sin(dLat / 2) * Math.sin(dLat / 2) + Math.sin(dLon / 2) * Math.sin(dLon / 2) * Math.cos(lat1) * Math.cos(lat2);
    const c = 2 * Math.atan2(Math.sqrt(u), Math.sqrt(1 - u));
    return R * c;
  };

  // return feature count for a dataset id, or null if dataset not loaded
  // This counts features honoring the current `searchQuery` and `showWithinRadius` + radius/center
  const getDatasetCount = (id: string) => {
    try {
      const q = (searchQuery || '').trim().toLowerCase();
      const countForDs = (ds: { id: string; name: string; data: any }) => {
        try {
          const allFeatures = ds.data?.features || [];
          let cnt = 0;
          for (const f of allFeatures) {
            try {
              const name = (f.properties?.name ?? '').toString().toLowerCase();
              if (q && !(name.includes(q) || ds.name.toLowerCase().includes(q))) continue;
              if (showWithinRadius) {
                const coords = f.geometry?.type === 'Point' ? f.geometry.coordinates : (f.geometry?.coordinates && f.geometry.coordinates[0]);
                if (!coords || coords.length < 2) continue;
                const flon = Number(coords[0]);
                const flat = Number(coords[1]);
                if (!Number.isFinite(flon) || !Number.isFinite(flat)) continue;
                const d = distanceKm(lat, lng, flat, flon);
                if (d > radiusKm) continue;
              }
              cnt++;
            } catch {
              continue;
            }
          }
          return cnt;
        } catch {
          return 0;
        }
      };

      // 'all' is a virtual dataset: combine counts from all loaded datasets (except 'all' itself)
      if (id === 'all') {
        let total = 0;
        for (const ds of geoDataList) {
          if (ds.id === 'all') continue;
          total += countForDs(ds);
        }
        return total;
      }

      const ds = geoDataList.find((g) => g.id === id);
      if (!ds) return null;
      return countForDs(ds);
    } catch {
      return null;
    }
  };

  // filtered dataset result based on selected dataset, searchQuery and radius filter
  const filteredGeoData = useMemo(() => {
    try {
      const q = searchQuery.trim().toLowerCase();
      const dsList = datasetId === 'all' ? geoDataList : geoDataList.filter((g) => g.id === datasetId);
      return dsList.map((ds) => {
        const features = (ds.data?.features || []).filter((f: any) => {
          try {
            const name = (f.properties?.name ?? '').toString().toLowerCase();
            if (q && !(name.includes(q) || ds.name.toLowerCase().includes(q))) return false;
            if (showWithinRadius) {
              const coords = f.geometry?.type === 'Point' ? f.geometry.coordinates : (f.geometry?.coordinates && f.geometry.coordinates[0]);
              if (!coords || coords.length < 2) return false;
              const flon = Number(coords[0]);
              const flat = Number(coords[1]);
              if (!Number.isFinite(flon) || !Number.isFinite(flat)) return false;
              const d = distanceKm(lat, lng, flat, flon);
              if (d > radiusKm) return false;
            }
            return true;
          } catch (e) {
            return false;
          }
        });
        return { id: ds.id, name: ds.name, features };
      }).filter((d) => (d.features || []).length > 0);
    } catch (e) {
      return [];
    }
  }, [geoDataList, datasetId, searchQuery, showWithinRadius, lat, lng, radiusKm]);

  // compute counts for the radar chart (6 feature categories) by scanning loaded geoDataList
  const radarCounts = useMemo(() => {
    const ids = ['education', 'cafes', 'temples', 'health', 'banks', 'other'];
    const q = (searchQuery || '').trim().toLowerCase();
    const countFeatures = (ds: any) => {
      try {
        const allFeatures = ds.data?.features || [];
        let cnt = 0;
        for (const f of allFeatures) {
          try {
            const name = (f.properties?.name ?? '').toString().toLowerCase();
            if (q && !(name.includes(q) || ds.name.toLowerCase().includes(q))) continue;
            if (showWithinRadius) {
              const coords = f.geometry?.type === 'Point' ? f.geometry.coordinates : (f.geometry?.coordinates && f.geometry.coordinates[0]);
              if (!coords || coords.length < 2) continue;
              const flon = Number(coords[0]);
              const flat = Number(coords[1]);
              if (!Number.isFinite(flon) || !Number.isFinite(flat)) continue;
              const d = distanceKm(lat, lng, flat, flon);
              if (d > radiusKm) continue;
            }
            cnt++;
          } catch {
            continue;
          }
        }
        return cnt;
      } catch {
        return 0;
      }
    };

    return ids.map((id) => {
      const ds = geoDataList.find((g) => g.id === id);
      return { POI: id.charAt(0).toUpperCase() + id.slice(1), count: ds ? countFeatures(ds) : 0 };
    });
  }, [geoDataList, searchQuery, showWithinRadius, lat, lng, radiusKm]);

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
        // (marker as any).openPopup && (marker as any).openPopup();
        return;
      }
    } catch (e) { }
    if (item?.lat && item?.lon) {
      setPoiLat(Number(item.lat));
      setPoiLng(Number(item.lon));
      setTimeout(() => {
        try {
          mapRef.current && mapRef.current.flyTo([Number(item.lat), Number(item.lon)], 16, { animate: true });
        } catch (e) { }
      }, 120);
    }
  }

  // Load all datasets (prefer geojson files in /data)
  // When `datasetId` changes we eagerly (re)load all category geojsons so
  // the UI can show counts and results immediately for any category.
  useEffect(() => {
    let mounted = true;
    const toLoad = DATASETS.filter((d) => d.path && d.id !== 'all');
    if (toLoad.length === 0) {
      setGeoDataList([]);
      setSelectedFeatureId(null);
      setGeoLoading(false);
      setShowPlaces(false);
      return;
    }

    setGeoLoading(true);
    (async () => {
      try {
        const loaders = toLoad.map(async (ds) => {
          try {
            const r = await fetch(ds.path);
            if (!r.ok) return { id: ds.id, name: ds.name, data: null };
            const json = await r.json();
            return { id: ds.id, name: ds.name, data: json };
          } catch {
            return { id: ds.id, name: ds.name, data: null };
          }
        });
        const results = await Promise.all(loaders);
        if (!mounted) return;
        const loaded = results.filter((r) => r.data);
        // Replace geoDataList with all successfully loaded datasets
        setGeoDataList(loaded.map((l) => ({ id: l.id, name: l.name, data: l.data })));
        setSelectedFeatureId(null);
        setShowPlaces(true);
      } catch {
        if (!mounted) return;
        setGeoDataList([]);
        setShowPlaces(false);
      } finally {
        if (mounted) setGeoLoading(false);
      }
    })();

    return () => { mounted = false; };
  }, [datasetId]);

  // Preload all dataset geojsons on mount and whenever `searchQuery` changes
  useEffect(() => {
    let mounted = true;
    const toLoad = DATASETS.filter((d) => d.path && d.id !== 'all');
    if (toLoad.length === 0) return;
    setGeoLoading(true);
    (async () => {
      try {
        const loaders = toLoad.map(async (ds) => {
          try {
            const r = await fetch(ds.path);
            if (!r.ok) return { id: ds.id, name: ds.name, data: null };
            const json = await r.json();
            return { id: ds.id, name: ds.name, data: json };
          } catch {
            return { id: ds.id, name: ds.name, data: null };
          }
        });
        const results = await Promise.all(loaders);
        if (!mounted) return;
        // keep only loaded datasets that have data
        const loaded = results.filter((r) => r.data);
        setGeoDataList((prev) => {
          const map = new Map(prev.map((p) => [p.id, p]));
          for (const l of loaded) map.set(l.id, l);
          return Array.from(map.values());
        });
      } catch {
        // ignore
      } finally {
        if (mounted) setGeoLoading(false);
      }
    })();
    return () => { mounted = false; };
    // load on mount and whenever the search changes so counts update quickly
  }, [searchQuery]);

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
          const dx = fx - poiLat;
          const dy = fy - poiLng;
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
  }, [poiLat, poiLng]);

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

              <div className="space-y-2">
                <Label>Analysis Mode</Label>
                <div className="flex gap-2">
                  <button
                    type="button"
                    onClick={() => setAnalysisMode("point")}
                    className={`px-3 py-1 rounded text-sm border ${analysisMode === "point" ? "bg-slate-900 text-white" : "bg-white text-slate-700"}`}
                  >
                    Point pick
                  </button>
                  <button
                    type="button"
                    onClick={() => setAnalysisMode("tolet")}
                    className={`px-3 py-1 rounded text-sm border ${analysisMode === "tolet" ? "bg-slate-900 text-white" : "bg-white text-slate-700"}`}
                  >
                    To-let pick
                  </button>
                </div>
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

              {analysisMode === "point" ? (
                <div className="space-y-2">
                  <Label>Point list</Label>
                  <div className="flex gap-2">
                    <Button type="button" variant="outline" onClick={() => setPointSelected({})}>
                      Clear selection
                    </Button>
                    <Button type="button" variant="outline" onClick={() => { setPointList([]); setPointSelected({}); }}>
                      Clear all
                    </Button>
                  </div>
                  <div className="max-h-40 overflow-auto rounded border p-2 text-sm">
                    {pointList.length === 0 ? (
                      <div className="text-muted-foreground text-xs">No locations added.</div>
                    ) : (
                      <ul className="space-y-1">
                        {pointList.map((p, idx) => {
                          const key = `${p.lat.toFixed(6)},${p.lng.toFixed(6)}`;
                          return (
                            <li
                              key={`point-${idx}`}
                              className="flex items-center justify-between gap-2"
                              onMouseEnter={() => {
                                setLat(p.lat);
                                setLng(p.lng);
                                mapRef.current?.flyTo([p.lat, p.lng], 18);
                              }}
                              onMouseLeave={() => mapRef.current?.flyTo([lat, lng], 16)}
                            >
                              <label className="flex items-center gap-2">
                                <input
                                  type="checkbox"
                                  checked={!!pointSelected[key]}
                                  onChange={(e) => setPointSelected((prev) => ({ ...prev, [key]: e.target.checked }))}
                                />
                                <span className="font-mono">{`${p.lat.toFixed(6)}, ${p.lng.toFixed(6)}`}</span>
                              </label>
                              <button
                                type="button"
                                onClick={() => removeFromPointList(idx)}
                                className="text-xs text-slate-500 hover:underline"
                              >
                                remove
                              </button>
                            </li>
                          );
                        })}
                      </ul>
                    )}
                  </div>
                </div>
              ) : (
                <div className="space-y-2">
                  <Label>To-let list</Label>
                  <div className="flex gap-2">
                    <Button type="button" variant="outline" onClick={() => setToLetSelected({})}>
                      Clear selection
                    </Button>
                  </div>
                  <div className="max-h-40 overflow-auto rounded border p-2 text-sm">
                    {toLetList.length === 0 ? (
                      <div className="text-muted-foreground text-xs">No to-let locations added.</div>
                    ) : (
                      <ul className="space-y-1">
                        {toLetList.map((p, idx) => {
                          const key = `${p.lat.toFixed(6)},${p.lng.toFixed(6)}`;
                          const isSelected = !!toLetSelected[key];
                          return (
                            <li
                              key={`tolet-${idx}`}
                              className="flex items-center gap-2"
                              onMouseEnter={() => {
                                mapRef.current?.flyTo([p.lat, p.lng], 18);
                                setLat(p.lat);
                                setLng(p.lng);
                                if (!isSelected) setHoverToLet(p);
                              }}
                              onMouseLeave={() => {
                                mapRef.current?.flyTo([lat, lng], 16);
                                if (!isSelected) setHoverToLet(null);
                              }}
                            >
                              <input
                                type="checkbox"
                                checked={isSelected}
                                onChange={(e) => setToLetSelected((prev) => ({ ...prev, [key]: e.target.checked }))}
                              />
                              <span className="font-mono">{`${p.lat.toFixed(6)}, ${p.lng.toFixed(6)}`}</span>
                            </li>
                          );
                        })}
                      </ul>
                    )}
                  </div>
                  <div className="rounded border p-2 text-sm">
                    <div className="text-xs text-muted-foreground mb-1">Selected points</div>
                    {selectedToLetList.length === 0 ? (
                      <div className="text-muted-foreground text-xs">None selected.</div>
                    ) : (
                      <ul className="space-y-1">
                        {selectedToLetList.map((p, idx) => (
                          <li
                            key={`tolet-selected-${idx}`}
                            className="font-mono text-xs"
                            onMouseEnter={() => mapRef.current?.flyTo([p.lat, p.lng], 18)}
                            onMouseLeave={() => mapRef.current?.flyTo([lat, lng], 16)}
                          >
                            {`${p.lat.toFixed(6)}, ${p.lng.toFixed(6)}`}
                          </li>
                        ))}
                      </ul>
                    )}
                  </div>
                </div>
              )}


              <div className="space-y-2">
                <Button type="submit" className="w-full py-3">
                  Submit Location
                </Button>
              </div>
              {/* Dataset selector moved to Places panel */}
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
          <ChartRadarLinesOnly data={radarCounts} />
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

                  <div className="space-y-2">
                    <Label>Analysis Mode</Label>
                    <div className="flex gap-2">
                      <button
                        type="button"
                        onClick={() => setAnalysisMode("point")}
                        className={`px-3 py-1 rounded text-sm border ${analysisMode === "point" ? "bg-slate-900 text-white" : "bg-white text-slate-700"}`}
                      >
                        Point pick
                      </button>
                      <button
                        type="button"
                        onClick={() => setAnalysisMode("tolet")}
                        className={`px-3 py-1 rounded text-sm border ${analysisMode === "tolet" ? "bg-slate-900 text-white" : "bg-white text-slate-700"}`}
                      >
                        To-let pick
                      </button>
                    </div>
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

                  {analysisMode === "point" ? (
                    <div className="space-y-2">
                      <Label>Point list</Label>
                      <div className="flex gap-2">
                        <Button type="button" onClick={() => addPointToActiveList({ lat, lng })}>
                          Add current
                        </Button>
                        <Button type="button" variant="outline" onClick={() => setPointSelected({})}>
                          Clear selection
                        </Button>
                        <Button type="button" variant="outline" onClick={() => { setPointList([]); setPointSelected({}); }}>
                          Clear all
                        </Button>
                      </div>
                      <div className="max-h-40 overflow-auto rounded border p-2 text-sm">
                        {pointList.length === 0 ? (
                          <div className="text-muted-foreground text-xs">No locations added.</div>
                        ) : (
                          <ul className="space-y-1">
                            {pointList.map((p, idx) => {
                              const key = `${p.lat.toFixed(6)},${p.lng.toFixed(6)}`;
                              return (
                                <li
                                  key={`point-${idx}`}
                                  className="flex items-center justify-between gap-2"
                                  onMouseEnter={() => {
                                    setLat(p.lat);
                                    setLng(p.lng);
                                    mapRef.current?.flyTo([p.lat, p.lng], 18);
                                  }}
                                  onMouseLeave={() => mapRef.current?.flyTo([lat, lng], 16)}
                                >
                                  <label className="flex items-center gap-2">
                                    <input
                                      type="checkbox"
                                      checked={!!pointSelected[key]}
                                      onChange={(e) => setPointSelected((prev) => ({ ...prev, [key]: e.target.checked }))}
                                    />
                                    <span className="font-mono">{`${p.lat.toFixed(6)}, ${p.lng.toFixed(6)}`}</span>
                                  </label>
                                  <button
                                    type="button"
                                    onClick={() => removeFromPointList(idx)}
                                    className="text-xs text-slate-500 hover:underline"
                                  >
                                    remove
                                  </button>
                                </li>
                              );
                            })}
                          </ul>
                        )}
                      </div>
                      <div className="rounded border p-2 text-sm">
                        <div className="text-xs text-muted-foreground mb-1">Selected points</div>
                        {selectedPointList.length === 0 ? (
                          <div className="text-muted-foreground text-xs">None selected.</div>
                        ) : (
                          <ul className="space-y-1">
                            {selectedPointList.map((p, idx) => (
                              <li
                                key={`point-selected-${idx}`}
                                className="font-mono text-xs"
                                onMouseEnter={() => {
                                  setLat(p.lat);
                                  setLng(p.lng);
                                  mapRef.current?.flyTo([p.lat, p.lng], 18);
                                }}
                                onMouseLeave={() => mapRef.current?.flyTo([lat, lng], 16)}
                              >
                                {`${p.lat.toFixed(6)}, ${p.lng.toFixed(6)}`}
                              </li>
                            ))}
                          </ul>
                        )}
                      </div>
                    </div>
                  ) : (
                    <div className="space-y-2">
                      <Label>To-let list</Label>
                      <div className="flex gap-2">
                        <Button type="button" variant="outline" onClick={() => setToLetSelected({})}>
                          Clear selection
                        </Button>
                      </div>
                      <div className="max-h-40 overflow-auto rounded border p-2 text-sm">
                        {toLetList.length === 0 ? (
                          <div className="text-muted-foreground text-xs">No to-let locations added.</div>
                        ) : (
                          <ul className="space-y-1">
                            {toLetList.map((p, idx) => {
                              const key = `${p.lat.toFixed(6)},${p.lng.toFixed(6)}`;
                              const isSelected = !!toLetSelected[key];
                              return (
                                <li
                                  key={`tolet-${idx}`}
                                  className="flex items-center gap-2"
                                  onMouseEnter={() => {
                                    setLat(p.lat);
                                    setLng(p.lng);
                                    mapRef.current?.flyTo([p.lat, p.lng], 18);
                                    if (!isSelected) setHoverToLet(p);
                                  }}
                                  onMouseLeave={() => {
                                    mapRef.current?.flyTo([lat, lng], 16);
                                    if (!isSelected) setHoverToLet(null);
                                  }}
                                >
                                  <input
                                    type="checkbox"
                                    checked={isSelected}
                                    onChange={(e) => setToLetSelected((prev) => ({ ...prev, [key]: e.target.checked }))}
                                  />
                                  <span className="font-mono">{`${p.lat.toFixed(6)}, ${p.lng.toFixed(6)}`}</span>
                                </li>
                              );
                            })}
                          </ul>
                        )}
                      </div>
                      <div className="rounded border p-2 text-sm">
                        <div className="text-xs text-muted-foreground mb-1">Selected points</div>
                        {selectedToLetList.length === 0 ? (
                          <div className="text-muted-foreground text-xs">None selected.</div>
                        ) : (
                          <ul className="space-y-1">
                            {selectedToLetList.map((p, idx) => (
                              <li
                                key={`tolet-selected-${idx}`}
                                className="font-mono text-xs"
                                onMouseEnter={() => {
                                  setLat(p.lat);
                                  setLng(p.lng);
                                  mapRef.current?.flyTo([p.lat, p.lng], 18);
                                }}
                                onMouseLeave={() => mapRef.current?.flyTo([lat, lng], 16)}
                              >
                                {`${p.lat.toFixed(6)}, ${p.lng.toFixed(6)}`}
                              </li>
                            ))}
                          </ul>
                        )}
                      </div>
                    </div>
                  )}

                  <div>
                    <Label htmlFor="radius-mobile">r: </Label>
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
                  {/* Dataset selector moved to Places panel */}

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
      <div className="flex-1 relative min-h-[480px] bg-transparent z-100 group">
        <MapContainer
          center={[lat, lng]}
          zoom={23}
          className="h-full w-full bg-transparent"
          scrollWheelZoom
          minZoom={15}
          maxBounds={MAP_BOUNDS}
          maxBoundsViscosity={1.0}
        >
          <TileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            attribution='&copy; <a href="https://osm.org/copyright">OpenStreetMap</a>'
          />
          <MapRefSetter mapRef={mapRef} />
          <MapPicker lat={lat} lng={lng} onPick={(plat, plng) => addPointToActiveList({ lat: plat, lng: plng })} />
          {mapPickList.map((p: { lat: number; lng: number }, idx: number) => (
            <Marker
              key={`${analysisMode}-${idx}`}
              position={[p.lat, p.lng]}
              icon={analysisMode === "point" ? pointPickIcon : toLetPickIcon}
            />
          ))}
          {hoverToLet && (
            <Marker
              key={`tolet-hover`}
              position={[hoverToLet.lat, hoverToLet.lng]}
              icon={toLetHoverIcon}
            />
          )}
          {showPlaces && !showWithinRadius && filteredGeoData.map((item) => (
            <MapFeatures
              key={item.id}
              datasetId={item.id}
              geoData={{ type: 'FeatureCollection', features: item.features }}
              selectedFeatureId={selectedFeatureId}
              onFeatureClick={(feature, _layer) => {
                try {
                  const coords = feature.geometry.type === "Point" ? feature.geometry.coordinates : feature.geometry.coordinates[0];
                  setPoiLat(coords[1]);
                  setPoiLng(coords[0]);
                } catch { }
                setSelectedFeatureId(feature.properties?.name ?? feature.id ?? null);
              }}
            />
          ))}

          {/* When showing every POI, render individual markers from geojson features filtered by radiusKm */}
          {showPlaces && showWithinRadius && filteredGeoData.map((ds) => (
            (ds.features || []).map((f: any, idx: number) => {
              try {
                const geom = f.geometry;
                if (!geom) return null;
                const coords = geom.type === 'Point' ? geom.coordinates : (geom.coordinates && geom.coordinates[0]);
                if (!coords || coords.length < 2) return null;
                const flon = Number(coords[0]);
                const flat = Number(coords[1]);
                if (!Number.isFinite(flon) || !Number.isFinite(flat)) return null;
                const d = distanceKm(lat, lng, flat, flon);
                if (d > radiusKm) return null;
                const fid = f.id ?? f.properties?.id ?? `${ds.id}-${idx}`;
                const isSelectedDs = Math.abs(flat - poiLat) < 1e-6 && Math.abs(flon - poiLng) < 1e-6;
                return (
                  <Marker
                    key={`${ds.id}-${fid}`}
                    position={[flat, flon]}
                    icon={isSelectedDs ? selectedPoiIcon(ds.id) : getDatasetIcon(ds.id)}
                    zIndexOffset={isSelectedDs ? 1000 : 0}
                    eventHandlers={{
                      click: () => {
                        setPoiLat(flat);
                        setPoiLng(flon);
                        setHoverTempPoiLat(flat);
                        setHoverTempPoiLng(flon);
                      },
                      mouseover: () => {
                        setPoiLat(flat);
                        setPoiLng(flon);
                      },
                      mouseout: () => {
                        setPoiLat(hoverTempPoiLat);
                        setPoiLng(hoverTempPoiLng);
                      },
                    }}
                  />
                );
              } catch (e) {
                return null;
              }
            })
          ))}
          {/* POI markers from augmented poisFlat grouped by category (keeps index in sync with panel) */}
          {Object.entries(poisFlat.reduce((acc: Record<string, any[]>, p: any) => { (acc[p.type] = acc[p.type] || []).push(p); return acc; }, {})).map(([type, items]: any) => (
            (items as any[]).map((p: any, idx: number) => {
              const key = `${type}-${idx}`;
              const plat = Number(p.lat);
              const plon = Number(p.lon);
              const isSelected = Math.abs(plat - poiLat) < 1e-6 && Math.abs(plon - poiLng) < 1e-6;
              return (
                <Marker
                  key={key}
                  position={[plat, plon]}
                  icon={isSelected ? selectedPoiIcon(type) : poiIcon(type)}
                  zIndexOffset={isSelected ? 1000 : 0}
                  ref={(r) => {
                    try {
                      if (r) poiMarkersRef.current[key] = (r as unknown) as L.Marker;
                      else delete poiMarkersRef.current[key];
                    } catch (e) { }
                  }}
                />
              );
            })
          ))}
        </MapContainer>

        {/* Places panel (toggle) */}
        {showPlaces && (
          <div className="absolute top-4 right-4 z-[9999]">
            <div className="liquid-glass rounded-md p-2 max-w-xs">
              <div className="px-2 pb-2 flex items-center gap-2 min-w-0">
                <input
                  type="search"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="Search places..."
                  className="flex-1 min-w-0 px-2 py-1 rounded border text-sm"
                />
                <div className="ml-0 flex items-center gap-2 flex-none">
                  {/* <Label htmlFor="radius" className="text-sm whitespace-nowrap"></Label> */}
                  <Input
                    id="radius"
                    type="number"
                    value={radiusKm}
                    onChange={(e) => setRadiusKm(Number(e.target.value) || 0)}
                    step="0.1"
                    min="0.1"
                    max="5"
                    className="mt-0 w-12 p-0 "
                  />
                  <div className="text-xs text-muted-foreground">km</div>
                </div>
              </div>
              <div className="px-2 pb-2 overflow-x-auto">
                <div className="flex flex-wrap items-center gap-2">
                  {DATASETS.map((d) => {
                    const cnt = getDatasetCount(d.id);
                    const label = `${d.name}${cnt === null ? ' (…)' : ` (${cnt})`}`;
                    const active = d.id === datasetId;
                    return (
                      <button
                        key={d.id}
                        onClick={() => { setDatasetId(d.id); setShowPlaces(true); }}
                        className={"text-sm px-3 py-1 rounded " + (active ? 'bg-slate-800 text-white' : 'bg-white/30 text-slate-700')}
                      >
                        {label}
                      </button>
                    );
                  })}
                </div>
              </div>
              <div className="mt-2 max-h-60 overflow-auto">
                {geoLoading && <div className="text-sm text-muted-foreground p-2">Loading...</div>}
                {!geoLoading && geoDataList.length === 0 && <div className="text-sm text-muted-foreground p-2">No places loaded</div>}
                {filteredGeoData.map((item) => {
                  const allFeatures = (item.features || []) as any[];
                  // when showWithinRadius is enabled, restrict to features within radiusKm of the center
                  const features = showWithinRadius
                    ? allFeatures.filter((f) => {
                      try {
                        const coords = f.geometry?.type === 'Point' ? f.geometry.coordinates : (f.geometry?.coordinates && f.geometry.coordinates[0]);
                        if (!coords || coords.length < 2) return false;
                        const flon = Number(coords[0]);
                        const flat = Number(coords[1]);
                        if (!Number.isFinite(flon) || !Number.isFinite(flat)) return false;
                        const d = distanceKm(lat, lng, flat, flon);
                        return d <= radiusKm;
                      } catch (e) {
                        return false;
                      }
                    })
                    : allFeatures;
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
                                    // setLat(coords[1]);
                                    // setLng(coords[0]);
                                    setPoiLat(coords[1]);
                                    setPoiLng(coords[0]);
                                    setHoverTempPoiLat(coords[1]);
                                    setHoverTempPoiLng(coords[0]);
                                  } catch (e) { }
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
          <div className="absolute bottom-4 right-4 z-[9999] opacity-0 invisible group-hover:opacity-100 group-hover:visible pointer-events-none group-hover:pointer-events-auto transition-opacity duration-200">
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
            <div className="w-80 h-44 rounded-lg overflow-hidden shadow-lg text-white relative">
              {selectedCsvRow?.imageUrl && !overlayImageFailed && (
                <img
                  src={selectedCsvRow.imageUrl}
                  alt={selectedCsvRow?.name || selectedCsvRow?.place_id || 'image'}
                  className="absolute inset-0 w-full h-full object-cover z-0"
                  onError={() => setOverlayImageFailed(true)}
                  onLoad={() => setOverlayImageFailed(false)}
                />
              )}
              <div className="w-full h-full bg-black/30 p-3 flex flex-col justify-end relative z-10">
                <div className="text-lg font-bold leading-tight">{selectedCsvRow['name'] || selectedCsvRow['place_id'] || 'Place'}</div>
                <div className="text-sm mt-1">{selectedCsvRow['address']}</div>
                <div className="text-sm mt-1">Distance: {distanceKm(poiLat, poiLng, lat, lng).toFixed(2)} KM</div>
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
