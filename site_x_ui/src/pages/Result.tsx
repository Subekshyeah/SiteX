"use client";

import React, { useMemo } from "react";
import { RadarChart, PolarAngleAxis, PolarGrid, Radar, BarChart, Bar, XAxis, YAxis, Tooltip, PieChart, Pie, Cell, ResponsiveContainer } from "recharts";

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

type Poi = { name: string; lat: number; lng: number; weight: number; distance_km: number };
type Category = { score: number; pois: Poi[] };

export default function ResultPage(): JSX.Element {
    const name = decodeURIComponent(qs("name") || "");
    const lat = parseFloat(qs("lat") || "0");
    const lng = parseFloat(qs("lng") || "0");

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

        return { success_score, categories: catMap } as any;
    }, [name, lat, lng]);

    const radarData = Object.entries(analysis.categories).map(([k, v]: any) => ({ POI: k.charAt(0).toUpperCase() + k.slice(1), score: Math.max(0.001, v.score) }));
    const barData = Object.entries(analysis.categories).map(([k, v]: any) => ({ name: k.charAt(0).toUpperCase() + k.slice(1), count: (v.pois || []).length }));
    const donutData = [
        { name: "Competitor", value: (analysis.categories.competitor.pois || []).length },
        { name: "Others", value: Object.entries(analysis.categories).filter(([k]) => k !== "competitor").reduce((s, [, v]: any) => s + ((v.pois || []).length), 0) },
    ];

    return (
        <div style={{ padding: 20, fontFamily: "Inter, system-ui, Arial", background: "#ffffff", minHeight: "100vh", color: "#0f172a" }}>
            <div style={{ maxWidth: 1100, margin: "0 auto" }}>
                <div style={{ background: "#ffffff", padding: 18, borderRadius: 10, border: "1px solid rgba(15,23,42,0.06)" }}>
                    <h1 style={{ margin: 0, color: '#0f172a' }}>{name || "Place"} — Analysis</h1>
                    <div style={{ color: "#475569", marginTop: 6 }}>{`lat: ${lat.toFixed(6)} · lng: ${lng.toFixed(6)}`}</div>
                    <div style={{ marginTop: 12 }}>
                        <div style={{ fontSize: 13, color: "#475569" }}>Success Score</div>
                        <div style={{ height: 14, background: "#f1f5f9", borderRadius: 8, marginTop: 6 }}>
                            <div style={{ height: 14, width: `${analysis.success_score * 100}%`, background: "linear-gradient(90deg,#16a34a,#06b6d4)", borderRadius: 8 }} />
                        </div>
                        <div style={{ marginTop: 6, color: '#0f172a' }}>{analysis.success_score}</div>
                    </div>
                </div>

                <div style={{ display: "grid", gridTemplateColumns: "1fr 360px", gap: 12, marginTop: 12 }}>
                    <div style={{ background: "#ffffff", padding: 12, borderRadius: 8, border: "1px solid rgba(15,23,42,0.04)" }}>
                        <h3 style={{ marginTop: 0 }}>POI Distribution (Radar)</h3>
                        <ResponsiveContainer width="100%" height={300}>
                            <RadarChart data={radarData}>
                                <PolarGrid />
                                <PolarAngleAxis dataKey="POI" />
                                <Radar name="score" dataKey="score" stroke="#2c7be5" fill="#2c7be5" fillOpacity={0.15} />
                                <Tooltip />
                            </RadarChart>
                        </ResponsiveContainer>
                    </div>

                    <div style={{ background: "#ffffff", padding: 12, borderRadius: 8, border: "1px solid rgba(15,23,42,0.04)" }}>
                        <h3 style={{ marginTop: 0 }}>Top Counts</h3>
                        <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
                            {Object.entries(analysis.categories).map(([k, v]: any) => (
                                <div key={k} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: 8, background: "rgba(255,255,255,0.01)", borderRadius: 8 }}>
                                    <div style={{ textTransform: "capitalize" }}>{k}</div>
                                    <div style={{ fontWeight: 700 }}>{(v.pois || []).length}</div>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>

                <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12, marginTop: 12 }}>
                    <div style={{ background: "#ffffff", padding: 12, borderRadius: 8, border: "1px solid rgba(15,23,42,0.04)" }}>
                        <h3 style={{ marginTop: 0 }}>POI Counts (Bar)</h3>
                        <ResponsiveContainer width="100%" height={220}>
                            <BarChart data={barData} layout="vertical">
                                <XAxis type="number" />
                                <YAxis dataKey="name" type="category" />
                                <Tooltip />
                                <Bar dataKey="count" fill="#2c7be5" />
                            </BarChart>
                        </ResponsiveContainer>
                    </div>

                    <div style={{ background: "#ffffff", padding: 12, borderRadius: 8, border: "1px solid rgba(15,23,42,0.04)" }}>
                        <h3 style={{ marginTop: 0 }}>Competitor vs Others</h3>
                        <ResponsiveContainer width="100%" height={220}>
                            <PieChart>
                                <Pie data={donutData} dataKey="value" nameKey="name" innerRadius={50} outerRadius={80} label>
                                    {donutData.map((entry, idx) => (
                                        <Cell key={idx} fill={idx === 0 ? "#ef4444" : "#2c7be5"} />
                                    ))}
                                </Pie>
                                <Tooltip />
                            </PieChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                <div style={{ marginTop: 12, display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(220px,1fr))", gap: 12 }}>
                    {Object.entries(analysis.categories).map(([cat, v]: any) => (
                        <div key={cat} style={{ background: "#ffffff", padding: 10, borderRadius: 8, border: "1px solid rgba(15,23,42,0.04)" }}>
                            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 8 }}>
                                <div style={{ textTransform: "capitalize", fontWeight: 700 }}>{cat}</div>
                                <div style={{ color: "#475569" }}>{`score ${v.score}`}</div>
                            </div>
                            <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
                                {(v.pois || []).slice(0, 10).map((p: Poi, i: number) => (
                                    <div key={i} style={{ display: "flex", justifyContent: "space-between", gap: 8, padding: 6, background: "rgba(255,255,255,0.01)", borderRadius: 6 }}>
                                        <div>
                                            <div style={{ fontWeight: 600 }}>{p.name}</div>
                                            <div style={{ color: "#64748b", fontSize: 12 }}>{`${p.lat.toFixed(6)}, ${p.lng.toFixed(6)}`}</div>
                                        </div>
                                        <div style={{ textAlign: "right" }}>
                                            <div style={{ fontWeight: 700 }}>{p.distance_km} km</div>
                                            <div style={{ color: "#64748b", fontSize: 12 }}>{`w:${p.weight}`}</div>
                                        </div>
                                    </div>
                                ))}
                                {(v.pois || []).length === 0 && <div style={{ color: "#9fb0c9" }}>No POIs</div>}
                            </div>
                        </div>
                    ))}
                </div>

                <div style={{ marginTop: 16 }}>
                    <button onClick={() => window.history.back()} style={{ background: "#2563eb", color: "white", padding: "10px 14px", borderRadius: 8, border: 0 }}>Back</button>
                </div>
            </div>
        </div>
    );
}
