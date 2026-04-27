import React, { useEffect, useRef, useMemo } from 'react';
import { Marker, GeoJSON, useMap, Circle } from 'react-leaflet';
import * as L from 'leaflet';
import { useExploreStore } from '@/store/exploreStore';

// ============================================================================
// ICONS
// ============================================================================
export function getDatasetIcon(type: string) {
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
    return L.divIcon({ className: `\${type}-icon`, html, iconSize: [24, 24], iconAnchor: [12, 24] });
}

export function selectedPoiIcon(type: string) {
    const raw = getDatasetIcon(type).options.html;
    const html = `
        <div style="position:relative; width:40px; height:40px; display:flex; align-items:center; justify-content:center;">
        <div style="position:absolute; width:100%; height:100%; background:rgba(79,70,229,0.3); border-radius:50%; animation: ping 2s cubic-bezier(0,0,0.2,1) infinite;"></div>
        <div style="position:relative; transform:scale(1.2); box-shadow:0 4px 12px rgba(0,0,0,0.5); border-radius:9999px;">
            \${raw}
        </div>
        </div>
    `;
    return L.divIcon({ className: `\${type}-icon-selected`, html, iconSize: [40, 40], iconAnchor: [20, 20] });
}

export const poiIcon = (type: string) => {
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
        html: `<div style="background:\${c};width:10px;height:10px;border-radius:50%;border:1px solid white;box-shadow:0 0 4px rgba(0,0,0,0.4)"></div>`,
        iconSize: [10, 10],
        iconAnchor: [5, 5],
    });
};

// ============================================================================
// OVERLAY COMPONENTS
// ============================================================================
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
                const latlng = ((layer as any).getLatLng && (layer as any).getLatLng()) || null;
                if (latlng) {
                    map.flyTo(latlng, 16, { animate: true });
                }
            } catch (e) { }
        }
    }, [selectedFeatureId, geoData, map]);

    if (!geoData) return null;

    return (
        <GeoJSON
            key={`\${datasetId}-\${selectedFeatureId ?? 'none'}`}
            data={geoData}
            pointToLayer={(feature, latlng) => {
                const fid = feature.id ?? feature.properties?.name ?? null;
                const isSelected = fid != null && fid === selectedFeatureId;
                const marker = L.marker(latlng, { icon: isSelected ? selectedPoiIcon(datasetId) : getDatasetIcon(datasetId) });
                if (fid != null) layerMap.current[fid] = marker;
                return marker;
            }}
            onEachFeature={(feature, layer) => {
                layer.on("click", () => onFeatureClick(feature, layer));
            }}
        />
    );
}

export const ExploreOverlays = () => {
    const lat = useExploreStore(state => state.lat);
    const lng = useExploreStore(state => state.lng);
    const radiusKm = useExploreStore(state => state.radiusKm);
    
    // Directory state
    const showPlaces = useExploreStore(state => state.showPlaces);
    const showWithinRadius = useExploreStore(state => state.showWithinRadius);
    const selectedFeatureId = useExploreStore(state => state.selectedFeatureId);
    const setSelectedFeatureId = useExploreStore(state => state.setSelectedFeatureId);
    
    // Derived/Filtered Data logic from Directory panel replicated/passed 
    const geoDataList = useExploreStore(state => state.geoDataList);
    const datasetId = useExploreStore(state => state.datasetId);
    const searchQuery = useExploreStore(state => state.searchQuery);
    
    const poiLat = useExploreStore(state => state.poiLat);
    const poiLng = useExploreStore(state => state.poiLng);
    const setPoiLat = useExploreStore(state => state.setPoiLat);
    const setPoiLng = useExploreStore(state => state.setPoiLng);
    const poisFlat = useExploreStore(state => state.poisFlat);

    // Distance calculation logic 
    const distanceKm = (aLat: number, aLon: number, bLat: number, bLon: number) => {
        const toRad = (v: number) => (v * Math.PI) / 180;
        const R = 6371; 
        const dLat = toRad(bLat - aLat);
        const dLon = toRad(bLon - aLon);
        const lat1 = toRad(aLat);
        const lat2 = toRad(bLat);
        const u = Math.sin(dLat / 2) * Math.sin(dLat / 2) + Math.sin(dLon / 2) * Math.sin(dLon / 2) * Math.cos(lat1) * Math.cos(lat2);
        const c = 2 * Math.atan2(Math.sqrt(u), Math.sqrt(1 - u));
        return R * c;
    };

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
                            const coords = f.geometry?.type === 'Point' 
                                ? f.geometry.coordinates 
                                : (f.geometry?.coordinates && f.geometry.coordinates[0]);
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

    return (
        <>
            {/* Draw Radius Circle */}
             <Circle
                center={[lat, lng]}
                radius={radiusKm * 1000} // km to meters
                pathOptions={{ color: "#3b82f6", fillColor: "#3b82f6", fillOpacity: 0.05, weight: 1, dashArray: "4,4" }}
            />

            {showPlaces && !showWithinRadius && filteredGeoData.map((item) => (
                <MapFeatures
                    key={item.id}
                    datasetId={item.id}
                    geoData={{ type: 'FeatureCollection', features: item.features }}
                    selectedFeatureId={selectedFeatureId}
                    onFeatureClick={(feature, _layer) => {
                        try {
                            const coords = feature.geometry.type === "Point" 
                                ? feature.geometry.coordinates 
                                : feature.geometry.coordinates[0];
                            setPoiLat(coords[1]);
                            setPoiLng(coords[0]);
                        } catch { }
                        setSelectedFeatureId(feature.properties?.name ?? feature.id ?? null);
                    }}
                />
            ))}

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
                        const fid = f.id ?? f.properties?.id ?? `\${ds.id}-\${idx}`;
                        const isSelectedDs = Math.abs(flat - poiLat) < 1e-6 && Math.abs(flon - poiLng) < 1e-6;
                        return (
                            <Marker
                                key={`\${ds.id}-\${fid}`}
                                position={[flat, flon]}
                                icon={isSelectedDs ? selectedPoiIcon(ds.id) : getDatasetIcon(ds.id)}
                                zIndexOffset={isSelectedDs ? 1000 : 0}
                                eventHandlers={{
                                    click: () => {
                                        setPoiLat(flat);
                                        setPoiLng(flon);
                                        setSelectedFeatureId(f.properties?.name ?? fid);
                                    }
                                }}
                            />
                        );
                    } catch (e) {
                        return null;
                    }
                })
            ))}

            {Object.entries(poisFlat.reduce((acc: Record<string, any[]>, p: any) => { 
                (acc[p.type] = acc[p.type] || []).push(p); return acc; 
            }, {})).map(([type, items]: any) => (
                (items as any[]).map((p: any, idx: number) => {
                    const key = `\${type}-\${idx}`;
                    const plat = Number(p.lat);
                    const plon = Number(p.lon);
                    const isSelected = Math.abs(plat - poiLat) < 1e-6 && Math.abs(plon - poiLng) < 1e-6;
                    return (
                        <Marker
                            key={key}
                            position={[plat, plon]}
                            icon={isSelected ? selectedPoiIcon(type) : poiIcon(type)}
                            zIndexOffset={isSelected ? 1000 : 0}
                        />
                    );
                })
            ))}
        </>
    );
};