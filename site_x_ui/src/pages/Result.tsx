"use client";

import React, { useMemo, useEffect, useState, useRef } from "react";
import {
    ResponsiveContainer,
    PieChart,
    Pie,
    Cell,
    Tooltip,
    BarChart,
    Bar,
    XAxis,
    YAxis,
    CartesianGrid,
    Legend
} from "recharts";
import { MapContainer, TileLayer, Marker, Polyline } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import * as L from "leaflet";

function qs(key: string) {
    return new URLSearchParams(window.location.search).get(key) || "";
}

function haversineKm(aLat: number, aLon: number, bLat: number, bLon: number) {
    const toRad = (v: number) => (v * Math.PI) / 180;
    const R = 6371;
    const dLat = toRad(bLat - aLat);
    const dLon = toRad(bLon - aLon);
    const lat1 = toRad(aLat);
    const lat2 = toRad(bLat);
    const u = Math.sin(dLat / 2) ** 2 + Math.sin(dLon / 2) ** 2 * Math.cos(lat1) * Math.cos(lat2);
    const c = 2 * Math.atan2(Math.sqrt(u), Math.sqrt(1 - u));
    return R * c;
}

type Point = { lat: number; lng: number };
type PoiApiItem = {
    lat: number;
    lon?: number;
    lng?: number;
    name?: string;
    weight?: number;
    distance_km?: number;
    path?: Array<{ lat: number; lon?: number; lng?: number }>;
    [key: string]: unknown;
};
type Poi = { name: string; lat: number; lng: number; weight: number; distance_km: number; subcategory?: string; raw?: PoiApiItem };
type ToLetEntry = {
    key: string;
    lat: number;
    lng: number;
    title: string;
    ratePerMonth?: number;
    url?: string;
    images: string[];
};
type CommonPoi = {
    key: string;
    name: string;
    lat: number;
    lng: number;
    weightA: number;
    weightB: number;
    distanceA: number;
    distanceB: number;
    decayedA: number;
    decayedB: number;
    rawA?: PoiApiItem;
    rawB?: PoiApiItem;
    subcategory?: string;
    cat: string;
};
type AccessibilityResponse = { score?: number };
type PredictionResponse = { predictions?: Array<{ lat: number; lon: number; score: number; risk_level?: string }> };

type PoisByCategory = Record<string, Poi[]>;

const TOLET_IMAGE_BY_INDEX: Array<string[]> = [
    ["1-nagadesh.jpg"],
    ["2.jpg", "2-2.jpg"],
    ["3.jpg"],
    ["4.jpg", "4-2.jpg"],
    ["5.jpg"],
];

function parseCsvLine(line: string) {
    const out: string[] = [];
    let cur = "";
    let inQuotes = false;
    for (let i = 0; i < line.length; i++) {
        const ch = line[i];
        if (ch === '"') {
            if (inQuotes && i + 1 < line.length && line[i + 1] === '"') {
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
}

function parseToLetCsv(text: string) {
    const lines = text.split(/\r?\n/).filter((l) => l.trim().length > 0);
    if (!lines.length) return [];
    const firstCols = parseCsvLine(lines[0]).map((v) => v.trim());
    const hasHeader = firstCols.some((v) => v.toLowerCase() === "lat" || v.toLowerCase() === "lng");
    const headers = hasHeader ? firstCols.map((h) => h.toLowerCase()) : [];
    const startIdx = hasHeader ? 1 : 0;
    const rows: Array<{ lat: number; lng: number; title: string; ratePerMonth?: number; url?: string }> = [];
    for (let i = startIdx; i < lines.length; i++) {
        const cols = parseCsvLine(lines[i]);
        if (cols.length < 2) continue;
        const latVal = Number(hasHeader ? cols[headers.indexOf("lat")] : cols[0]);
        const lngVal = Number(hasHeader ? cols[headers.indexOf("lng")] : cols[1]);
        if (!Number.isFinite(latVal) || !Number.isFinite(lngVal)) continue;
        const title = (hasHeader ? cols[headers.indexOf("description")] : cols[2]) ?? "";
        const rateRaw = (hasHeader ? cols[headers.indexOf("rate_per_month")] : cols[3]) ?? "";
        const url = (hasHeader ? cols[headers.indexOf("url")] : cols[4]) ?? "";
        const ratePerMonth = Number(rateRaw);
        rows.push({
            lat: latVal,
            lng: lngVal,
            title: String(title || "").trim(),
            ratePerMonth: Number.isFinite(ratePerMonth) ? ratePerMonth : undefined,
            url: String(url || "").trim() || undefined
        });
    }
    return rows;
}

function parsePoints(raw: string, fallbackLat: number, fallbackLng: number): Point[] {
    const cleaned = (raw || "").trim();
    if (!cleaned) {
        if (Number.isFinite(fallbackLat) && Number.isFinite(fallbackLng) && (fallbackLat !== 0 || fallbackLng !== 0)) {
            return [{ lat: fallbackLat, lng: fallbackLng }];
        }
        return [];
    }
    const lines = cleaned.split(/\r?\n|;/).map(l => l.trim()).filter(Boolean);
    const points: Point[] = [];
    for (const line of lines) {
        const parts = line.split(/[\s,]+/).filter(Boolean);
        if (parts.length < 2) continue;
        const plat = Number(parts[0]);
        const plng = Number(parts[1]);
        if (!Number.isFinite(plat) || !Number.isFinite(plng)) continue;
        points.push({ lat: Number(plat.toFixed(6)), lng: Number(plng.toFixed(6)) });
    }
    if (points.length === 0 && Number.isFinite(fallbackLat) && Number.isFinite(fallbackLng) && (fallbackLat !== 0 || fallbackLng !== 0)) {
        return [{ lat: fallbackLat, lng: fallbackLng }];
    }
    return points;
}


export default function ResultPage() {
    const name = decodeURIComponent(qs("name") || "");
    const lat = parseFloat(qs("lat") || "0");
    const lng = parseFloat(qs("lng") || "0");
    const mode = qs("mode") || "point";
    const pick = qs("pick") || (qs("points") ? "multiple" : "single");
    const rentParam = qs("rent");
    const pointsParam = qs("points");
    const points = useMemo(() => parsePoints(pointsParam, lat, lng), [pointsParam, lat, lng]);
    const center = useMemo(() => {
        if (!points.length) return { lat, lng };
        const total = points.reduce((acc, p) => ({ lat: acc.lat + p.lat, lng: acc.lng + p.lng }), { lat: 0, lng: 0 });
        return { lat: total.lat / points.length, lng: total.lng / points.length };
    }, [points, lat, lng]);
    const centerLat = center.lat;
    const centerLng = center.lng;

    const [loadedPoisByPointKey, setLoadedPoisByPointKey] = useState<Record<string, PoisByCategory>>({});
    const poisCacheRef = useRef<Map<string, Record<string, Poi[]>>>(new Map());
    const accessibilityCacheRef = useRef<Map<string, Record<string, number>>>(new Map());
    const predictionCacheRef = useRef<Map<string, Record<string, { score: number; risk_level?: string }>>>(new Map());
    const aiCacheRef = useRef<Map<string, string>>(new Map());
    const [toLetEntries, setToLetEntries] = useState<ToLetEntry[]>([]);
    const [selectedPointIdx, setSelectedPointIdx] = useState<number>(0);
    const [viewMode, setViewMode] = useState<"single" | "compare">("single");
    const [comparePointIdxA, setComparePointIdxA] = useState<number>(0);
    const [comparePointIdxB, setComparePointIdxB] = useState<number>(1);
    const [singlePage, setSinglePage] = useState<"insights" | "nearby" | "explain">("insights");
    const [comparePage, setComparePage] = useState<"insights" | "nearby" | "explain">("insights");
    const [selectedCategory, setSelectedCategory] = useState<string>("All");
    const [accessibilityScores, setAccessibilityScores] = useState<Record<string, number>>({});
    const [predictionScores, setPredictionScores] = useState<Record<string, { score: number; risk_level?: string }>>({});
    const [aiExplanation, setAiExplanation] = useState<string>("");
    const [aiLoading, setAiLoading] = useState<boolean>(false);
    const [aiError, setAiError] = useState<string>("");
    const selectedPoint = useMemo(() => {
        return points[selectedPointIdx] || points[0] || { lat: centerLat, lng: centerLng };
    }, [points, selectedPointIdx, centerLat, centerLng]);
    const selectedPointKey = useMemo(
        () => `${Number(selectedPoint.lat).toFixed(6)},${Number(selectedPoint.lng).toFixed(6)}`,
        [selectedPoint]
    );
    const loadedPois = loadedPoisByPointKey[selectedPointKey] ?? null;
    const selectedAccessibility = accessibilityScores[selectedPointKey] ?? null;
    const selectedPrediction = predictionScores[selectedPointKey] ?? null;
    const pointsKey = useMemo(
        () => points.map((p) => `${p.lat.toFixed(6)},${p.lng.toFixed(6)}`).join("|") || "__empty__",
        [points]
    );
    const MAX_RADIUS_KM = 1;
    const ACCESS_RADIUS_KM = 0.3;
    const PREDICTION_DISPLAY_MAX = 100;
    const POI_SCORE_MAX = 35;
    // --- Load POIs from backend POI endpoint instead of CSVs ---
    const DECAY_SCALE_KM = 1.0;
    const cachePrefix = "sitex:cache:";
    const getCache = <T,>(key: string): T | null => {
        try {
            const raw = localStorage.getItem(cachePrefix + key);
            if (!raw) return null;
            return JSON.parse(raw) as T;
        } catch {
            return null;
        }
    };
    const setCache = (key: string, value: unknown) => {
        try {
            localStorage.setItem(cachePrefix + key, JSON.stringify(value));
        } catch {
            // ignore storage errors
        }
    };
    const getDecayedWeight = (poi: Poi) => {
        const w = Number(poi.weight) || 0;
        const d = Number(poi.distance_km) || 0;
        return w * Math.exp(-d / DECAY_SCALE_KM);
    };
    const getPredictionDisplayScore = (score?: number | null) => {
        const raw = Number(score);
        if (!Number.isFinite(raw)) return null;
        return Math.max(0, Math.min(raw * 25, PREDICTION_DISPLAY_MAX));
    };

    const rentIndexes = useMemo(() => {
        if (!rentParam) return [] as Array<number | null>;
        return rentParam.split(",").map((v) => {
            const n = Number(v);
            return Number.isFinite(n) ? Math.trunc(n) : null;
        });
    }, [rentParam]);

    const clampPct = (value?: number | null) => {
        const raw = Number(value);
        if (!Number.isFinite(raw)) return null;
        return Math.max(0, Math.min(raw, 100));
    };

    const getPoiScorePercent = (score?: number | null) => {
        const raw = Number(score);
        if (!Number.isFinite(raw)) return null;
        return Math.max(0, Math.min((raw / POI_SCORE_MAX) * 100, 100));
    };

    const renderScoreRing = (value: number | null, title: string, subtitle: string, color: string) => {
        const pct = clampPct(value);
        const size = 110;
        const stroke = 10;
        const r = (size - stroke) / 2;
        const c = 2 * Math.PI * r;
        const offset = pct == null ? c : c * (1 - pct / 100);
        return (
            <div style={{ border: '1px solid #e2e8f0', borderRadius: 14, padding: 12, background: '#f8fafc', display: 'flex', alignItems: 'center', gap: 12 }}>
                <div style={{ position: 'relative', width: size, height: size }}>
                    <svg width={size} height={size}>
                        <circle cx={size / 2} cy={size / 2} r={r} stroke="#e5e7eb" strokeWidth={stroke} fill="none" />
                        <circle
                            cx={size / 2}
                            cy={size / 2}
                            r={r}
                            stroke={color}
                            strokeWidth={stroke}
                            fill="none"
                            strokeDasharray={`${c} ${c}`}
                            strokeDashoffset={offset}
                            strokeLinecap="round"
                            transform={`rotate(-90 ${size / 2} ${size / 2})`}
                            style={{ transition: 'stroke-dashoffset 0.7s ease' }}
                        />
                    </svg>
                    <div style={{ position: 'absolute', inset: 0, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
                        <div style={{ fontWeight: 800, fontSize: 20 }}>{pct == null ? '...' : `${Math.round(pct)}%`}</div>
                        <div style={{ fontSize: 11, color: '#64748b', textAlign: 'center' }}>{subtitle}</div>
                    </div>
                </div>
                <div style={{ flex: 1 }}>
                    <div style={{ fontWeight: 800 }}>{title}</div>
                </div>
            </div>
        );
    };

    useEffect(() => {
        if (viewMode !== "compare") return;
        if (points.length === 0) return;
        setSelectedPointIdx(comparePointIdxA);
    }, [viewMode, comparePointIdxA, points.length]);

    useEffect(() => {
        let mounted = true;
        if (mode !== "tolet" && !rentParam) return () => { mounted = false; };
        (async () => {
            try {
                const res = await fetch("/data/to-let/listings.csv");
                if (!res.ok) return;
                const txt = await res.text();
                const parsed = parseToLetCsv(txt);
                const entries: ToLetEntry[] = parsed.map((row, idx) => {
                    const key = `${row.lat.toFixed(6)},${row.lng.toFixed(6)}`;
                    const imageNames = TOLET_IMAGE_BY_INDEX[idx] || [];
                    const images = imageNames.map((img) => `/data/to-let/${img}`);
                    return {
                        key,
                        lat: row.lat,
                        lng: row.lng,
                        title: row.title || `To-let ${idx + 1}`,
                        ratePerMonth: row.ratePerMonth,
                        url: row.url,
                        images
                    };
                });
                if (mounted) setToLetEntries(entries);
            } catch {
                // ignore
            }
        })();
        return () => { mounted = false; };
    }, [mode, rentParam]);

    const pointMeta = useMemo(() => {
        return points.map((p, idx) => {
            const rentIdx = rentIndexes[idx];
            const entry = rentIdx != null && rentIdx >= 0 ? toLetEntries[rentIdx] : null;
            const label = entry?.title || (name ? name : `Point ${idx + 1}`);
            const image = entry?.images?.[0] || null;
            return {
                key: `${p.lat.toFixed(6)},${p.lng.toFixed(6)}`,
                label,
                image,
                entry
            };
        });
    }, [points, rentIndexes, toLetEntries, name]);

    const selectedPointMeta = pointMeta[selectedPointIdx] || null;

    useEffect(() => {
        if (points.length < 2) {
            setViewMode("single");
            setComparePointIdxA(0);
            setComparePointIdxB(1);
            setSelectedPointIdx(0);
            return;
        }

        setComparePointIdxA((prev) => Math.min(Math.max(0, prev), points.length - 1));
        setComparePointIdxB((prev) => {
            const clamped = Math.min(Math.max(0, prev), points.length - 1);
            if (clamped === comparePointIdxA) {
                return comparePointIdxA === 0 ? 1 : 0;
            }
            return clamped;
        });
        setSelectedPointIdx((prev) => Math.min(Math.max(0, prev), points.length - 1));
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [points.length]);

    useEffect(() => {
        let mounted = true;
        const controller = new AbortController();
        const mapName: Record<string, string> = { cafes: 'Cafes', banks: 'Bank', education: 'Education', health: 'Health', temples: 'Temples', other: 'Other' };

        const setPoisForKey = (key: string, categoriesMap: PoisByCategory) => {
            setLoadedPoisByPointKey((prev) => {
                if (prev[key] === categoriesMap) return prev;
                return { ...prev, [key]: categoriesMap };
            });
        };

        const fetchPoisForPoint = async (point: Point) => {
            const key = `${point.lat.toFixed(6)},${point.lng.toFixed(6)}`;
            const inMem = poisCacheRef.current.get(key);
            if (inMem) {
                if (mounted) setPoisForKey(key, inMem);
                return;
            }
            const cachedLocal = getCache<Record<string, Poi[]>>(`pois:${key}`);
            if (cachedLocal) {
                poisCacheRef.current.set(key, cachedLocal);
                if (mounted) setPoisForKey(key, cachedLocal);
                return;
            }
            const radius = 0.3; // km
            const base = `http://127.0.0.1:8000/api/v1/pois/?lat=${encodeURIComponent(point.lat)}&lon=${encodeURIComponent(point.lng)}&radius_km=${radius}`;
            const streamUrl = base + `&stream=true`;
            const res = await fetch(streamUrl, { signal: controller.signal });
            const categoriesMap: Record<string, Poi[]> = {};
            if (!res.ok) {
                poisCacheRef.current.set(key, {});
                setCache(`pois:${key}`, {});
                if (mounted) setPoisForKey(key, {});
                return;
            }
            if (res.body && (res.headers.get('content-type') || '').includes('ndjson')) {
                const reader = res.body.getReader();
                const dec = new TextDecoder();
                let buf = '';
                while (true) {
                    const { done, value } = await reader.read();
                    if (done) break;
                    buf += dec.decode(value, { stream: true });
                    const parts = buf.split(/\n/);
                    buf = parts.pop() || '';
                    for (const line of parts) {
                        const trimmed = line.trim();
                        if (!trimmed) continue;
                        try {
                            const obj = JSON.parse(trimmed);
                            const catKey = obj.category as string;
                            const arr = Array.isArray(obj.items) ? (obj.items as PoiApiItem[]) : [];
                            const display = mapName[catKey] || catKey;
                            const list = arr.map((it: PoiApiItem) => {
                                const plat = Number(it.lat);
                                const plng = Number(it.lon ?? it.lng ?? 0);
                                const nameVal = it.name ?? '';
                                const weight = Number(it.weight ?? 0) || 0;
                                const distance_km = Number(it.distance_km ?? 0) || 0;
                                const poi: Poi = { name: nameVal, lat: plat, lng: plng, weight, distance_km, raw: it };
                                return poi;
                            }).filter((p: Poi) => Number.isFinite(p.lat) && Number.isFinite(p.lng));
                            if (list.length) {
                                categoriesMap[display] = (categoriesMap[display] || []).concat(list);
                            }
                        } catch {
                            // ignore parse errors for partial lines
                        }
                    }
                }
                if (buf.trim()) {
                    try {
                        const obj = JSON.parse(buf.trim());
                        const catKey = obj.category as string;
                        const arr = Array.isArray(obj.items) ? (obj.items as PoiApiItem[]) : [];
                        const display = mapName[catKey] || catKey;
                        const list = arr.map((it: PoiApiItem) => {
                            const plat = Number(it.lat);
                            const plng = Number(it.lon ?? it.lng ?? 0);
                            const nameVal = it.name ?? '';
                            const weight = Number(it.weight ?? 0) || 0;
                            const distance_km = Number(it.distance_km ?? 0) || 0;
                            const poi: Poi = { name: nameVal, lat: plat, lng: plng, weight, distance_km, raw: it };
                            return poi;
                        }).filter((p: Poi) => Number.isFinite(p.lat) && Number.isFinite(p.lng));
                        if (list.length) {
                            categoriesMap[display] = (categoriesMap[display] || []).concat(list);
                        }
                    } catch { /* ignore */ }
                }
            } else {
                const data = await res.json();
                const pois = data?.pois || {};
                for (const [catKey, arr] of Object.entries(pois)) {
                    const display = mapName[catKey] || catKey;
                    const list = (arr as PoiApiItem[]).map((it: PoiApiItem) => {
                        const plat = Number(it.lat);
                        const plng = Number(it.lon ?? it.lng ?? 0);
                        const nameVal = it.name ?? '';
                        const weight = Number(it.weight ?? 0) || 0;
                        const distance_km = Number(it.distance_km ?? 0) || 0;
                        const poi: Poi = { name: nameVal, lat: plat, lng: plng, weight, distance_km, raw: it };
                        return poi;
                    }).filter((p: Poi) => Number.isFinite(p.lat) && Number.isFinite(p.lng));
                    if (list.length) categoriesMap[display] = list;
                }
            }
            poisCacheRef.current.set(key, categoriesMap);
            setCache(`pois:${key}`, categoriesMap);
            if (mounted) setPoisForKey(key, categoriesMap);
        };

        (async () => {
            try {
                if (!points.length) {
                    if (mounted) setLoadedPoisByPointKey({});
                    return;
                }
                await Promise.all(points.map((p) => fetchPoisForPoint(p)));
            } catch {
                // keep existing state; failures are handled per-point
            }
        })();
        return () => { mounted = false; controller.abort(); };
    }, [points]);

    // CSV fallback removed — POIs are loaded from backend `/api/v1/pois/` above.

    const mapRef = useRef<L.Map | null>(null);
    const [hoverPos, setHoverPos] = useState<{ lat: number; lng: number } | null>(null);
    const [hoverPath, setHoverPath] = useState<Array<[number, number]> | null>(null);
    const [hoverPathA, setHoverPathA] = useState<Array<[number, number]> | null>(null);
    const [hoverPathB, setHoverPathB] = useState<Array<[number, number]> | null>(null);
    const [pathDashOffset, setPathDashOffset] = useState<number>(0);
    const [pathOpacity, setPathOpacity] = useState<number>(0);
    const [searchQuery, setSearchQuery] = useState("");

    const compareMarkerA = useMemo(() => L.divIcon({
        className: "",
        html: '<div style="width:18px;height:18px;border-radius:50%;background:#3b82f6;border:2px solid #1e40af;box-shadow:0 0 0 2px rgba(59,130,246,0.2);"></div>',
        iconSize: [18, 18],
        iconAnchor: [9, 9]
    }), []);

    const compareMarkerB = useMemo(() => L.divIcon({
        className: "",
        html: '<div style="width:18px;height:18px;border-radius:50%;background:#f97316;border:2px solid #c2410c;box-shadow:0 0 0 2px rgba(249,115,22,0.2);"></div>',
        iconSize: [18, 18],
        iconAnchor: [9, 9]
    }), []);

    const getPathCoords = (raw?: PoiApiItem | null) => {
        if (!raw || !Array.isArray(raw.path)) return null;
        const coords: Array<[number, number]> = raw.path
            .map((pt) => [Number(pt.lat), Number(pt.lon ?? pt.lng)] as [number, number])
            .filter(([a, b]: [number, number]) => Number.isFinite(a) && Number.isFinite(b));
        return coords.length ? coords : null;
    };

    useEffect(() => {
        const hasPath = (hoverPath && hoverPath.length > 0)
            || (hoverPathA && hoverPathA.length > 0)
            || (hoverPathB && hoverPathB.length > 0);
        if (!hasPath) return;
        let raf = 0;
        let offset = 0;
        setPathOpacity(0);
        requestAnimationFrame(() => setPathOpacity(1));
        const tick = () => {
            offset = (offset + 1) % 32;
            setPathDashOffset(offset);
            raf = requestAnimationFrame(tick);
        };
        raf = requestAnimationFrame(tick);
        return () => cancelAnimationFrame(raf);
    }, [hoverPath, hoverPathA, hoverPathB]);

    useEffect(() => {
        let mounted = true;
        const controller = new AbortController();
        (async () => {
            if (points.length === 0) {
                if (mounted) {
                    setAccessibilityScores({});
                    setPredictionScores({});
                }
                return;
            }

            const loadAccessibility = async () => {
                const cached = accessibilityCacheRef.current.get(pointsKey);
                if (cached) return cached;
                const cachedLocal = getCache<Record<string, number>>(`accessibility:${pointsKey}`);
                if (cachedLocal) {
                    accessibilityCacheRef.current.set(pointsKey, cachedLocal);
                    return cachedLocal;
                }
                const newScores: Record<string, number> = {};
                await Promise.all(points.map(async (p) => {
                    const url = `http://127.0.0.1:8000/api/v1/road-types/summary-accessibility?lat=${encodeURIComponent(p.lat)}&lon=${encodeURIComponent(p.lng)}&radius_km=${ACCESS_RADIUS_KM}&decay_scale_km=${ACCESS_RADIUS_KM}`;
                    const res = await fetch(url, { signal: controller.signal });
                    if (!res.ok) return;
                    const data = (await res.json()) as AccessibilityResponse;
                    const score = Number(data?.score);
                    if (Number.isFinite(score)) {
                        const key = `${p.lat.toFixed(6)},${p.lng.toFixed(6)}`;
                        newScores[key] = score;
                    }
                }));
                accessibilityCacheRef.current.set(pointsKey, newScores);
                setCache(`accessibility:${pointsKey}`, newScores);
                return newScores;
            };

            const loadPredictions = async () => {
                const cached = predictionCacheRef.current.get(pointsKey);
                if (cached) return cached;
                const cachedLocal = getCache<Record<string, { score: number; risk_level?: string }>>(`prediction:${pointsKey}`);
                if (cachedLocal) {
                    predictionCacheRef.current.set(pointsKey, cachedLocal);
                    return cachedLocal;
                }
                const payload = {
                    locations: points.map((p) => ({ lat: p.lat, lon: p.lng }))
                };
                const res = await fetch("http://127.0.0.1:8000/api/v1/predict/", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(payload),
                    signal: controller.signal
                });
                if (!res.ok) return {};
                const data = (await res.json()) as PredictionResponse;
                const newScores: Record<string, { score: number; risk_level?: string }> = {};
                (data?.predictions || []).forEach((item) => {
                    const key = `${Number(item.lat).toFixed(6)},${Number(item.lon).toFixed(6)}`;
                    newScores[key] = {
                        score: Number(item.score) || 0,
                        risk_level: item.risk_level
                    };
                });
                predictionCacheRef.current.set(pointsKey, newScores);
                setCache(`prediction:${pointsKey}`, newScores);
                return newScores;
            };

            try {
                const [accessScores, predictScores] = await Promise.all([
                    loadAccessibility(),
                    loadPredictions()
                ]);
                if (mounted) {
                    setAccessibilityScores(accessScores);
                    setPredictionScores(predictScores);
                }
            } catch (err) {
                if (mounted) {
                    setAccessibilityScores({});
                    setPredictionScores({});
                }
                console.error('Error fetching accessibility/prediction scores:', err);
            }
        })();
        return () => { mounted = false; controller.abort(); };
    }, [points, pointsKey]);

    useEffect(() => {
        try {
            mapRef.current?.flyTo([selectedPoint.lat, selectedPoint.lng], 16);
        } catch (err) { void err; }
    }, [selectedPoint]);

    const filteredPois = useMemo(() => {
        if (!loadedPois) return null;
        const result: Record<string, Poi[]> = {};
        Object.entries(loadedPois).forEach(([cat, list]) => {
            const items = list
                .map((p) => ({
                    ...p,
                    distance_km: Number(haversineKm(selectedPoint.lat, selectedPoint.lng, p.lat, p.lng).toFixed(3))
                }))
                .filter((p) => p.distance_km <= MAX_RADIUS_KM);
            result[cat] = items;
        });
        return result;
    }, [loadedPois, selectedPoint, MAX_RADIUS_KM]);

    const categoryCounts = useMemo(() => {
        if (!filteredPois) return {};
        const counts: Record<string, number> = {};
        let total = 0;
        Object.entries(filteredPois).forEach(([cat, list]) => {
            const filteredList = list.filter(p => p.name.toLowerCase().includes(searchQuery.toLowerCase()));
            counts[cat] = filteredList.length;
            total += filteredList.length;
        });
        counts['All'] = total;
        return counts;
    }, [filteredPois, searchQuery]);

    const categoryDecayedAverages = useMemo(() => {
        if (!filteredPois) return {};
        const averages: Record<string, number> = {};
        let totalCount = 0;
        let totalSum = 0;
        Object.entries(filteredPois).forEach(([cat, list]) => {
            const filteredList = list.filter(p => p.name.toLowerCase().includes(searchQuery.toLowerCase()));
            if (filteredList.length === 0) {
                averages[cat] = 0;
                return;
            }
            const sum = filteredList.reduce((acc, p) => acc + getDecayedWeight(p), 0);
            averages[cat] = sum / filteredList.length;
            totalCount += filteredList.length;
            totalSum += sum;
        });
        averages['All'] = totalCount > 0 ? totalSum / totalCount : 0;
        return averages;
    }, [filteredPois, searchQuery]);

    const categoryTotals = useMemo(() => {
        if (!filteredPois) return {} as Record<string, number>;
        const totals: Record<string, number> = {};
        Object.entries(filteredPois).forEach(([cat, list]) => {
            const filteredList = list.filter(p => p.name.toLowerCase().includes(searchQuery.toLowerCase()));
            totals[cat] = filteredList.reduce((acc, poi) => acc + getDecayedWeight(poi), 0);
        });
        return totals;
    }, [filteredPois, searchQuery]);

    const allTotalDecayed = useMemo(() => {
        if (!filteredPois) return 0;
        return Object.values(categoryTotals).reduce((acc, v) => acc + v, 0);
    }, [categoryTotals, filteredPois]);

    const getAllSharePct = (poi: Poi) => {
        const total = allTotalDecayed;
        const wEff = getDecayedWeight(poi);
        if (total <= 0) return 0;
        return Math.round(Math.min(1, wEff / total) * 100);
    };

    const getCategorySharePct = (poi: Poi, cat: string) => {
        const total = categoryTotals[cat] || 0;
        const wEff = getDecayedWeight(poi);
        if (total <= 0) return 0;
        return Math.round(Math.min(1, wEff / total) * 100);
    };

    const getCommonSharePct = (poi: CommonPoi) => {
        const total = commonAllTotalDecayed;
        const wEff = poi.decayedA + poi.decayedB;
        if (total <= 0) return 0;
        return Math.round(Math.min(1, wEff / total) * 100);
    };

    const getCommonCategorySharePct = (poi: CommonPoi, cat: string) => {
        const total = commonCategoryTotals[cat] || 0;
        const wEff = poi.decayedA + poi.decayedB;
        if (total <= 0) return 0;
        return Math.round(Math.min(1, wEff / total) * 100);
    };

    const chartColors = useMemo(() => ({
        Cafes: "#22c55e",
        Bank: "#0ea5e9",
        Education: "#a855f7",
        Health: "#f97316",
        Temples: "#eab308",
        Other: "#64748b"
    }), []);

    const categoryPieData = useMemo(() => {
        const data = Object.entries(categoryCounts)
            .filter(([cat]) => cat !== "All")
            .map(([cat, count]) => ({ name: cat, value: count }));
        return data.filter((d) => d.value > 0);
    }, [categoryCounts]);

    const categoryAvgData = useMemo(() => {
        return Object.entries(categoryDecayedAverages)
            .filter(([cat]) => cat !== "All")
            .map(([cat, avg]) => ({ name: cat, value: Number(avg) || 0 }))
            .sort((a, b) => b.value - a.value);
    }, [categoryDecayedAverages]);


    const selectedTargets = useMemo(() => {
        const mkKey = (p: Point) => `${Number(p.lat).toFixed(6)},${Number(p.lng).toFixed(6)}`;
        if (viewMode === "compare" && points.length >= 2) {
            const a = points[comparePointIdxA] ?? points[0];
            const b = points[comparePointIdxB] ?? points[1] ?? points[0];
            const aKey = mkKey(a);
            const bKey = mkKey(b);
            return [
                {
                    label: "A" as const,
                    idx: comparePointIdxA,
                    point: a,
                    key: aKey,
                    accessibility: accessibilityScores[aKey] ?? null,
                    prediction: predictionScores[aKey] ?? null
                },
                {
                    label: "B" as const,
                    idx: comparePointIdxB,
                    point: b,
                    key: bKey,
                    accessibility: accessibilityScores[bKey] ?? null,
                    prediction: predictionScores[bKey] ?? null
                }
            ];
        }

        return [
            {
                label: "S" as const,
                idx: selectedPointIdx,
                point: selectedPoint,
                key: selectedPointKey,
                accessibility: selectedAccessibility,
                prediction: selectedPrediction
            }
        ];
    }, [
        viewMode,
        points,
        comparePointIdxA,
        comparePointIdxB,
        selectedPointIdx,
        selectedPoint,
        selectedPointKey,
        selectedAccessibility,
        selectedPrediction,
        accessibilityScores,
        predictionScores
    ]);

    const compareCategoryStats = useMemo(() => {
        if (viewMode !== "compare" || selectedTargets.length < 2) return null;
        const [a, b] = selectedTargets;
        const poisA = loadedPoisByPointKey[a.key] || {};
        const poisB = loadedPoisByPointKey[b.key] || {};
        const categories = Array.from(new Set([...Object.keys(poisA), ...Object.keys(poisB)])).sort();
        const countData = categories.map((cat) => {
            const listA = (poisA[cat] || [])
                .map((p) => ({ ...p, distance_km: Number(haversineKm(a.point.lat, a.point.lng, p.lat, p.lng).toFixed(3)) }))
                .filter((p) => p.distance_km <= MAX_RADIUS_KM)
                .filter((p) => p.name.toLowerCase().includes(searchQuery.toLowerCase()));
            const listB = (poisB[cat] || [])
                .map((p) => ({ ...p, distance_km: Number(haversineKm(b.point.lat, b.point.lng, p.lat, p.lng).toFixed(3)) }))
                .filter((p) => p.distance_km <= MAX_RADIUS_KM)
                .filter((p) => p.name.toLowerCase().includes(searchQuery.toLowerCase()));
            return { name: cat, A: listA.length, B: listB.length, delta: listA.length - listB.length };
        });
        const avgData = categories.map((cat) => {
            const listA = (poisA[cat] || [])
                .map((p) => ({ ...p, distance_km: Number(haversineKm(a.point.lat, a.point.lng, p.lat, p.lng).toFixed(3)) }))
                .filter((p) => p.distance_km <= MAX_RADIUS_KM)
                .filter((p) => p.name.toLowerCase().includes(searchQuery.toLowerCase()));
            const listB = (poisB[cat] || [])
                .map((p) => ({ ...p, distance_km: Number(haversineKm(b.point.lat, b.point.lng, p.lat, p.lng).toFixed(3)) }))
                .filter((p) => p.distance_km <= MAX_RADIUS_KM)
                .filter((p) => p.name.toLowerCase().includes(searchQuery.toLowerCase()));
            const sumA = listA.reduce((acc, p) => acc + getDecayedWeight(p), 0);
            const sumB = listB.reduce((acc, p) => acc + getDecayedWeight(p), 0);
            const avgA = listA.length ? sumA / listA.length : 0;
            const avgB = listB.length ? sumB / listB.length : 0;
            return { name: cat, A: Number(avgA) || 0, B: Number(avgB) || 0, delta: avgA - avgB };
        });
        return { countData, avgData };
    }, [viewMode, selectedTargets, loadedPoisByPointKey, MAX_RADIUS_KM, searchQuery]);

    const compareCommonByCategory = useMemo(() => {
        if (viewMode !== "compare" || selectedTargets.length < 2) return null;
        const [a, b] = selectedTargets;
        const poisA = loadedPoisByPointKey[a.key] || {};
        const poisB = loadedPoisByPointKey[b.key] || {};
        const keyFor = (poi: Poi) => `${(poi.name || "").toLowerCase()}|${poi.lat.toFixed(6)}|${poi.lng.toFixed(6)}`;
        const result: Record<string, CommonPoi[]> = {};

        Object.entries(poisA).forEach(([cat, listA]) => {
            const listB = poisB[cat] || [];
            const mapB = new Map<string, Poi>();
            listB.forEach((p) => {
                const distB = haversineKm(b.point.lat, b.point.lng, p.lat, p.lng);
                if (distB <= MAX_RADIUS_KM) {
                    mapB.set(keyFor(p), { ...p, distance_km: Number(distB.toFixed(3)) });
                }
            });

            listA.forEach((pA) => {
                const distA = haversineKm(a.point.lat, a.point.lng, pA.lat, pA.lng);
                if (distA > MAX_RADIUS_KM) return;
                const key = keyFor(pA);
                const matchB = mapB.get(key);
                if (!matchB) return;
                const weightA = Number(pA.weight) || 0;
                const weightB = Number(matchB.weight) || 0;
                const distanceA = Number(distA.toFixed(3));
                const distanceB = Number((matchB.distance_km ?? distA).toFixed(3));
                const decayedA = weightA * Math.exp(-distanceA / DECAY_SCALE_KM);
                const decayedB = weightB * Math.exp(-distanceB / DECAY_SCALE_KM);
                const common: CommonPoi = {
                    key,
                    name: pA.name || matchB.name || "",
                    lat: pA.lat,
                    lng: pA.lng,
                    weightA,
                    weightB,
                    distanceA,
                    distanceB,
                    decayedA,
                    decayedB,
                    rawA: pA.raw,
                    rawB: matchB.raw,
                    subcategory: pA.subcategory || matchB.subcategory,
                    cat
                };
                result[cat] = (result[cat] || []).concat(common);
            });
        });

        return result;
    }, [viewMode, selectedTargets, loadedPoisByPointKey, MAX_RADIUS_KM, DECAY_SCALE_KM]);

    const commonCategoryCounts = useMemo(() => {
        if (!compareCommonByCategory) return {} as Record<string, number>;
        const counts: Record<string, number> = {};
        let total = 0;
        Object.entries(compareCommonByCategory).forEach(([cat, list]) => {
            const filteredList = list.filter((p) => p.name.toLowerCase().includes(searchQuery.toLowerCase()));
            counts[cat] = filteredList.length;
            total += filteredList.length;
        });
        counts["All"] = total;
        return counts;
    }, [compareCommonByCategory, searchQuery]);

    const commonCategoryTotals = useMemo(() => {
        if (!compareCommonByCategory) return {} as Record<string, number>;
        const totals: Record<string, number> = {};
        Object.entries(compareCommonByCategory).forEach(([cat, list]) => {
            const filteredList = list.filter((p) => p.name.toLowerCase().includes(searchQuery.toLowerCase()));
            totals[cat] = filteredList.reduce((acc, poi) => acc + (poi.decayedA + poi.decayedB), 0);
        });
        return totals;
    }, [compareCommonByCategory, searchQuery]);

    const commonCategoryAverages = useMemo(() => {
        if (!compareCommonByCategory) return {} as Record<string, number>;
        const averages: Record<string, number> = {};
        let totalCount = 0;
        let totalSum = 0;
        Object.entries(compareCommonByCategory).forEach(([cat, list]) => {
            const filteredList = list.filter((p) => p.name.toLowerCase().includes(searchQuery.toLowerCase()));
            if (filteredList.length === 0) {
                averages[cat] = 0;
                return;
            }
            const sum = filteredList.reduce((acc, p) => acc + (p.decayedA + p.decayedB), 0);
            averages[cat] = sum / (filteredList.length * 2);
            totalCount += filteredList.length;
            totalSum += sum;
        });
        averages["All"] = totalCount > 0 ? totalSum / (totalCount * 2) : 0;
        return averages;
    }, [compareCommonByCategory, searchQuery]);

    const commonAllTotalDecayed = useMemo(() => {
        if (!compareCommonByCategory) return 0;
        return Object.values(commonCategoryTotals).reduce((acc, v) => acc + v, 0);
    }, [compareCommonByCategory, commonCategoryTotals]);

    const displayCategoryCounts = viewMode === "compare" && compareCommonByCategory
        ? commonCategoryCounts
        : categoryCounts;
    const displayCategoryAverages = viewMode === "compare" && compareCommonByCategory
        ? commonCategoryAverages
        : categoryDecayedAverages;

    const pointSummaries = useMemo(() => {
        if (points.length === 0) {
            return [] as Array<{
                key: string;
                point: Point;
                totalScore: number;
                perCategory: Array<{ cat: string; topPois: Array<Poi & { decayed_weight: number }>; score: number }>;
            }>;
        }

        return selectedTargets.map((t) => {
            const poisForPoint = loadedPoisByPointKey[t.key] || {};
            const perCategory: Array<{ cat: string; topPois: Array<Poi & { decayed_weight: number }>; score: number }> = [];
            let totalScore = 0;

            Object.entries(poisForPoint).forEach(([cat, list]) => {
                const within = list
                    .map((poi) => ({
                        ...poi,
                        distance_km: Number(haversineKm(t.point.lat, t.point.lng, poi.lat, poi.lng).toFixed(3))
                    }))
                    .filter((poi) => poi.distance_km <= MAX_RADIUS_KM)
                    .sort((a, b) => {
                        const aw = Number(a.weight) || 0;
                        const bw = Number(b.weight) || 0;
                        const ad = Number(a.distance_km) || 0;
                        const bd = Number(b.distance_km) || 0;
                        const aScore = aw * Math.exp(-ad / DECAY_SCALE_KM);
                        const bScore = bw * Math.exp(-bd / DECAY_SCALE_KM);
                        return bScore - aScore;
                    });

                const topPois = within.slice(0, 20).map((poi) => {
                    const w = Number(poi.weight) || 0;
                    const d = Number(poi.distance_km) || 0;
                    const decayed_weight = w * Math.exp(-d / DECAY_SCALE_KM);
                    return { ...poi, decayed_weight };
                });
                const score = topPois.reduce((acc, poi) => acc + (Number(poi.decayed_weight) || 0), 0);
                totalScore += score;
                perCategory.push({ cat, topPois, score });
            });

            return {
                key: t.key,
                point: t.point,
                totalScore,
                perCategory
            };
        });
    }, [loadedPoisByPointKey, selectedTargets, points.length, MAX_RADIUS_KM, DECAY_SCALE_KM]);

    const singleSummary = useMemo(() => {
        return pointSummaries.find((s) => s.key === selectedPointKey) || null;
    }, [pointSummaries, selectedPointKey]);

    const canGenerateAi = useMemo(() => {
        const hasScore = selectedTargets.some((t) => t.accessibility != null && Number.isFinite(Number(t.accessibility)));
        const hasPoisForAll = selectedTargets.every((t) => loadedPoisByPointKey[t.key] != null);
        return hasScore && hasPoisForAll && pointSummaries.length > 0;
    }, [selectedTargets, loadedPoisByPointKey, pointSummaries.length]);

    const handleGenerateAi = async () => {
        if (!canGenerateAi || aiLoading) return;
        const controller = new AbortController();
        try {
            setAiLoading(true);
            setAiError("");
            const preferred = pointSummaries.reduce<{ key: string; totalScore: number } | null>((best, cur) => {
                if (!best) return { key: cur.key, totalScore: cur.totalScore };
                return cur.totalScore > best.totalScore ? { key: cur.key, totalScore: cur.totalScore } : best;
            }, null);
            const payload = {
                preferred_point_key: preferred?.key ?? pointSummaries[0]?.key ?? null,
                radius_km: MAX_RADIUS_KM,
                decay_scale_km: DECAY_SCALE_KM,
                points: pointSummaries.map((s) => ({
                    key: s.key,
                    lat: s.point.lat,
                    lng: s.point.lng,
                    total_score: s.totalScore,
                    per_category: s.perCategory.map((c) => ({
                        cat: c.cat,
                        score: c.score,
                        top_pois: c.topPois.map((p) => ({
                            name: p.name,
                            distance_km: p.distance_km,
                            weight: p.weight,
                            decayed_weight: p.decayed_weight,
                            avg_weight_value: p.decayed_weight,
                            subcategory: p.subcategory || null
                        }))
                    }))
                }))
            };
            const cacheKey = JSON.stringify(payload);
            const cached = aiCacheRef.current.get(cacheKey);
            if (cached) {
                setAiExplanation(cached);
                return;
            }
            const cachedLocal = getCache<string>(`ai:${cacheKey}`);
            if (cachedLocal) {
                aiCacheRef.current.set(cacheKey, cachedLocal);
                setAiExplanation(cachedLocal);
                return;
            }
            const res = await fetch("http://127.0.0.1:8000/api/v1/explain/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload),
                signal: controller.signal
            });
            if (!res.ok) {
                const err = await res.json().catch(() => ({}));
                throw new Error(err?.detail || "Explanation request failed");
            }
            const data = await res.json();
            const explanation = (data?.explanation || "").trim();
            aiCacheRef.current.set(cacheKey, explanation);
            setCache(`ai:${cacheKey}`, explanation);
            setAiExplanation(explanation);
        } catch (err: unknown) {
            if ((err as { name?: string }).name !== "AbortError") {
                setAiError((err as Error).message || "Failed to generate explanation.");
            }
        } finally {
            setAiLoading(false);
        }
        return () => controller.abort();
    };

    return (
        <div style={{ padding: 20, fontFamily: "Inter, system-ui, Arial", background: "linear-gradient(135deg,#f8fafc 0%,#eef2ff 50%,#fff7ed 100%)", minHeight: "100vh", color: "#0f172a" }}>
            <style>{`
                @keyframes floatIn { 0% { opacity: 0; transform: translateY(8px); } 100% { opacity: 1; transform: translateY(0); } }
                @keyframes pulseGlow { 0% { box-shadow: 0 0 0 rgba(99,102,241,0.0);} 50% { box-shadow: 0 0 24px rgba(99,102,241,0.25);} 100% { box-shadow: 0 0 0 rgba(99,102,241,0.0);} }
                .ytm-tabs { display: flex; gap: 24px; align-items: center; border-bottom: 1px solid rgba(15,23,42,0.08); margin: 16px 0 6px; }
                .ytm-tab { background: transparent; border: none; padding: 10px 0; color: #64748b; font-weight: 800; font-size: 12px; letter-spacing: 0.08em; text-transform: uppercase; cursor: pointer; position: relative; }
                .ytm-tab.active { color: #0f172a; }
                .ytm-tab.active::after { content: ""; position: absolute; left: 0; right: 0; bottom: -1px; height: 2px; background: #0f172a; }
            `}</style>
            <div style={{ maxWidth: 1150, margin: "0 auto" }}>
                {/* <div style={{ background: "#ffffff", padding: 20, borderRadius: 14, border: "1px solid rgba(15,23,42,0.06)", boxShadow: "0 10px 30px rgba(15,23,42,0.06)", animation: "floatIn 0.4s ease" }}>
                    <h1 style={{ margin: 0, color: '#0f172a' }}>{name || "Place"} — Analysis</h1>
                    {points.length > 1 ? (
                        <div style={{ color: "#475569", marginTop: 6 }}>{`points: ${points.length} · center: ${centerLat.toFixed(6)} · ${centerLng.toFixed(6)}`}</div>
                    ) : (
                        <div style={{ color: "#475569", marginTop: 6 }}>{`lat: ${centerLat.toFixed(6)} · lng: ${centerLng.toFixed(6)}`}</div>
                    )}
                    <div style={{ color: "#94a3b8", fontSize: 12, marginTop: 4 }}>{`mode: ${mode} · pick: ${pick}`}</div>
                    {points.length <= 1 && (
                        <>
                            <div style={{ marginTop: 12 }}>
                                <div style={{ fontSize: 13, color: "#475569" }}>Accessibility Score</div>
                                <div style={{ height: 14, background: "#f1f5f9", borderRadius: 8, marginTop: 6 }}>
                                    <div style={{ height: 14, width: `${Math.min((averageScore ?? primaryAccessibility ?? 0) || 0, 100)}%`, background: "linear-gradient(90deg,#16a34a,#06b6d4)", borderRadius: 8, transition: "width 0.6s", animation: "pulseGlow 2.2s ease-in-out infinite" }} />
                                </div>
                                <div style={{ marginTop: 6, color: '#0f172a' }}>
                                    {averageScore != null ? averageScore.toFixed(1) : (primaryAccessibility != null ? primaryAccessibility.toFixed(1) : "Calculating...")}
                                </div>
                            </div>
                            <div style={{ marginTop: 12 }}>
                                <div style={{ fontSize: 13, color: "#475569" }}>Model Prediction Score</div>
                                <div style={{ height: 14, background: "#f1f5f9", borderRadius: 8, marginTop: 6 }}>
                                    <div
                                        style={{
                                            height: 14,
                                            width: `${Math.min(getPredictionDisplayScore(averagePrediction ?? primaryPrediction?.score) ?? 0, PREDICTION_DISPLAY_MAX)}%`,
                                            background: "linear-gradient(90deg,#f97316,#ef4444)",
                                            borderRadius: 8,
                                            transition: "width 0.6s"
                                        }}
                                    />
                                </div>
                                <div style={{ marginTop: 6, color: '#0f172a' }}>
                                    {averagePrediction != null
                                        ? (getPredictionDisplayScore(averagePrediction) ?? 0).toFixed(1)
                                        : (primaryPrediction ? (getPredictionDisplayScore(primaryPrediction.score) ?? 0).toFixed(1) : "Calculating...")}
                                </div>
                                {primaryPrediction?.risk_level && (
                                    <div style={{ fontSize: 12, color: "#475569", marginTop: 2 }}>
                                        Risk: {primaryPrediction.risk_level}
                                    </div>
                                )}
                            </div>
                        </>
                    )}
                    {points.length > 1 && (
                        <div style={{ marginTop: 10, fontSize: 12, color: "#475569" }}>
                            {points.map((p: Point, idx: number) => {
                                const key = `${p.lat.toFixed(6)},${p.lng.toFixed(6)}`;
                                const score = accessibilityScores[key];
                                const prediction = predictionScores[key];
                                const predictionDisplay = getPredictionDisplayScore(prediction?.score);
                                return (
                                    <div key={key} style={{ display: 'flex', justifyContent: 'space-between', gap: 8 }}>
                                        <span>{`${idx + 1}. ${p.lat.toFixed(6)}, ${p.lng.toFixed(6)}`}</span>
                                        <span style={{ color: '#0f172a', fontWeight: 600 }}>
                                            {Number.isFinite(score) ? score.toFixed(1) : "…"}
                                        </span>
                                        <span style={{ color: '#0f172a', fontWeight: 600 }}>
                                            {predictionDisplay != null ? predictionDisplay.toFixed(1) : "…"}
                                        </span>
                                    </div>
                                );
                            })}
                        </div>
                    )}
                </div> */}

                {points.length > 0 && (
                    <div style={{ background: "#ffffff", padding: 18, borderRadius: 12, border: "1px solid rgba(15,23,42,0.06)", marginTop: 12, boxShadow: "0 6px 18px rgba(15,23,42,0.05)", animation: "floatIn 0.5s ease" }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: 12, flexWrap: 'wrap' }}>
                            <h3 style={{ marginTop: 0, marginBottom: 0 }}>Selected Point</h3>
                            {points.length > 1 && (
                                <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap' }}>
                                    <button
                                        onClick={() => setViewMode("single")}
                                        style={{
                                            padding: '4px 10px',
                                            borderRadius: 14,
                                            border: '1px solid #e2e8f0',
                                            background: viewMode === 'single' ? '#0f172a' : '#ffffff',
                                            color: viewMode === 'single' ? '#ffffff' : '#64748b',
                                            fontSize: 12,
                                            cursor: 'pointer',
                                            fontWeight: 600
                                        }}
                                    >
                                        Single
                                    </button>
                                    <button
                                        onClick={() => {
                                            setViewMode("compare");
                                            setComparePointIdxA((prev) => Math.min(Math.max(0, prev), Math.max(0, points.length - 1)));
                                            setComparePointIdxB((prev) => {
                                                const clamped = Math.min(Math.max(0, prev), Math.max(0, points.length - 1));
                                                if (clamped === comparePointIdxA) return comparePointIdxA === 0 ? 1 : 0;
                                                return clamped;
                                            });
                                        }}
                                        style={{
                                            padding: '4px 10px',
                                            borderRadius: 14,
                                            border: '1px solid #e2e8f0',
                                            background: viewMode === 'compare' ? '#0f172a' : '#ffffff',
                                            color: viewMode === 'compare' ? '#ffffff' : '#64748b',
                                            fontSize: 12,
                                            cursor: 'pointer',
                                            fontWeight: 600
                                        }}
                                    >
                                        Compare
                                    </button>
                                </div>
                            )}
                        </div>

                        {viewMode === 'single' && (
                            <>
                                {selectedPointMeta && (
                                    <div style={{ marginTop: 10, display: 'flex', gap: 12, alignItems: 'center', background: '#f8fafc', border: '1px solid #e2e8f0', borderRadius: 10, padding: 10 }}>
                                        {selectedPointMeta.image && (
                                            <img
                                                src={selectedPointMeta.image}
                                                alt={selectedPointMeta.label}
                                                style={{ width: 72, height: 72, borderRadius: 10, objectFit: 'cover' }}
                                            />
                                        )}
                                        <div>
                                            <div style={{ fontWeight: 800 }}>{selectedPointMeta.label}</div>
                                            {selectedPointMeta.entry?.ratePerMonth != null && (
                                                <div style={{ fontSize: 12, color: '#475569', marginTop: 2 }}>{`Rs ${selectedPointMeta.entry.ratePerMonth.toLocaleString()} / month`}</div>
                                            )}
                                            <div style={{ fontSize: 12, color: '#64748b' }}>{selectedPointKey}</div>
                                        </div>
                                    </div>
                                )}
                                {points.length > 1 && (
                                    <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap', marginBottom: 10, marginTop: 10 }}>
                                        {points.map((p: Point, idx: number) => (
                                            <button
                                                key={`pt-top-${idx}`}
                                                onClick={() => setSelectedPointIdx(idx)}
                                                title={pointMeta[idx]?.label || `P${idx + 1}`}
                                                style={{
                                                    padding: '4px 10px',
                                                    borderRadius: 14,
                                                    border: '1px solid #e2e8f0',
                                                    background: selectedPointIdx === idx ? '#0f172a' : '#ffffff',
                                                    color: selectedPointIdx === idx ? '#ffffff' : '#64748b',
                                                    fontSize: 12,
                                                    cursor: 'pointer',
                                                    fontWeight: 600
                                                }}
                                            >
                                                {pointMeta[idx]?.label || `P${idx + 1}`}
                                            </button>
                                        ))}
                                    </div>
                                )}
                            </>
                        )}

                        {viewMode === 'compare' && points.length > 1 && (
                            <>
                                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: 12, marginTop: 12 }}>
                                    {[
                                        { label: 'A', idx: comparePointIdxA },
                                        { label: 'B', idx: comparePointIdxB }
                                    ].map((item) => {
                                        const meta = pointMeta[item.idx];
                                        if (!meta) return null;
                                        return (
                                            <div key={`compare-meta-${item.label}`} style={{ border: '1px solid #e2e8f0', borderRadius: 10, padding: 10, background: '#f8fafc', display: 'flex', gap: 10, alignItems: 'center' }}>
                                                {meta.image && (
                                                    <img
                                                        src={meta.image}
                                                        alt={meta.label}
                                                        style={{ width: 64, height: 64, borderRadius: 10, objectFit: 'cover' }}
                                                    />
                                                )}
                                                <div style={{ flex: 1 }}>
                                                    <div style={{ fontSize: 12, color: '#64748b', fontWeight: 700 }}>{item.label}</div>
                                                    <div style={{ fontWeight: 800 }}>{meta.label}</div>
                                                    {meta.entry?.ratePerMonth != null && (
                                                        <div style={{ fontSize: 12, color: '#475569', marginTop: 2 }}>{`Rs ${meta.entry.ratePerMonth.toLocaleString()} / month`}</div>
                                                    )}
                                                    <div style={{ fontSize: 11, color: '#94a3b8', marginTop: 2 }}>{meta.key}</div>
                                                </div>
                                            </div>
                                        );
                                    })}
                                </div>
                                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: 12, marginTop: 12 }}>
                                    <div>
                                        {/* <div style={{ fontSize: 12, color: '#64748b', fontWeight: 700, marginBottom: 6 }}>A</div> */}
                                        <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap' }}>
                                            {points.map((p: Point, idx: number) => (
                                                <button
                                                    key={`pt-a-${idx}`}
                                                    onClick={() => {
                                                        setComparePointIdxA(idx);
                                                        setSelectedPointIdx(idx);
                                                        if (idx === comparePointIdxB) {
                                                            setComparePointIdxB(idx === 0 ? 1 : 0);
                                                        }
                                                    }}
                                                    title={pointMeta[idx]?.label || `P${idx + 1}`}
                                                    style={{
                                                        padding: '4px 10px',
                                                        borderRadius: 14,
                                                        border: '1px solid #e2e8f0',
                                                        background: comparePointIdxA === idx ? '#0f172a' : '#ffffff',
                                                        color: comparePointIdxA === idx ? '#ffffff' : '#64748b',
                                                        fontSize: 12,
                                                        cursor: 'pointer',
                                                        fontWeight: 600
                                                    }}
                                                >
                                                    {pointMeta[idx]?.label || `P${idx + 1}`}
                                                </button>
                                            ))}
                                        </div>
                                    </div>
                                    <div>
                                        {/* <div style={{ fontSize: 12, color: '#64748b', fontWeight: 700, marginBottom: 6 }}>B</div> */}
                                        <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap' }}>
                                            {points.map((p: Point, idx: number) => (
                                                <button
                                                    key={`pt-b-${idx}`}
                                                    onClick={() => {
                                                        setComparePointIdxB(idx);
                                                        if (idx === comparePointIdxA) {
                                                            const nextA = idx === 0 ? 1 : 0;
                                                            setComparePointIdxA(nextA);
                                                            setSelectedPointIdx(nextA);
                                                        }
                                                    }}
                                                    title={pointMeta[idx]?.label || `P${idx + 1}`}
                                                    style={{
                                                        padding: '4px 10px',
                                                        borderRadius: 14,
                                                        border: '1px solid #e2e8f0',
                                                        background: comparePointIdxB === idx ? '#0f172a' : '#ffffff',
                                                        color: comparePointIdxB === idx ? '#ffffff' : '#64748b',
                                                        fontSize: 12,
                                                        cursor: 'pointer',
                                                        fontWeight: 600
                                                    }}
                                                >
                                                    {pointMeta[idx]?.label || `P${idx + 1}`}
                                                </button>
                                            ))}
                                        </div>
                                    </div>
                                </div>
                            </>
                        )}
                    </div>
                )}

                {(viewMode === "single" || viewMode === "compare") && (
                    <div className="ytm-tabs">
                        <button
                            className={`ytm-tab ${(viewMode === "compare" ? comparePage : singlePage) === "insights" ? "active" : ""}`}
                            onClick={() => (viewMode === "compare" ? setComparePage("insights") : setSinglePage("insights"))}
                        >
                            Insights
                        </button>
                        <button
                            className={`ytm-tab ${(viewMode === "compare" ? comparePage : singlePage) === "nearby" ? "active" : ""}`}
                            onClick={() => (viewMode === "compare" ? setComparePage("nearby") : setSinglePage("nearby"))}
                        >
                            Nearby Pois
                        </button>
                        <button
                            className={`ytm-tab ${(viewMode === "compare" ? comparePage : singlePage) === "explain" ? "active" : ""}`}
                            onClick={() => (viewMode === "compare" ? setComparePage("explain") : setSinglePage("explain"))}
                        >
                            Explanation
                        </button>
                    </div>
                )}

                {((viewMode === "compare" && comparePage === "insights") || (viewMode === "single" && singlePage === "insights")) && (
                    <div style={{ background: "#ffffff", padding: 18, borderRadius: 12, border: "1px solid rgba(15,23,42,0.06)", marginTop: 12, boxShadow: "0 6px 18px rgba(15,23,42,0.05)", animation: "floatIn 0.5s ease" }}>
                        {/* <h3 style={{ marginTop: 0 }}>Insights</h3> */}
                        {viewMode === "single" && (
                            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: 12, marginBottom: 12 }}>
                                {renderScoreRing(
                                    clampPct(selectedAccessibility),
                                    'Accessibility Score',
                                    'Access',
                                    '#16a34a'
                                )}
                                {renderScoreRing(
                                    clampPct(getPredictionDisplayScore(selectedPrediction?.score)),
                                    'Model Prediction Score',
                                    'Prediction',
                                    '#f97316'
                                )}
                                {renderScoreRing(
                                    getPoiScorePercent(singleSummary?.totalScore),
                                    'POI Score',
                                    // singleSummary ? `${singleSummary.totalScore.toFixed(2)} / ${POI_SCORE_MAX}` : 'POI score',
                                    'POI score',
                                    '#6366f1'
                                )}
                            </div>
                        )}
                        {viewMode === "compare" && (
                            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: 12, marginBottom: 12 }}>
                                {selectedTargets.map((t) => {
                                    const summary = pointSummaries.find((s) => s.key === t.key) || null;
                                    const poiPct = getPoiScorePercent(summary?.totalScore);
                                    const label = pointMeta[t.idx]?.label || `P${t.idx + 1}`;
                                    return (
                                        <div key={`compare-insights-${t.key}`} style={{ border: '1px solid #e2e8f0', borderRadius: 12, padding: 12, background: "#f8fafc" }}>
                                            <div style={{ fontWeight: 800, marginBottom: 6 }}>{`${t.label}: ${label}`}</div>
                                            <div style={{ fontWeight: 700, fontSize: 12, color: '#475569' }}>Accessibility</div>
                                            <div style={{ height: 10, background: "#f1f5f9", borderRadius: 6, marginTop: 6 }}>
                                                <div style={{ height: 10, width: `${Math.min(Number(t.accessibility ?? 0) || 0, 100)}%`, background: "linear-gradient(90deg,#16a34a,#06b6d4)", borderRadius: 6, transition: "width 0.5s" }} />
                                            </div>
                                            <div style={{ marginTop: 6, fontWeight: 800 }}>
                                                {t.accessibility != null && Number.isFinite(Number(t.accessibility)) ? Number(t.accessibility).toFixed(1) : "Calculating..."}
                                            </div>

                                            <div style={{ fontWeight: 700, fontSize: 12, color: '#475569', marginTop: 10 }}>Prediction</div>
                                            <div style={{ height: 10, background: "#f1f5f9", borderRadius: 6, marginTop: 6 }}>
                                                <div style={{ height: 10, width: `${Math.min(getPredictionDisplayScore(t.prediction?.score) ?? 0, PREDICTION_DISPLAY_MAX)}%`, background: "linear-gradient(90deg,#f97316,#ef4444)", borderRadius: 6, transition: "width 0.5s" }} />
                                            </div>
                                            <div style={{ marginTop: 6, fontWeight: 800 }}>
                                                {t.prediction ? (getPredictionDisplayScore(t.prediction.score) ?? 0).toFixed(1) : "Calculating..."}
                                            </div>
                                            {t.prediction?.risk_level && (
                                                <div style={{ color: '#64748b', fontSize: 12, marginTop: 2 }}>
                                                    Risk: {t.prediction.risk_level}
                                                </div>
                                            )}

                                            <div style={{ fontWeight: 700, fontSize: 12, color: '#475569', marginTop: 10 }}>POI Score</div>
                                            <div style={{ height: 10, background: "#f1f5f9", borderRadius: 6, marginTop: 6 }}>
                                                <div style={{ height: 10, width: `${Math.min(poiPct ?? 0, 100)}%`, background: "linear-gradient(90deg,#6366f1,#8b5cf6)", borderRadius: 6, transition: "width 0.5s" }} />
                                            </div>
                                            <div style={{ marginTop: 6, fontWeight: 800 }}>
                                                {/* {summary ? `${summary.totalScore.toFixed(2)} / ${POI_SCORE_MAX} (${Math.round(poiPct ?? 0)}%)` : "Calculating..."} */}
                                                {summary ? `${Math.round(poiPct ?? 0)}` : "Calculating..."}
                                            </div>
                                        </div>
                                    );
                                })}
                            </div>
                        )}
                        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(260px, 1fr))", gap: 14 }}>
                            {viewMode === "compare" && compareCategoryStats ? (
                                <>
                                    <div style={{ border: "1px solid #e2e8f0", borderRadius: 12, padding: 12, background: "#f8fafc" }}>
                                        <div style={{ fontWeight: 700, marginBottom: 6 }}>POI Counts (A vs B)</div>
                                        {compareCategoryStats.countData.length === 0 ? (
                                            <div style={{ fontSize: 12, color: "#94a3b8" }}>No POIs loaded yet.</div>
                                        ) : (
                                            <div style={{ width: "100%", height: 220 }}>
                                                <ResponsiveContainer>
                                                    <BarChart data={compareCategoryStats.countData} margin={{ top: 10, right: 10, left: 0, bottom: 5 }}>
                                                        <CartesianGrid strokeDasharray="3 3" />
                                                        <XAxis dataKey="name" tick={{ fontSize: 11 }} />
                                                        <YAxis tick={{ fontSize: 11 }} />
                                                        <Tooltip />
                                                        <Legend />
                                                        <Bar dataKey="A" fill="#3b82f6" radius={[8, 8, 0, 0]} isAnimationActive animationDuration={900} />
                                                        <Bar dataKey="B" fill="#f97316" radius={[8, 8, 0, 0]} isAnimationActive animationDuration={900} />
                                                    </BarChart>
                                                </ResponsiveContainer>
                                            </div>
                                        )}
                                    </div>

                                    <div style={{ border: "1px solid #e2e8f0", borderRadius: 12, padding: 12, background: "#f8fafc" }}>
                                        <div style={{ fontWeight: 700, marginBottom: 6 }}>Avg Decayed Weight (A vs B)</div>
                                        {compareCategoryStats.avgData.length === 0 ? (
                                            <div style={{ fontSize: 12, color: "#94a3b8" }}>No POIs loaded yet.</div>
                                        ) : (
                                            <div style={{ width: "100%", height: 220 }}>
                                                <ResponsiveContainer>
                                                    <BarChart data={compareCategoryStats.avgData} margin={{ top: 10, right: 10, left: 0, bottom: 5 }}>
                                                        <CartesianGrid strokeDasharray="3 3" />
                                                        <XAxis dataKey="name" tick={{ fontSize: 11 }} />
                                                        <YAxis tick={{ fontSize: 11 }} />
                                                        <Tooltip />
                                                        <Legend />
                                                        <Bar dataKey="A" fill="#3b82f6" radius={[8, 8, 0, 0]} isAnimationActive animationDuration={900} />
                                                        <Bar dataKey="B" fill="#f97316" radius={[8, 8, 0, 0]} isAnimationActive animationDuration={900} />
                                                    </BarChart>
                                                </ResponsiveContainer>
                                            </div>
                                        )}
                                    </div>
                                </>
                            ) : (
                                <>
                                    <div style={{ border: "1px solid #e2e8f0", borderRadius: 12, padding: 12, background: "#f8fafc" }}>
                                        <div style={{ fontWeight: 700, marginBottom: 6 }}>POI Category Share</div>
                                        {categoryPieData.length === 0 ? (
                                            <div style={{ fontSize: 12, color: "#94a3b8" }}>No POIs loaded yet.</div>
                                        ) : (
                                            <div style={{ width: "100%", height: 220 }}>
                                                <ResponsiveContainer>
                                                    <PieChart>
                                                        <Pie
                                                            data={categoryPieData}
                                                            dataKey="value"
                                                            nameKey="name"
                                                            innerRadius={50}
                                                            outerRadius={85}
                                                            paddingAngle={4}
                                                            isAnimationActive
                                                            animationDuration={900}
                                                        >
                                                            {categoryPieData.map((entry) => (
                                                                <Cell key={entry.name} fill={chartColors[entry.name as keyof typeof chartColors] || "#94a3b8"} />
                                                            ))}
                                                        </Pie>
                                                        <Tooltip />
                                                        <Legend />
                                                    </PieChart>
                                                </ResponsiveContainer>
                                            </div>
                                        )}
                                    </div>

                                    <div style={{ border: "1px solid #e2e8f0", borderRadius: 12, padding: 12, background: "#f8fafc" }}>
                                        <div style={{ fontWeight: 700, marginBottom: 6 }}>Avg Decayed Weight by Category</div>
                                        {categoryAvgData.length === 0 ? (
                                            <div style={{ fontSize: 12, color: "#94a3b8" }}>No POIs loaded yet.</div>
                                        ) : (
                                            <div style={{ width: "100%", height: 220 }}>
                                                <ResponsiveContainer>
                                                    <BarChart data={categoryAvgData} margin={{ top: 10, right: 10, left: 0, bottom: 5 }}>
                                                        <CartesianGrid strokeDasharray="3 3" />
                                                        <XAxis dataKey="name" tick={{ fontSize: 11 }} />
                                                        <YAxis tick={{ fontSize: 11 }} />
                                                        <Tooltip />
                                                        <Bar dataKey="value" fill="#6366f1" radius={[8, 8, 0, 0]} isAnimationActive animationDuration={900} />
                                                    </BarChart>
                                                </ResponsiveContainer>
                                            </div>
                                        )}
                                    </div>
                                </>
                            )}
                        </div>
                        <div style={{ marginTop: 16, border: "1px solid #e2e8f0", borderRadius: 12, overflow: "hidden", background: "#f8fafc" }}>
                            {/* <div style={{ padding: "10px 12px", fontWeight: 700, borderBottom: "1px solid #e2e8f0" }}>
                                Location Map
                            </div> */}
                            <div style={{ width: "100%", height: 260 }}>
                                {viewMode === "compare" && selectedTargets.length >= 2 ? (
                                    <MapContainer
                                        key={`insight-map-compare-${comparePointIdxA}-${comparePointIdxB}`}
                                        center={[
                                            (selectedTargets[0].point.lat + selectedTargets[1].point.lat) / 2,
                                            (selectedTargets[0].point.lng + selectedTargets[1].point.lng) / 2
                                        ]}
                                        zoom={15}
                                        style={{ width: "100%", height: "100%" }}
                                        scrollWheelZoom={false}
                                    >
                                        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
                                        <Marker
                                            key={`insight-compare-a-${selectedTargets[0].key}`}
                                            position={[selectedTargets[0].point.lat, selectedTargets[0].point.lng]}
                                            icon={compareMarkerA}
                                        />
                                        <Marker
                                            key={`insight-compare-b-${selectedTargets[1].key}`}
                                            position={[selectedTargets[1].point.lat, selectedTargets[1].point.lng]}
                                            icon={compareMarkerB}
                                        />
                                    </MapContainer>
                                ) : (
                                    <MapContainer
                                        key={`insight-map-${selectedPointKey}`}
                                        center={[selectedPoint.lat || 27.670587, selectedPoint.lng || 85.420868]}
                                        zoom={16}
                                        style={{ width: "100%", height: "100%" }}
                                        scrollWheelZoom={false}
                                    >
                                        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
                                        <Marker key={`insight-point-${selectedPointKey}`} position={[selectedPoint.lat, selectedPoint.lng]} />
                                    </MapContainer>
                                )}
                            </div>
                        </div>
                    </div>
                )}

                {((viewMode === "compare" && comparePage === "nearby") || (viewMode === "single" && singlePage === "nearby")) && (
                    <div style={{ display: "grid", gap: 12, marginTop: 12 }}>
                        <div style={{ background: "#ffffff", padding: 18, borderRadius: 12, border: "1px solid rgba(15,23,42,0.04)", boxShadow: "0 6px 18px rgba(15,23,42,0.05)", animation: "floatIn 0.5s ease" }}>
                            {/* <h3 style={{ marginTop: 0 }}>Map and POIs</h3> */}
                            <div style={{ display: 'flex', gap: 12 }}>
                                <div style={{ flex: 1 }}>
                                    <div style={{ width: '100%', aspectRatio: '1 / 1' }}>
                                        <MapContainer
                                            ref={(m: unknown) => { mapRef.current = m as L.Map | null; }}
                                            center={[selectedPoint.lat || 27.670587, selectedPoint.lng || 85.420868]}
                                            zoom={16}
                                            style={{ width: '100%', height: '100%', borderRadius: 8 }}
                                        >
                                            <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
                                            {/* selected points */}
                                            {viewMode === "compare" && selectedTargets.length >= 2 ? (
                                                <>
                                                    <Marker
                                                        key={`point-a-${selectedTargets[0].idx}`}
                                                        position={[selectedTargets[0].point.lat, selectedTargets[0].point.lng]}
                                                        icon={compareMarkerA}
                                                    />
                                                    <Marker
                                                        key={`point-b-${selectedTargets[1].idx}`}
                                                        position={[selectedTargets[1].point.lat, selectedTargets[1].point.lng]}
                                                        icon={compareMarkerB}
                                                    />
                                                </>
                                            ) : (
                                                <Marker key={`point-selected-${selectedPointKey}`} position={[selectedPoint.lat, selectedPoint.lng]} />
                                            )}
                                            {/* hover marker */}
                                            {hoverPos && <Marker position={[hoverPos.lat, hoverPos.lng]} />}
                                            {/* hover path (rendered inside MapContainer so Leaflet context is available) */}
                                            {viewMode !== "compare" && hoverPath && hoverPath.length > 0 && (
                                                <Polyline
                                                    positions={hoverPath.map(([la, lo]) => [la, lo])}
                                                    pathOptions={{
                                                        color: '#ff6b6b',
                                                        weight: 5,
                                                        dashArray: '10 8',
                                                        dashOffset: `${pathDashOffset}`,
                                                        opacity: pathOpacity
                                                    }}
                                                />
                                            )}
                                            {viewMode === "compare" && hoverPathA && hoverPathA.length > 0 && (
                                                <Polyline
                                                    positions={hoverPathA.map(([la, lo]) => [la, lo])}
                                                    pathOptions={{
                                                        color: '#3b82f6',
                                                        weight: 5,
                                                        dashArray: '10 8',
                                                        dashOffset: `${-pathDashOffset}`,
                                                        opacity: pathOpacity
                                                    }}
                                                />
                                            )}
                                            {viewMode === "compare" && hoverPathB && hoverPathB.length > 0 && (
                                                <Polyline
                                                    positions={hoverPathB.map(([la, lo]) => [la, lo])}
                                                    pathOptions={{
                                                        color: '#f97316',
                                                        weight: 5,
                                                        dashArray: '10 8',
                                                        dashOffset: `${-pathDashOffset}`,
                                                        opacity: pathOpacity
                                                    }}
                                                />
                                            )}
                                        </MapContainer>
                                    </div>
                                </div>

                                <div style={{ width: 360, maxHeight: '72vh', overflowY: 'auto', borderLeft: '1px solid rgba(15,23,42,0.04)', paddingLeft: 8, position: 'relative' }}>
                                    <div style={{ position: 'sticky', top: 0, background: '#ffffff', zIndex: 10, paddingBottom: 8, paddingTop: 0 }}>
                                        <div style={{ fontWeight: 700, marginBottom: 4 }}>Nearby POIs</div>
                                        <div style={{ fontSize: 13, color: '#64748b', marginBottom: 8 }}>{selectedPointMeta?.label || name}</div>

                                        <div style={{ marginBottom: 8 }}>
                                            <input
                                                type="text"
                                                placeholder="Search POIs..."
                                                value={searchQuery}
                                                onChange={(e) => setSearchQuery(e.target.value)}
                                                style={{ width: '100%', padding: '6px 10px', borderRadius: 6, border: '1px solid #e2e8f0', fontSize: 13 }}
                                            />
                                        </div>

                                        <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap' }}>
                                            {['All', 'Cafes', 'Education', 'Health', 'Temples', 'Bank', 'Other'].map(cat => (
                                                <button
                                                    key={cat}
                                                    onClick={() => setSelectedCategory(cat)}
                                                    style={{
                                                        padding: '4px 10px',
                                                        borderRadius: 16,
                                                        border: '1px solid #e2e8f0',
                                                        background: selectedCategory === cat ? '#0f172a' : '#ffffff',
                                                        color: selectedCategory === cat ? '#ffffff' : '#64748b',
                                                        fontSize: 12,
                                                        cursor: 'pointer',
                                                        fontWeight: 500
                                                    }}
                                                >
                                                    {cat}
                                                    <span style={{ opacity: 0.7, fontSize: 11, marginLeft: 6 }}>
                                                        {displayCategoryCounts[cat] || 0}
                                                    </span>
                                                    {/* <span style={{ opacity: 0.7, fontSize: 11, marginLeft: 6 }}>
                                                        avg: {(displayCategoryAverages[cat] || 0).toFixed(3)}
                                                    </span> */}
                                                </button>
                                            ))}
                                        </div>
                                    </div>

                                    {viewMode === "compare" && !compareCommonByCategory && <div>Loading...</div>}
                                    {viewMode === "compare" && compareCommonByCategory && Object.keys(compareCommonByCategory).length === 0 && (
                                        <div>No common POIs found within radius.</div>
                                    )}
                                    {viewMode === "compare" && compareCommonByCategory && selectedCategory === 'All' && (() => {
                                        const mixed = Object.entries(compareCommonByCategory).flatMap(([cat, list]) => {
                                            const filteredList = list
                                                .filter((p) => p.name.toLowerCase().includes(searchQuery.toLowerCase()))
                                                .map((p) => ({ poi: p, cat }));
                                            return filteredList;
                                        });
                                        const sorted = mixed
                                            .slice()
                                            .sort((a, b) => (b.poi.decayedA + b.poi.decayedB) - (a.poi.decayedA + a.poi.decayedB));
                                        if (sorted.length === 0) return null;
                                        return (
                                            <div key="All" style={{ marginBottom: 12 }}>
                                                <div style={{ fontWeight: 700, textTransform: 'capitalize', marginBottom: 6 }}>All (Common)</div>
                                                {sorted.map(({ poi: p, cat }, idx) => {
                                                    const pct = getCommonSharePct(p);
                                                    return (
                                                        <div key={`${cat}-${p.name}-${idx}`}
                                                            onMouseEnter={() => {
                                                                setHoverPos({ lat: p.lat, lng: p.lng });
                                                                setHoverPath(null);
                                                                setHoverPathA(getPathCoords(p.rawA));
                                                                setHoverPathB(getPathCoords(p.rawB));
                                                                try { mapRef.current?.flyTo([p.lat, p.lng], 17); } catch (err) { void err; }
                                                            }}
                                                            onMouseLeave={() => {
                                                                setHoverPos(null);
                                                                setHoverPath(null);
                                                                setHoverPathA(null);
                                                                setHoverPathB(null);
                                                                try { mapRef.current?.flyTo([selectedPoint.lat, selectedPoint.lng], 16); } catch (err) { void err; }
                                                            }}
                                                            style={{
                                                                display: 'flex',
                                                                gap: 8,
                                                                padding: 8,
                                                                borderRadius: 6,
                                                                alignItems: 'center',
                                                                cursor: 'pointer',
                                                                border: '1px solid rgba(15,23,42,0.03)',
                                                                marginBottom: 8,
                                                                background: `linear-gradient(90deg, rgba(59,130,246,0.18) ${pct}%, rgba(255,255,255,0) ${pct}%)`
                                                            }}>
                                                            <div style={{ flex: 1 }}>
                                                                <div style={{ fontWeight: 700 }}>{p.name}</div>
                                                                <div style={{ fontSize: 11, color: '#3b82f6', fontWeight: 600, textTransform: 'uppercase', marginTop: 2 }}>{cat}</div>
                                                                {p.subcategory && <div style={{ fontSize: 11, color: '#0ea5e9', fontWeight: 600, textTransform: 'uppercase', marginTop: 2 }}>{p.subcategory}</div>}
                                                                <div style={{ color: '#64748b', fontSize: 13 }}>{`${p.lat.toFixed(6)}, ${p.lng.toFixed(6)}`}</div>
                                                            </div>
                                                            <div style={{ textAlign: 'right' }}>
                                                                <div style={{ fontWeight: 800, fontSize: 13, color: '#3b82f6' }}>{`A: ${p.distanceA.toFixed(3)} km`}</div>
                                                                <div style={{ fontWeight: 800, fontSize: 13, color: '#f97316' }}>{`B: ${p.distanceB.toFixed(3)} km`}</div>
                                                            </div>
                                                        </div>
                                                    );
                                                })}
                                            </div>
                                        );
                                    })()}
                                    {viewMode === "compare" && compareCommonByCategory && selectedCategory !== 'All' && Object.entries(compareCommonByCategory)
                                        .filter(([cat]) => cat === selectedCategory)
                                        .map(([cat, list]) => {
                                            const filteredList = list
                                                .filter((p) => p.name.toLowerCase().includes(searchQuery.toLowerCase()))
                                                .slice()
                                                .sort((a, b) => (b.decayedA + b.decayedB) - (a.decayedA + a.decayedB));
                                            if (filteredList.length === 0) return null;
                                            return (
                                                <div key={cat} style={{ marginBottom: 12 }}>
                                                    <div style={{ fontWeight: 700, textTransform: 'capitalize', marginBottom: 6 }}>{cat} (Common)</div>
                                                    {filteredList.map((p, idx) => (
                                                        <div key={`${p.name}-${idx}`}
                                                            onMouseEnter={() => {
                                                                setHoverPos({ lat: p.lat, lng: p.lng });
                                                                setHoverPath(null);
                                                                setHoverPathA(getPathCoords(p.rawA));
                                                                setHoverPathB(getPathCoords(p.rawB));
                                                                try { mapRef.current?.flyTo([p.lat, p.lng], 17); } catch (err) { void err; }
                                                            }}
                                                            onMouseLeave={() => {
                                                                setHoverPos(null);
                                                                setHoverPath(null);
                                                                setHoverPathA(null);
                                                                setHoverPathB(null);
                                                                try { mapRef.current?.flyTo([selectedPoint.lat, selectedPoint.lng], 16); } catch (err) { void err; }
                                                            }}
                                                            style={{
                                                                display: 'flex',
                                                                gap: 8,
                                                                padding: 8,
                                                                borderRadius: 6,
                                                                alignItems: 'center',
                                                                cursor: 'pointer',
                                                                border: '1px solid rgba(15,23,42,0.03)',
                                                                marginBottom: 8,
                                                                background: (() => {
                                                                    const pct = getCommonCategorySharePct(p, cat);
                                                                    return `linear-gradient(90deg, rgba(59,130,246,0.18) ${pct}%, rgba(255,255,255,0) ${pct}%)`;
                                                                })()
                                                            }}>
                                                            <div style={{ flex: 1 }}>
                                                                <div style={{ fontWeight: 700 }}>{p.name}</div>
                                                                {p.subcategory && <div style={{ fontSize: 11, color: '#0ea5e9', fontWeight: 600, textTransform: 'uppercase', marginTop: 2 }}>{p.subcategory}</div>}
                                                                <div style={{ color: '#64748b', fontSize: 13 }}>{`${p.lat.toFixed(6)}, ${p.lng.toFixed(6)}`}</div>
                                                            </div>
                                                            <div style={{ textAlign: 'right' }}>
                                                                <div style={{ fontWeight: 800, fontSize: 13, color: '#3b82f6' }}>{`A: ${p.distanceA.toFixed(3)} km`}</div>
                                                                <div style={{ fontWeight: 800, fontSize: 13, color: '#f97316' }}>{`B: ${p.distanceB.toFixed(3)} km`}</div>
                                                            </div>
                                                        </div>
                                                    ))}
                                                </div>
                                            );
                                        })}

                                    {viewMode !== "compare" && !filteredPois && <div>Loading...</div>}
                                    {viewMode !== "compare" && filteredPois && Object.keys(filteredPois).length === 0 && <div>No POIs found within radius.</div>}
                                    {viewMode !== "compare" && filteredPois && selectedCategory === 'All' && (() => {
                                        const mixed = Object.entries(filteredPois).flatMap(([cat, list]) => {
                                            const filteredList = list
                                                .filter(p => p.name.toLowerCase().includes(searchQuery.toLowerCase()))
                                                .map((p) => ({ poi: p, cat }));
                                            return filteredList;
                                        });
                                        const sorted = mixed
                                            .slice()
                                            .sort((a, b) => getDecayedWeight(b.poi) - getDecayedWeight(a.poi));
                                        if (sorted.length === 0) return null;
                                        return (
                                            <div key="All" style={{ marginBottom: 12 }}>
                                                <div style={{ fontWeight: 700, textTransform: 'capitalize', marginBottom: 6 }}>All</div>
                                                {sorted.map(({ poi: p, cat }, idx) => {
                                                    const wEff = getDecayedWeight(p);
                                                    const pct = getAllSharePct(p);
                                                    return (
                                                        <div key={`${cat}-${p.name}-${idx}`}
                                                            onMouseEnter={() => {
                                                                setHoverPos({ lat: p.lat, lng: p.lng });
                                                                setHoverPathA(null);
                                                                setHoverPathB(null);
                                                                try { mapRef.current?.flyTo([p.lat, p.lng], 17); } catch (err) { void err; }
                                                                setHoverPath(getPathCoords(p.raw));
                                                            }}
                                                            onMouseLeave={() => {
                                                                setHoverPos(null);
                                                                setHoverPath(null);
                                                                setHoverPathA(null);
                                                                setHoverPathB(null);
                                                                try { mapRef.current?.flyTo([selectedPoint.lat, selectedPoint.lng], 16); } catch (err) { void err; }
                                                            }}
                                                            style={{
                                                                display: 'flex',
                                                                gap: 8,
                                                                padding: 8,
                                                                borderRadius: 6,
                                                                alignItems: 'center',
                                                                cursor: 'pointer',
                                                                border: '1px solid rgba(15,23,42,0.03)',
                                                                marginBottom: 8,
                                                                background: `linear-gradient(90deg, rgba(99,102,241,0.18) ${pct}%, rgba(255,255,255,0) ${pct}%)`
                                                            }}>
                                                            <div style={{ flex: 1 }}>
                                                                <div style={{ fontWeight: 700 }}>{p.name}</div>
                                                                <div style={{ fontSize: 11, color: '#6366f1', fontWeight: 600, textTransform: 'uppercase', marginTop: 2 }}>{cat}</div>
                                                                {p.subcategory && <div style={{ fontSize: 11, color: '#3b82f6', fontWeight: 600, textTransform: 'uppercase', marginTop: 2 }}>{p.subcategory}</div>}
                                                                <div style={{ color: '#64748b', fontSize: 13 }}>{`${p.lat.toFixed(6)}, ${p.lng.toFixed(6)}`}</div>
                                                            </div>
                                                            <div style={{ textAlign: 'right' }}>
                                                                {/* <div style={{ fontWeight: 800, fontSize: 14 }}>{`w*e^{-d/s}: ${wEff.toFixed(3)}`}</div> */}
                                                                <div style={{ fontWeight: 800, fontSize: 14 }}>{`${Number(p.distance_km).toFixed(3)} km`}</div>
                                                                {/* <div style={{ fontSize: 12, color: '#475569' }}>{`w: ${Number(p.weight).toFixed(3)} · s: ${DECAY_SCALE_KM}km`}</div> */}
                                                            </div>
                                                        </div>
                                                    );
                                                })}
                                            </div>
                                        );
                                    })()}
                                    {viewMode !== "compare" && filteredPois && selectedCategory !== 'All' && Object.entries(filteredPois)
                                        .filter(([cat]) => cat === selectedCategory)
                                        .map(([cat, list]) => {
                                            const filteredList = list
                                                .filter(p => p.name.toLowerCase().includes(searchQuery.toLowerCase()))
                                                .slice()
                                                .sort((a, b) => {
                                                    return getDecayedWeight(b) - getDecayedWeight(a);
                                                });
                                            if (filteredList.length === 0) return null;
                                            return (
                                                <div key={cat} style={{ marginBottom: 12 }}>
                                                    <div style={{ fontWeight: 700, textTransform: 'capitalize', marginBottom: 6 }}>{cat}</div>
                                                    {filteredList.map((p, idx) => (
                                                        <div key={`${p.name}-${idx}`}
                                                            onMouseEnter={() => {
                                                                setHoverPos({ lat: p.lat, lng: p.lng });
                                                                setHoverPathA(null);
                                                                setHoverPathB(null);
                                                                try { mapRef.current?.flyTo([p.lat, p.lng], 17); } catch (err) { void err; }
                                                                setHoverPath(getPathCoords(p.raw));
                                                            }}
                                                            onMouseLeave={() => {
                                                                setHoverPos(null);
                                                                setHoverPath(null);
                                                                setHoverPathA(null);
                                                                setHoverPathB(null);
                                                                try { mapRef.current?.flyTo([selectedPoint.lat, selectedPoint.lng], 16); } catch (err) { void err; }
                                                            }}
                                                            style={{
                                                                display: 'flex',
                                                                gap: 8,
                                                                padding: 8,
                                                                borderRadius: 6,
                                                                alignItems: 'center',
                                                                cursor: 'pointer',
                                                                border: '1px solid rgba(15,23,42,0.03)',
                                                                marginBottom: 8,
                                                                background: (() => {
                                                                    const pct = getCategorySharePct(p, cat);
                                                                    return `linear-gradient(90deg, rgba(99,102,241,0.18) ${pct}%, rgba(255,255,255,0) ${pct}%)`;
                                                                })()
                                                            }}>
                                                            <div style={{ flex: 1 }}>
                                                                <div style={{ fontWeight: 700 }}>{p.name}</div>
                                                                {p.subcategory && <div style={{ fontSize: 11, color: '#3b82f6', fontWeight: 600, textTransform: 'uppercase', marginTop: 2 }}>{p.subcategory}</div>}
                                                                <div style={{ color: '#64748b', fontSize: 13 }}>{`${p.lat.toFixed(6)}, ${p.lng.toFixed(6)}`}</div>
                                                            </div>
                                                            <div style={{ textAlign: 'right' }}>
                                                                <div style={{ fontWeight: 800, fontSize: 14 }}>{`${Number(p.distance_km).toFixed(3)} km`}</div>
                                                            </div>
                                                        </div>
                                                    ))}
                                                </div>
                                            );
                                        })}
                                    {/* hover path now rendered inside MapContainer */}
                                </div>
                            </div>
                        </div>
                    </div>
                )}

                {points.length > 0 && ((viewMode === "compare" && comparePage === "explain") || (viewMode === "single" && singlePage === "explain")) && (
                    <div style={{ background: "#ffffff", padding: 18, borderRadius: 12, border: "1px solid rgba(15,23,42,0.06)", marginTop: 12, boxShadow: "0 6px 18px rgba(15,23,42,0.05)", animation: "floatIn 0.5s ease" }}>
                        <div style={{ display: "flex", justifyContent: "space-between", gap: 12, flexWrap: "wrap", alignItems: "center" }}>
                            <div>
                                <div style={{ fontSize: 13, color: "#64748b", textTransform: "uppercase", letterSpacing: "0.12em", fontWeight: 800 }}>Explanation</div>
                                <div style={{ fontSize: 20, fontWeight: 900, color: "#0f172a" }}>Top contributors by category</div>
                            </div>
                            <div style={{ fontSize: 12, color: "#64748b" }}>Radius: {MAX_RADIUS_KM} km · decay: {DECAY_SCALE_KM} km</div>
                        </div>

                        {aiLoading && <div style={{ fontSize: 12, color: "#64748b", marginTop: 8 }}>Generating explanation…</div>}
                        {aiError && <div style={{ fontSize: 12, color: "#ef4444", marginTop: 8 }}>{aiError}</div>}
                        {aiExplanation ? (
                            <div style={{ whiteSpace: "pre-wrap", fontSize: 13, color: "#0f172a", marginTop: 10, background: "#f8fafc", border: "1px solid #e2e8f0", padding: 12, borderRadius: 10 }}>
                                {aiExplanation}
                            </div>
                        ) : (
                            <div style={{ fontSize: 13, color: "#64748b", marginTop: 10, background: "#f8fafc", border: "1px dashed #e2e8f0", padding: 12, borderRadius: 10 }}>
                                Generate an explanation to see a detailed narrative of the top contributing POIs.
                            </div>
                        )}

                        {pointSummaries.length > 0 && (
                            <div style={{ marginTop: 16, display: "grid", gap: 14 }}>
                                {selectedTargets.map((t) => {
                                    const summary = pointSummaries.find((s) => s.key === t.key);
                                    if (!summary) return null;
                                    return (
                                        <div key={`explain-summary-${summary.key}`} style={{ border: "1px solid #e2e8f0", borderRadius: 12, padding: 14, background: "linear-gradient(135deg, rgba(248,250,252,1) 0%, rgba(255,255,255,1) 100%)" }}>
                                            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", gap: 10, flexWrap: "wrap" }}>
                                                <div style={{ fontWeight: 900, fontSize: 14 }}>
                                                    {viewMode === "compare"
                                                        ? `${t.label}: ${pointMeta[t.idx]?.label || `P${t.idx + 1}`}`
                                                        : (selectedPointMeta?.label || (points.length > 1 ? `Point ${selectedPointIdx + 1}` : "Point"))}
                                                </div>
                                                <div style={{ fontSize: 12, color: "#64748b" }}>{summary.key}</div>
                                            </div>
                                            <div style={{ marginTop: 6, fontSize: 12, color: "#475569" }}>
                                                Total decayed contribution: <strong>{summary.totalScore.toFixed(3)}</strong>
                                            </div>
                                            <div style={{ marginTop: 12, display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(420px, 1fr))", gap: 12 }}>
                                                {summary.perCategory.map((catSummary) => {
                                                    const chartData = catSummary.topPois.map((poi) => ({
                                                        name: poi.name.length > 18 ? `${poi.name.slice(0, 17)}…` : poi.name,
                                                        fullName: poi.name,
                                                        value: Number(poi.decayed_weight) || 0
                                                    }));
                                                    return (
                                                        <div key={`${summary.key}-${catSummary.cat}`} style={{ border: "1px solid #e2e8f0", borderRadius: 10, padding: 10, background: "#ffffff" }}>
                                                            <div style={{ fontWeight: 800, fontSize: 12 }}>{catSummary.cat}</div>
                                                            <div style={{ fontSize: 11, color: "#64748b", marginTop: 2 }}>Top contributors</div>
                                                            {catSummary.topPois.length === 0 ? (
                                                                <div style={{ fontSize: 12, color: "#94a3b8", marginTop: 8 }}>No POIs within {MAX_RADIUS_KM} km.</div>
                                                            ) : (
                                                                <div style={{ width: "100%", maxHeight: 220, marginTop: 6, overflowY: "auto", paddingRight: 4 }}>
                                                                    <div style={{ height: Math.max(140, chartData.length * 28) }}>
                                                                        <ResponsiveContainer>
                                                                            <BarChart data={chartData} layout="vertical" margin={{ top: 6, right: 6, left: 6, bottom: 6 }}>
                                                                                <XAxis type="number" tick={{ fontSize: 10 }} axisLine={false} tickLine={false} />
                                                                                <YAxis type="category" dataKey="name" width={100} tick={{ fontSize: 10 }} axisLine={false} tickLine={false} />
                                                                                <Tooltip
                                                                                    formatter={(v) => Number(v as number).toFixed(3)}
                                                                                    labelFormatter={(_, payload) => {
                                                                                        const fullName = payload?.[0]?.payload?.fullName as string | undefined;
                                                                                        return fullName || "POI";
                                                                                    }}
                                                                                />
                                                                                <Bar dataKey="value" fill={chartColors[catSummary.cat as keyof typeof chartColors] || "#0ea5e9"} radius={[6, 6, 6, 6]} isAnimationActive animationDuration={800} />
                                                                            </BarChart>
                                                                        </ResponsiveContainer>
                                                                    </div>
                                                                </div>
                                                            )}
                                                            <div style={{ marginTop: 6, fontSize: 11, color: "#475569" }}>Decayed sum: {catSummary.score.toFixed(3)}</div>
                                                        </div>
                                                    );
                                                })}
                                            </div>
                                        </div>
                                    );
                                })}
                            </div>
                        )}

                        <div style={{ display: "flex", justifyContent: "flex-end", alignItems: "center", gap: 10, marginTop: 16, paddingTop: 12, borderTop: "1px solid #e2e8f0" }}>
                            {!canGenerateAi && <div style={{ fontSize: 12, color: "#94a3b8" }}>Load scores and POIs to enable explanation.</div>}
                            <button
                                onClick={handleGenerateAi}
                                disabled={!canGenerateAi || aiLoading}
                                style={{
                                    padding: "8px 12px",
                                    borderRadius: 8,
                                    border: "1px solid #e2e8f0",
                                    background: canGenerateAi && !aiLoading ? "#0f172a" : "#f1f5f9",
                                    color: canGenerateAi && !aiLoading ? "#ffffff" : "#94a3b8",
                                    fontSize: 12,
                                    fontWeight: 700,
                                    cursor: canGenerateAi && !aiLoading ? "pointer" : "not-allowed"
                                }}
                            >
                                {aiLoading ? "Generating…" : "Generate Explanation"}
                            </button>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}
