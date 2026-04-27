import React, { useMemo } from 'react';
import { useExploreStore, DATASETS } from '@/store/exploreStore';
import { Input } from '@/components/ui/input';
import { ChevronDown, ChevronRight, X } from 'lucide-react';
import { Button } from '@/components/ui/button';

export const ExploreDirectory = () => {
    // Zustand store bindings
    const showPlaces = useExploreStore(state => state.showPlaces);
    const searchQuery = useExploreStore(state => state.searchQuery);
    const setSearchQuery = useExploreStore(state => state.setSearchQuery);
    const radiusKm = useExploreStore(state => state.radiusKm);
    const setRadiusKm = useExploreStore(state => state.setRadiusKm);
    const datasetId = useExploreStore(state => state.datasetId);
    const setDatasetId = useExploreStore(state => state.setDatasetId);
    const geoDataList = useExploreStore(state => state.geoDataList);
    const showWithinRadius = useExploreStore(state => state.showWithinRadius);
    const setShowWithinRadius = useExploreStore(state => state.setShowWithinRadius);
    
    const lat = useExploreStore(state => state.lat);
    const lng = useExploreStore(state => state.lng);
    const setPoiLat = useExploreStore(state => state.setPoiLat);
    const setPoiLng = useExploreStore(state => state.setPoiLng);
    const poiLat = useExploreStore(state => state.poiLat);
    const poiLng = useExploreStore(state => state.poiLng);

    // Distance calculation logic for filtering inside the panel
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

    if (!showPlaces) return null;

    return (
        <div className="absolute top-4 right-4 z-[1000] w-80 max-w-[calc(100vw-32px)]">
            <div className="bg-white/90 backdrop-blur-md rounded-xl shadow-xl p-3 border border-slate-200">
                {/* Search Header */}
                <div className="flex items-center gap-2 mb-3">
                    <input
                        type="search"
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        placeholder="Search places..."
                        className="flex-1 px-3 py-2 bg-white/50 border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500"
                    />
                    <div className="flex items-center gap-1 bg-white/50 border rounded-lg px-2">
                        <Input
                            type="number"
                            value={radiusKm}
                            onChange={(e) => setRadiusKm(Number(e.target.value) || 0)}
                            step="0.1"
                            min="0.1"
                            max="5"
                            className="w-12 px-1 py-2 text-center text-sm border-none bg-transparent h-9"
                        />
                        <span className="text-xs font-medium text-slate-500">km</span>
                    </div>
                </div>

                {/* Filter / Datasets Row */}
                <div className="overflow-x-auto pb-2 scrollbar-none">
                    <div className="flex items-center gap-1.5 flex-nowrap min-w-max">
                        <Button 
                            variant={showWithinRadius ? "default" : "outline"}
                            size="sm"
                            className={`rounded-full h-7 px-3 text-xs shadow-sm whitespace-nowrap \${showWithinRadius ? 'bg-indigo-600 hover:bg-indigo-700 text-white border-transparent' : 'bg-white hover:bg-slate-50 text-slate-700'}`}
                            onClick={() => setShowWithinRadius(!showWithinRadius)}
                        >
                            Filter by Radius ({radiusKm}km)
                        </Button>
                        
                        {DATASETS.map((d) => {
                            if (!d.path && d.id !== 'all') return null;
                            const isSel = datasetId === d.id;
                            const count = getDatasetCount(d.id);
                            return (
                                <Button
                                    key={d.id}
                                    variant={isSel ? "default" : "outline"}
                                    size="sm"
                                    onClick={() => setDatasetId(d.id)}
                                    className={`rounded-full h-7 px-3 text-xs shadow-sm transition-colors whitespace-nowrap \${
                                        isSel 
                                            ? 'bg-slate-800 hover:bg-slate-900 text-white border-transparent' 
                                            : count !== null && count > 0 
                                                ? 'bg-white hover:bg-slate-50 text-slate-700 border-slate-200' 
                                                : 'bg-slate-50/50 hover:bg-slate-50 text-slate-400 border-slate-100 opacity-60'
                                    }`}
                                >
                                    {d.name} {count !== null ? `(\${count})` : ''}
                                </Button>
                            );
                        })}
                    </div>
                </div>

                {/* POI Listing */}
                <div className="max-h-[300px] overflow-y-auto mt-2 pr-1 space-y-3 custom-scrollbar">
                    {filteredGeoData.map((ds) => (
                        <div key={ds.id}>
                            <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2 sticky top-0 bg-white/90 backdrop-blur pb-1 z-10">
                                {ds.name} <span className="font-normal opacity-70">({ds.features.length})</span>
                            </h4>
                            <ul className="space-y-1.5">
                                {(ds.features || []).map((f: any, idx: number) => {
                                    try {
                                        const geom = f.geometry;
                                        if (!geom) return null;
                                        const coords = geom.type === 'Point' 
                                            ? geom.coordinates 
                                            : (geom.coordinates && geom.coordinates[0]);
                                        if (!coords || coords.length < 2) return null;
                                        
                                        const flon = Number(coords[0]);
                                        const flat = Number(coords[1]);
                                        const d = distanceKm(lat, lng, flat, flon);
                                        const fid = f.id ?? f.properties?.id ?? `\${ds.id}-\${idx}`;
                                        
                                        const isSelectedDs = Math.abs(flat - (poiLat || 0)) < 1e-6 && Math.abs(flon - (poiLng || 0)) < 1e-6;

                                        return (
                                            <li
                                                key={`\${ds.id}-\${fid}`}
                                                className={`text-xs p-2.5 rounded-lg border cursor-pointer transition-all duration-200 \${
                                                    isSelectedDs 
                                                        ? 'bg-indigo-50 border-indigo-200 shadow-sm' 
                                                        : 'bg-white border-slate-100 hover:border-slate-300 hover:shadow-sm hover:bg-slate-50'
                                                }`}
                                                onClick={() => {
                                                    setPoiLat(flat);
                                                    setPoiLng(flon);
                                                }}
                                            >
                                                <div className="font-medium text-slate-800 line-clamp-1">
                                                    {f.properties?.name || 'Unnamed'}
                                                </div>
                                                <div className="flex items-center justify-between mt-1 text-[10px] text-slate-500">
                                                    {Number.isFinite(d) && 
                                                        <span className="flex items-center gap-1 opacity-80">
                                                            <span>📍</span>
                                                            {(d * 1000).toFixed(0)}m
                                                        </span>
                                                    }
                                                </div>
                                            </li>
                                        );
                                    } catch (e) {
                                        return null;
                                    }
                                })}
                            </ul>
                        </div>
                    ))}
                    {filteredGeoData.length === 0 && (
                        <div className="text-center py-6 text-sm text-slate-400">
                            No matching places found.
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};