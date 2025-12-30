"use client";

import React, { useMemo, useEffect, useState, useRef } from "react";
import { MapContainer, TileLayer, Marker } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import * as L from "leaflet";

function qs(key: string) {
    return new URLSearchParams(window.location.search).get(key) || "";
}

function seededRandom(seed: string) {
    let h = 2166136261 >>> 0;
    for (let i = 0; i < seed.length; i++) {
        h += seed.charCodeAt(i);
        h += h << 1;
        h ^= h >>> 7;
    }
    return function () {
        h += 0x6d2b79f5;
        let t = Math.imul(h ^ (h >>> 15), 1 | h);
        t ^= t + Math.imul(t ^ (t >>> 7), 61 | t);
        return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
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

type Poi = { name: string; lat: number; lng: number; weight: number; distance_km: number; subcategory?: string; raw?: Record<string, string> };
type Category = { score: number; pois: Poi[] };

export default function ResultPage() {
    const name = decodeURIComponent(qs("name") || "");
    const lat = parseFloat(qs("lat") || "0");
    const lng = parseFloat(qs("lng") || "0");

    const [loadedPois, setLoadedPois] = useState<Record<string, Poi[]> | null>(null);
    const [selectedCategory, setSelectedCategory] = useState<string>("All");
    const [prediction, setPrediction] = useState<{ score: number; risk: string } | null>(null);

    useEffect(() => {
        if (!lat || !lng) return;
        fetch("http://127.0.0.1:8000/api/v1/predict-score/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ lat, lng })
        })
        .then(res => res.json())
        .then(data => {
            setPrediction({ score: data.predicted_score, risk: data.risk_level });
        })
        .catch(err => console.error("Prediction fetch error:", err));
    }, [lat, lng]);

    const analysis = useMemo(() => {
        const s = `${name}|${lat}|${lng}`;
        const rnd = seededRandom(s);

        const categories = ["competitor", "education", "banks", "health", "temples", "other"] as const;
        const catMap: Record<string, Category> = {};
        const scores: number[] = [];

        categories.forEach((cat) => {
            const score = Number((rnd()).toFixed(3));
            scores.push(score);
            const count = Math.floor(rnd() * 1000);
            const pois: Poi[] = [];
            for (let i = 0; i < count; i++) {
                const dlat = (rnd() - 0.5) * 0.02; // ~±1km
                const dlng = (rnd() - 0.5) * 0.02;
                const plat = lat + dlat;
                const plng = lng + dlng;
                const distance_km = Number(haversineKm(lat, lng, plat, plng).toFixed(3));
                pois.push({ name: `${cat} ${i + 1}`, lat: Number(plat.toFixed(6)), lng: Number(plng.toFixed(6)), weight: Number(rnd().toFixed(3)), distance_km });
            }
            catMap[cat] = { score, pois };
        });

        // success_score: simple aggregate of scores
        const success_score = Number((scores.reduce((s, v) => s + v, 0) / scores.length).toFixed(3));

        return { success_score, categories: catMap } as { success_score: number; categories: Record<string, Category> };
    }, [name, lat, lng]);

    // --- CSV loading + mapping images ---
    useEffect(() => {
        let mounted = true;
        const MAX_RADIUS_KM = 1; // filter radius
        const csvFiles = [
            "education_final.csv",
            "health_final.csv",
            "other_final.csv",
            "temples_final.csv",
            "banks_final.csv",
            "cafe_final.csv",
        ];

        // const imageCsvs = ["/data/d/compact_summary_images.csv", "/data/d/education.csv", "/data/d/health.csv", "/data/d/other.csv", "/data/d/temples.csv", "/data/d/banks.csv"];

        const parseCsv = (text: string): Record<string, string>[] => {
            const lines = text.split(/\r?\n/).filter(l => l.trim().length > 0);
            if (lines.length === 0) return [];
            const header = lines[0];
            const cols = header.split(/,(?=(?:[^"]*"[^"]*")*[^"]*$)/).map(c => c.replace(/^"|"$/g, "").trim());
            const rows: Record<string, string>[] = [];
            for (let i = 1; i < lines.length; i++) {
                const parts = lines[i].split(/,(?=(?:[^"]*"[^"]*")*[^"]*$)/).map(p => p.replace(/^"|"$/g, "").trim());
                if (parts.length === 0) continue;
                const row: Record<string, string> = {};
                for (let j = 0; j < cols.length; j++) row[cols[j]] = parts[j] ?? "";
                rows.push(row);
            }
            return rows;
        };

        (async () => {
            try {
                // load image metadata first
                // const imageMap = new Map<string, string>(); // key: lat|lng or name -> image url
                // for (const p of imageCsvs) {
                //     try {
                //         const resp = await fetch(p);
                //         if (!resp.ok) continue;
                //         const txt = await resp.text();
                //         const rows = parseCsv(txt);
                //         rows.forEach((row) => {
                //             const lat = (row['lat'] ?? row['Lat'] ?? row['lat '])?.toString();
                //             const lng = (row['lng'] ?? row['Lng'] ?? row['lon'] ?? row['Lon'])?.toString();
                //             const name = (row['name'] ?? row['Name'] ?? row['place'] ?? row['place_name'])?.toString();
                //             const image = (row['image'] ?? row['img'] ?? row['image_url'] ?? row['photo'])?.toString();
                //             if (image && lat && lng) imageMap.set(`${Number(lat).toFixed(6)}|${Number(lng).toFixed(6)}`, image);
                //             if (image && name) imageMap.set(name.trim().toLowerCase(), image);
                //         });
                //     } catch { void 0; }
                // }

                // persist image map for rendering
                // if (mounted) setImageMapState(Object.fromEntries(imageMap.entries()));

                const categoriesMap: Record<string, Poi[]> = {};
                for (const fname of csvFiles) {
                    try {
                        const url = `/data/${fname}`;
                        const res = await fetch(url);
                        if (!res.ok) continue;
                        const txt = await res.text();
                        const rows = parseCsv(txt);
                        for (const row of rows) {
                            const latStr = (row['lat'] ?? row['Lat'] ?? row['lat '])?.toString();
                            const lngStr = (row['lng'] ?? row['Lng'] ?? row['lon'] ?? row['Lng '])?.toString();
                            if (!latStr || !lngStr) continue;
                            const plat = Number(latStr);
                            const plng = Number(lngStr);
                            if (!Number.isFinite(plat) || !Number.isFinite(plng)) continue;
                            const distance_km = Number(haversineKm(lat, lng, plat, plng).toFixed(3));
                            if (distance_km > MAX_RADIUS_KM) continue;
                            // choose weight field
                            let weight = NaN;
                            if ((row['cafe_individual_score'] ?? row['cafe_individual_score '])) weight = Number(row['cafe_individual_score'] ?? row['cafe_individual_score ']);
                            if (Number.isNaN(weight) || weight === 0) weight = Number(row['final_weight'] ?? row['final_weight '] ?? row['final_weight'] ?? NaN);
                            if (!Number.isFinite(weight)) weight = 0;
                            const nameVal = (row['name'] ?? row['Name'] ?? row['place'] ?? '')?.toString();

                            // Determine Main Category strictly by filename
                            let mainCat = 'Other';
                            if (fname === 'education_final.csv') mainCat = 'Education';
                            else if (fname === 'health_final.csv') mainCat = 'Health';
                            else if (fname === 'temples_final.csv') mainCat = 'Temples';
                            else if (fname === 'banks_final.csv') mainCat = 'Bank';
                            else if (fname === 'cafe_final.csv') mainCat = 'Cafes';
                            else if (fname === 'other_final.csv') mainCat = 'Other';

                            // Determine Subcategory from the category column
                            const subCat = (row['category'] ?? row['Category'])?.toString() || '';

                            const poi: Poi = { name: nameVal || fname.replace(/\.csv$/, ''), lat: plat, lng: plng, weight, distance_km, subcategory: subCat, raw: row };
                            categoriesMap[mainCat] = categoriesMap[mainCat] || [];
                            categoriesMap[mainCat].push(poi);
                        }
                    } catch { void 0; }
                }
                // sort each category: prefer cafe_individual_score when available, then final_weight, then distance
                for (const list of Object.values(categoriesMap)) {
                    list.sort((a, b) => {
                        const aw = Number(a.weight);
                        const bw = Number(b.weight);
                        if (Number.isFinite(aw) && Number.isFinite(bw)) {
                            return bw - aw;
                        }
                        return 0;
                    });
                }

                if (mounted) setLoadedPois(categoriesMap);
            } catch (e) { void e; if (mounted) setLoadedPois({}); }
        })();

        return () => { mounted = false; };
    }, [lat, lng]);

    const mapRef = useRef<L.Map | null>(null);
    const [hoverPos, setHoverPos] = useState<{ lat: number; lng: number } | null>(null);
    const [searchQuery, setSearchQuery] = useState("");

    const categoryCounts = useMemo(() => {
        if (!loadedPois) return {};
        const counts: Record<string, number> = {};
        let total = 0;
        Object.entries(loadedPois).forEach(([cat, list]) => {
            const filteredList = list.filter(p => p.name.toLowerCase().includes(searchQuery.toLowerCase()));
            counts[cat] = filteredList.length;
            total += filteredList.length;
        });
        counts['All'] = total;
        return counts;
    }, [loadedPois, searchQuery]);

    const analysisEntries = Object.entries(analysis.categories) as [string, Category][];

    return (
        <div style={{ padding: 20, fontFamily: "Inter, system-ui, Arial", background: "#ffffff", minHeight: "100vh", color: "#0f172a" }}>
            <div style={{ maxWidth: 1100, margin: "0 auto" }}>
                <div style={{ background: "#ffffff", padding: 18, borderRadius: 10, border: "1px solid rgba(15,23,42,0.06)" }}>
                    <h1 style={{ margin: 0, color: '#0f172a' }}>{name || "Place"} — Analysis</h1>
                    <div style={{ color: "#475569", marginTop: 6 }}>{`lat: ${lat.toFixed(6)} · lng: ${lng.toFixed(6)}`}</div>
                    <div style={{ marginTop: 12 }}>
                        <div style={{ fontSize: 13, color: "#475569" }}>Success Score {prediction ? `(${prediction.risk})` : ''}</div>
                        <div style={{ height: 14, background: "#f1f5f9", borderRadius: 8, marginTop: 6 }}>
                            <div style={{ height: 14, width: `${Math.min(((prediction?.score || 0) / 3) * 100, 100)}%`, background: "linear-gradient(90deg,#16a34a,#06b6d4)", borderRadius: 8, transition: "width 0.5s" }} />
                        </div>
                        <div style={{ marginTop: 6, color: '#0f172a' }}>{prediction ? prediction.score.toFixed(3) : "Calculating..."}</div>
                    </div>
                </div>

                <div style={{ display: "grid", gap: 12, marginTop: 12 }}>
                    <div style={{ background: "#ffffff", padding: 8, borderRadius: 8, border: "1px solid rgba(15,23,42,0.04)" }}>
                        <h3 style={{ marginTop: 0 }}>Map and POIs</h3>
                        <div style={{ display: 'flex', gap: 12 }}>
                            <div style={{ flex: 1 }}>
                                <div style={{ width: '100%', aspectRatio: '1 / 1' }}>
                                    <MapContainer
                                        ref={(m: unknown) => { mapRef.current = m as L.Map | null; }}
                                        center={[lat || 27.670587, lng || 85.420868]}
                                        zoom={16}
                                        style={{ width: '100%', height: '100%', borderRadius: 8 }}
                                    >
                                        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
                                        {/* center marker */}
                                        <Marker position={[lat, lng]} />
                                        {/* hover marker */}
                                        {hoverPos && <Marker position={[hoverPos.lat, hoverPos.lng]} />}
                                    </MapContainer>
                                </div>
                            </div>

                            <div style={{ width: 360, maxHeight: '72vh', overflowY: 'auto', borderLeft: '1px solid rgba(15,23,42,0.04)', paddingLeft: 8, position: 'relative' }}>
                                <div style={{ position: 'sticky', top: 0, background: '#ffffff', zIndex: 10, paddingBottom: 8, paddingTop: 0 }}>
                                    <div style={{ fontWeight: 700, marginBottom: 4 }}>Nearby POIs (within 1 km)</div>
                                    <div style={{ fontSize: 13, color: '#64748b', marginBottom: 8 }}>{name}</div>

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

                                {!loadedPois && <div>Loading...</div>}
                                {loadedPois && Object.keys(loadedPois).length === 0 && <div>No POIs found within radius.</div>}
                                {loadedPois && Object.entries(loadedPois)
                                    .filter(([cat]) => selectedCategory === 'All' || cat === selectedCategory)
                                    .map(([cat, list]) => {
                                        const filteredList = list.filter(p => p.name.toLowerCase().includes(searchQuery.toLowerCase()));
                                        if (filteredList.length === 0) return null;
                                        return (
                                            <div key={cat} style={{ marginBottom: 12 }}>
                                                <div style={{ fontWeight: 700, textTransform: 'capitalize', marginBottom: 6 }}>{cat}</div>
                                                {filteredList.map((p, idx) => (
                                                    <div key={`${p.name}-${idx}`}
                                                        onMouseEnter={() => { setHoverPos({ lat: p.lat, lng: p.lng }); try { mapRef.current?.flyTo([p.lat, p.lng], 17); } catch (err) { void err; } }}
                                                        onMouseLeave={() => { setHoverPos(null); try { mapRef.current?.flyTo([lat, lng], 16); } catch (err) { void err; } }}
                                                        style={{ display: 'flex', gap: 8, padding: 8, borderRadius: 6, alignItems: 'center', cursor: 'pointer', border: '1px solid rgba(15,23,42,0.03)', marginBottom: 8 }}>
                                                        <div style={{ flex: 1 }}>
                                                            <div style={{ fontWeight: 700 }}>{p.name}</div>
                                                            {p.subcategory && <div style={{ fontSize: 11, color: '#3b82f6', fontWeight: 600, textTransform: 'uppercase', marginTop: 2 }}>{p.subcategory}</div>}
                                                            <div style={{ color: '#64748b', fontSize: 13 }}>{`${p.lat.toFixed(6)}, ${p.lng.toFixed(6)}`}</div>
                                                        </div>
                                                        <div style={{ textAlign: 'right' }}>
                                                            <div style={{ fontWeight: 800, fontSize: 15 }}>{`w: ${Number(p.weight).toFixed(3)}`}</div>
                                                            <div style={{ color: '#64748b', fontSize: 12 }}>{p.distance_km} km</div>
                                                        </div>
                                                    </div>
                                                ))}
                                            </div>
                                        );
                                    })}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
