import { useEffect } from 'react';
import { useExploreStore } from '@/store/exploreStore';
import { Card, CardContent, CardTitle, CardHeader } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Switch } from '@/components/ui/switch';
import { MapPin, X } from 'lucide-react';
import React, { useState } from 'react';

export const SidebarPanel = () => {
    // Local state for the static form fields (could optionally go in Zustand, but fine here)
    const [name, setName] = useState("");

    // State pulled from our new Zustand store
    const lat = useExploreStore(state => state.lat);
    const lng = useExploreStore(state => state.lng);
    const radiusKm = useExploreStore(state => state.radiusKm);
    const analysisMode = useExploreStore(state => state.analysisMode);
    
    const pointList = useExploreStore(state => state.pointList);
    const pointSelected = useExploreStore(state => state.pointSelected);
    const toLetList = useExploreStore(state => state.toLetList);
    const toLetSelected = useExploreStore(state => state.toLetSelected);

    // Setters
    const setLat = useExploreStore(state => state.setLat);
    const setLng = useExploreStore(state => state.setLng);
    const setRadiusKm = useExploreStore(state => state.setRadiusKm);
    const setAnalysisMode = useExploreStore(state => state.setAnalysisMode);
    const setPointSelected = useExploreStore(state => state.setPointSelected);
    const setPointList = useExploreStore(state => state.setPointList);

    const toKey = (p: { lat: number; lng: number }) => `${p.lat.toFixed(6)},${p.lng.toFixed(6)}`;

    const addPointToActiveList = (p: { lat: number; lng: number }) => {
        setLat(p.lat);
        setLng(p.lng);
        if (analysisMode === "point") {
            setPointList([...pointList, p]);
            setPointSelected({ ...pointSelected, [toKey(p)]: true });
        }
    };

    const removeFromPointList = (idx: number) => {
        const p = pointList[idx];
        const nextList = pointList.filter((_, i) => i !== idx);
        setPointList(nextList);
        
        if (p) {
            const nextSel = { ...pointSelected };
            delete nextSel[toKey(p)];
            setPointSelected(nextSel);
        }
    };

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        console.log("Submitting:", { name, lat, lng, analysisMode });
        // NOTE: Navigation and route logic goes here
    };

    return (
        <Card className="h-full border-r border-t-0 border-b-0 border-l-0 rounded-none bg-white/70 backdrop-blur-xl shadow-[4px_0_24px_-12px_rgba(0,0,0,0.1)] z-10 flex flex-col w-full md:w-[28rem] overflow-y-auto p-3 md:p-4">
            <CardHeader className="pb-4">
                <CardTitle className="flex items-center gap-3 text-2xl font-semibold">
                    <MapPin className="w-6 h-6" />
                    Location Analysis
                </CardTitle>
            </CardHeader>

            <CardContent className={analysisMode === "tolet" ? "p-2" : undefined}>
                <form onSubmit={handleSubmit} className="space-y-6">
                    <div>
                        <Label htmlFor="name">Location Name</Label>
                        <Input
                            id="name"
                            placeholder="Store or Site Name"
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
                            <Label>Latitude</Label>
                            <Input 
                              type="number" 
                              step="any" 
                              value={lat} 
                              onChange={(e) => setLat(parseFloat(e.target.value))} 
                              className="mt-1 font-mono text-sm" 
                            />
                        </div>
                        <div>
                            <Label>Longitude</Label>
                            <Input 
                              type="number" 
                              step="any" 
                              value={lng} 
                              onChange={(e) => setLng(parseFloat(e.target.value))} 
                              className="mt-1 font-mono text-sm" 
                            />
                        </div>
                    </div>
                    
                    <div className="space-y-2">
                        <Label>Search Radius ({radiusKm} km)</Label>
                        <input
                            type="range"
                            min="0.1"
                            max="5.0"
                            step="0.1"
                            value={radiusKm}
                            onChange={(e) => setRadiusKm(parseFloat(e.target.value))}
                            className="w-full"
                        />
                    </div>

                    {analysisMode === "point" ? (
                        <div className="space-y-2">
                            <Label>Point list</Label>
                            <div className="flex gap-2">
                                <Button type="button" variant="outline" onClick={() => setPointSelected({})}>
                                    Clear selection
                                </Button>
                                <Button type="button" onClick={() => addPointToActiveList({ lat, lng })}>
                                    Add current
                                </Button>
                            </div>
                            <ul className="space-y-1 max-h-40 overflow-auto border rounded p-1">
                                {pointList.length === 0 && <li className="text-xs text-muted-foreground p-1">No points added.</li>}
                                {pointList.map((p, idx) => {
                                    const key = toKey(p);
                                    return (
                                        <li key={key} className="flex items-center justify-between text-xs bg-slate-50 px-2 py-1 rounded">
                                            <div className="flex items-center gap-2">
                                                <input
                                                    type="checkbox"
                                                    checked={!!pointSelected[key]}
                                                    onChange={(e) => setPointSelected({ ...pointSelected, [key]: e.target.checked })}
                                                />
                                                <span className="font-mono">{p.lat.toFixed(5)}, {p.lng.toFixed(5)}</span>
                                            </div>
                                            <button type="button" onClick={() => removeFromPointList(idx)} className="text-slate-400 hover:text-red-500">
                                                <X className="w-4 h-4" />
                                            </button>
                                        </li>
                                    );
                                })}
                            </ul>
                        </div>
                    ) : (
                        <div className="space-y-2">
                            <Label>To-Let List Coming Soon</Label>
                            {/* Will migrate renderToLetList logic here shortly */}
                        </div>
                    )}

                    <Button type="submit" className="w-full py-6 text-lg font-bold shadow-lg bg-indigo-600 hover:bg-indigo-700">
                        Analyze {analysisMode === 'point' ? 'Points' : 'Properties'}
                    </Button>
                </form>
            </CardContent>
        </Card>
    );
};