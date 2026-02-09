"use client";

import React, { useMemo, useEffect, useState, useRef } from "react";
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

type Poi = { name: string; lat: number; lng: number; weight: number; distance_km: number; subcategory?: string; raw?: Record<string, string> };
export default function ResultPage() {
    const name = decodeURIComponent(qs("name") || "");
    const lat = parseFloat(qs("lat") || "0");
    const lng = parseFloat(qs("lng") || "0");
    const mode = qs("mode") || "point";
    const pick = qs("pick") || (qs("points") ? "multiple" : "single");
    const pointsParam = qs("points");
    const points = useMemo(() => parsePoints(pointsParam, lat, lng), [pointsParam, lat, lng]);
    const center = useMemo(() => {
        if (!points.length) return { lat, lng };
        const total = points.reduce((acc, p) => ({ lat: acc.lat + p.lat, lng: acc.lng + p.lng }), { lat: 0, lng: 0 });
        return { lat: total.lat / points.length, lng: total.lng / points.length };
    }, [points, lat, lng]);
    const centerLat = center.lat;
    const centerLng = center.lng;

    const [loadedPois, setLoadedPois] = useState<Record<string, Poi[]> | null>(null);
    const [selectedPointIdx, setSelectedPointIdx] = useState<number>(0);
    const [selectedCategory, setSelectedCategory] = useState<string>("All");
    const [predictions, setPredictions] = useState<Record<string, { score: number; risk: string }>>({});
    const primaryPoint = points[0] || { lat, lng };
    const primaryKey = `${primaryPoint.lat.toFixed(6)},${primaryPoint.lng.toFixed(6)}`;
    const primaryPrediction = predictions[primaryKey] || null;
    const averageScore = useMemo(() => {
        const vals = Object.values(predictions).map((p) => p.score).filter((v) => Number.isFinite(v));
        if (vals.length === 0) return null;
        return vals.reduce((s, v) => s + v, 0) / vals.length;
    }, [predictions]);
    const selectedPoint = useMemo(() => {
        return points[selectedPointIdx] || points[0] || { lat: centerLat, lng: centerLng };
    }, [points, selectedPointIdx, centerLat, centerLng]);
    const MAX_RADIUS_KM = 1;
    // --- Load POIs from backend POI endpoint instead of CSVs ---
    useEffect(() => {
        let mounted = true;
        const controller = new AbortController();
        (async () => {
            try {
                const radius = 0.3; // km
                const base = `http://127.0.0.1:8000/api/v1/pois/?lat=${encodeURIComponent(centerLat)}&lon=${encodeURIComponent(centerLng)}&radius_km=${radius}`;
                const streamUrl = base + `&stream=true`;
                const res = await fetch(streamUrl, { signal: controller.signal });
                const mapName: Record<string, string> = { cafes: 'Cafes', banks: 'Bank', education: 'Education', health: 'Health', temples: 'Temples', other: 'Other' };
                const categoriesMap: Record<string, Poi[]> = {};
                if (!res.ok) {
                    if (mounted) setLoadedPois({});
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
                                const arr = Array.isArray(obj.items) ? obj.items : [];
                                const display = mapName[catKey] || catKey;
                                const list = arr.map((it: any) => {
                                    const plat = Number(it.lat);
                                    const plng = Number(it.lon ?? it.lng ?? 0);
                                    const nameVal = it.name ?? '';
                                    const weight = Number(it.weight ?? 0) || 0;
                                    const distance_km = Number(it.distance_km ?? 0) || 0;
                                    const poi: Poi = { name: nameVal, lat: plat, lng: plng, weight, distance_km, raw: it };
                                    return poi;
                                }).filter(p => Number.isFinite(p.lat) && Number.isFinite(p.lng));
                                if (list.length) {
                                    categoriesMap[display] = (categoriesMap[display] || []).concat(list);
                                    if (mounted) setLoadedPois({ ...categoriesMap });
                                }
                            } catch (err) {
                                // ignore parse errors for partial lines
                            }
                        }
                    }
                    // final buffer
                    if (buf.trim()) {
                        try {
                            const obj = JSON.parse(buf.trim());
                            const catKey = obj.category as string;
                            const arr = Array.isArray(obj.items) ? obj.items : [];
                            const display = mapName[catKey] || catKey;
                            const list = arr.map((it: any) => {
                                const plat = Number(it.lat);
                                const plng = Number(it.lon ?? it.lng ?? 0);
                                const nameVal = it.name ?? '';
                                const weight = Number(it.weight ?? 0) || 0;
                                const distance_km = Number(it.distance_km ?? 0) || 0;
                                const poi: Poi = { name: nameVal, lat: plat, lng: plng, weight, distance_km, raw: it };
                                return poi;
                            }).filter(p => Number.isFinite(p.lat) && Number.isFinite(p.lng));
                            if (list.length) {
                                categoriesMap[display] = (categoriesMap[display] || []).concat(list);
                                if (mounted) setLoadedPois({ ...categoriesMap });
                            }
                        } catch (err) { /* ignore */ }
                    }
                } else {
                    // fallback to non-streaming JSON
                    const data = await res.json();
                    const pois = data?.pois || {};
                    for (const [key, arr] of Object.entries(pois)) {
                        const display = mapName[key] || key;
                        const list = (arr as any[]).map((it) => {
                            const plat = Number(it.lat);
                            const plng = Number(it.lon ?? it.lng ?? 0);
                            const nameVal = it.name ?? '';
                            const weight = Number(it.weight ?? 0) || 0;
                            const distance_km = Number(it.distance_km ?? 0) || 0;
                            const poi: Poi = { name: nameVal, lat: plat, lng: plng, weight, distance_km, raw: it };
                            return poi;
                        }).filter(p => Number.isFinite(p.lat) && Number.isFinite(p.lng));
                        if (list.length) categoriesMap[display] = list;
                    }
                    if (mounted) setLoadedPois(categoriesMap);
                }
            } catch (err) {
                if (mounted) setLoadedPois({});
            }
        })();
        return () => { mounted = false; controller.abort(); };
    }, [centerLat, centerLng]);

        // CSV fallback removed — POIs are loaded from backend `/api/v1/pois/` above.

    const mapRef = useRef<L.Map | null>(null);
    const [hoverPos, setHoverPos] = useState<{ lat: number; lng: number } | null>(null);
    const [hoverPath, setHoverPath] = useState<Array<[number, number]> | null>(null);
    const [searchQuery, setSearchQuery] = useState("");

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

    return (
        <div style={{ padding: 20, fontFamily: "Inter, system-ui, Arial", background: "#ffffff", minHeight: "100vh", color: "#0f172a" }}>
            <div style={{ maxWidth: 1100, margin: "0 auto" }}>
                <div style={{ background: "#ffffff", padding: 18, borderRadius: 10, border: "1px solid rgba(15,23,42,0.06)" }}>
                    <h1 style={{ margin: 0, color: '#0f172a' }}>{name || "Place"} — Analysis</h1>
                    {points.length > 1 ? (
                        <div style={{ color: "#475569", marginTop: 6 }}>{`points: ${points.length} · center: ${centerLat.toFixed(6)} · ${centerLng.toFixed(6)}`}</div>
                    ) : (
                        <div style={{ color: "#475569", marginTop: 6 }}>{`lat: ${centerLat.toFixed(6)} · lng: ${centerLng.toFixed(6)}`}</div>
                    )}
                    <div style={{ color: "#94a3b8", fontSize: 12, marginTop: 4 }}>{`mode: ${mode} · pick: ${pick}`}</div>
                    <div style={{ marginTop: 12 }}>
                        <div style={{ fontSize: 13, color: "#475569" }}>Success Score {points.length > 1 ? "(Multiple)" : (primaryPrediction ? `(${primaryPrediction.risk})` : "")}</div>
                        <div style={{ height: 14, background: "#f1f5f9", borderRadius: 8, marginTop: 6 }}>
                            <div style={{ height: 14, width: `${Math.min((((averageScore ?? primaryPrediction?.score ?? 0) || 0) / 3) * 100, 100)}%`, background: "linear-gradient(90deg,#16a34a,#06b6d4)", borderRadius: 8, transition: "width 0.5s" }} />
                        </div>
                        <div style={{ marginTop: 6, color: '#0f172a' }}>
                            {averageScore != null ? averageScore.toFixed(3) : (primaryPrediction ? primaryPrediction.score.toFixed(3) : "Calculating...")}
                        </div>
                    </div>
                    {points.length > 1 && (
                        <div style={{ marginTop: 10, fontSize: 12, color: "#475569" }}>
                            {points.map((p, idx) => {
                                const key = `${p.lat.toFixed(6)},${p.lng.toFixed(6)}`;
                                const pred = predictions[key];
                                return (
                                    <div key={key} style={{ display: 'flex', justifyContent: 'space-between', gap: 8 }}>
                                        <span>{`${idx + 1}. ${p.lat.toFixed(6)}, ${p.lng.toFixed(6)}`}</span>
                                        <span style={{ color: '#0f172a', fontWeight: 600 }}>{pred ? pred.score.toFixed(3) : "…"}</span>
                                    </div>
                                );
                            })}
                        </div>
                    )}
                </div>

                {points.length > 0 && (
                    <div style={{ background: "#ffffff", padding: 18, borderRadius: 10, border: "1px solid rgba(15,23,42,0.06)", marginTop: 12 }}>
                        <h3 style={{ marginTop: 0 }}>Per-point Analysis</h3>
                        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: 10 }}>
                            {points.map((p, idx) => {
                                const key = `${p.lat.toFixed(6)},${p.lng.toFixed(6)}`;
                                const pred = predictions[key];
                                const score = pred?.score;
                                const width = Math.min((((score ?? 0) / 3) * 100), 100);
                                return (
                                    <div key={`card-${key}`} style={{ border: '1px solid #e2e8f0', borderRadius: 8, padding: 12 }}>
                                        <div style={{ fontWeight: 700 }}>{`Point ${idx + 1}`}</div>
                                        <div style={{ color: '#64748b', fontSize: 12, marginTop: 4 }}>{`${p.lat.toFixed(6)}, ${p.lng.toFixed(6)}`}</div>
                                        <div style={{ fontSize: 12, color: '#64748b', marginTop: 6 }}>{pred ? `Risk: ${pred.risk}` : 'Risk: …'}</div>
                                        <div style={{ height: 10, background: "#f1f5f9", borderRadius: 6, marginTop: 6 }}>
                                            <div style={{ height: 10, width: `${width}%`, background: "linear-gradient(90deg,#16a34a,#06b6d4)", borderRadius: 6, transition: "width 0.5s" }} />
                                        </div>
                                        <div style={{ marginTop: 6, fontWeight: 700 }}>{pred ? pred.score.toFixed(3) : "Calculating..."}</div>
                                    </div>
                                );
                            })}
                        </div>
                    </div>
                )}

                <div style={{ display: "grid", gap: 12, marginTop: 12 }}>
                    <div style={{ background: "#ffffff", padding: 8, borderRadius: 8, border: "1px solid rgba(15,23,42,0.04)" }}>
                        <h3 style={{ marginTop: 0 }}>Map and POIs</h3>
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
                                        {points.map((p, idx) => (
                                            <Marker key={`point-${idx}`} position={[p.lat, p.lng]} />
                                        ))}
                                        {/* hover marker */}
                                        {hoverPos && <Marker position={[hoverPos.lat, hoverPos.lng]} />}
                                        {/* hover path (rendered inside MapContainer so Leaflet context is available) */}
                                        {hoverPath && hoverPath.length > 0 && (
                                            <Polyline positions={hoverPath.map(([la, lo]) => [la, lo])} pathOptions={{ color: '#ff6b6b', weight: 5 }} />
                                        )}
                                    </MapContainer>
                                </div>
                            </div>

                            <div style={{ width: 360, maxHeight: '72vh', overflowY: 'auto', borderLeft: '1px solid rgba(15,23,42,0.04)', paddingLeft: 8, position: 'relative' }}>
                                <div style={{ position: 'sticky', top: 0, background: '#ffffff', zIndex: 10, paddingBottom: 8, paddingTop: 0 }}>
                                    <div style={{ fontWeight: 700, marginBottom: 4 }}>Nearby POIs (within 1 km)</div>
                                    <div style={{ fontSize: 13, color: '#64748b', marginBottom: 8 }}>{name}</div>

                                    {points.length > 1 && (
                                        <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap', marginBottom: 8 }}>
                                            {points.map((p, idx) => (
                                                <button
                                                    key={`pt-${idx}`}
                                                    onClick={() => setSelectedPointIdx(idx)}
                                                    style={{
                                                        padding: '4px 8px',
                                                        borderRadius: 14,
                                                        border: '1px solid #e2e8f0',
                                                        background: selectedPointIdx === idx ? '#0f172a' : '#ffffff',
                                                        color: selectedPointIdx === idx ? '#ffffff' : '#64748b',
                                                        fontSize: 11,
                                                        cursor: 'pointer',
                                                        fontWeight: 600
                                                    }}
                                                >
                                                    {`P${idx + 1}`}
                                                </button>
                                            ))}
                                        </div>
                                    )}

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
                                                {cat} <span style={{ opacity: 0.7, fontSize: 11, marginLeft: 2 }}>{categoryCounts[cat] || 0}</span>
                                            </button>
                                        ))}
                                    </div>
                                </div>

                                {!filteredPois && <div>Loading...</div>}
                                {filteredPois && Object.keys(filteredPois).length === 0 && <div>No POIs found within radius.</div>}
                                {filteredPois && Object.entries(filteredPois)
                                    .filter(([cat]) => selectedCategory === 'All' || cat === selectedCategory)
                                    .map(([cat, list]) => {
                                        const DECAY_SCALE_KM = 1.0;
                                        const filteredList = list
                                            .filter(p => p.name.toLowerCase().includes(searchQuery.toLowerCase()))
                                            .slice()
                                            .sort((a, b) => {
                                                const aw = Number(a.weight) || 0;
                                                const bw = Number(b.weight) || 0;
                                                const ad = Number(a.distance_km) || 0;
                                                const bd = Number(b.distance_km) || 0;
                                                const aScore = aw * Math.exp(-ad / DECAY_SCALE_KM);
                                                const bScore = bw * Math.exp(-bd / DECAY_SCALE_KM);
                                                return bScore - aScore;
                                            });
                                        if (filteredList.length === 0) return null;
                                        return (
                                            <div key={cat} style={{ marginBottom: 12 }}>
                                                <div style={{ fontWeight: 700, textTransform: 'capitalize', marginBottom: 6 }}>{cat}</div>
                                                {filteredList.map((p, idx) => (
                                                    <div key={`${p.name}-${idx}`}
                                                        onMouseEnter={() => {
                                                            setHoverPos({ lat: p.lat, lng: p.lng });
                                                            try { mapRef.current?.flyTo([p.lat, p.lng], 17); } catch (err) { void err; }
                                                            try {
                                                                const raw = p.raw as any;
                                                                if (raw && Array.isArray(raw.path)) {
                                                                    const coords: Array<[number, number]> = raw.path.map((pt: any) => [Number(pt.lat), Number(pt.lon ?? pt.lng)]).filter(([a,b]) => Number.isFinite(a) && Number.isFinite(b));
                                                                    setHoverPath(coords.length ? coords : null);
                                                                } else {
                                                                    setHoverPath(null);
                                                                }
                                                            } catch (err) { setHoverPath(null); }
                                                        }}
                                                            onMouseLeave={() => { setHoverPos(null); setHoverPath(null); try { mapRef.current?.flyTo([selectedPoint.lat, selectedPoint.lng], 16); } catch (err) { void err; } }}
                                                        style={{ display: 'flex', gap: 8, padding: 8, borderRadius: 6, alignItems: 'center', cursor: 'pointer', border: '1px solid rgba(15,23,42,0.03)', marginBottom: 8 }}>
                                                        <div style={{ flex: 1 }}>
                                                            <div style={{ fontWeight: 700 }}>{p.name}</div>
                                                            {p.subcategory && <div style={{ fontSize: 11, color: '#3b82f6', fontWeight: 600, textTransform: 'uppercase', marginTop: 2 }}>{p.subcategory}</div>}
                                                            <div style={{ color: '#64748b', fontSize: 13 }}>{`${p.lat.toFixed(6)}, ${p.lng.toFixed(6)}`}</div>
                                                        </div>
                                                        <div style={{ textAlign: 'right' }}>
                                                            {(() => {
                                                                const w = Number(p.weight) || 0;
                                                                const d = Number(p.distance_km) || 0;
                                                                const wEff = w * Math.exp(-d / DECAY_SCALE_KM);
                                                                return (
                                                                    <>
                                                                        <div style={{ fontWeight: 800, fontSize: 14 }}>{`w*e^{-d/s}: ${wEff.toFixed(3)}`}</div>
                                                                        <div style={{ fontWeight: 800, fontSize: 14 }}>{`${d.toFixed(3)} km`}</div>
                                                                        <div style={{ fontSize: 12, color: '#475569' }}>{`w: ${w.toFixed(3)} · s: ${DECAY_SCALE_KM}km`}</div>
                                                                    </>
                                                                );
                                                            })()}
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
            </div>
        </div>
    );
}
