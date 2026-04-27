import React, { useEffect, useRef } from "react";
import { MapContainer, TileLayer, Marker, useMapEvents, useMap } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import * as L from "leaflet";
import { useExploreStore } from "@/store/exploreStore";
import { ExploreOverlays } from "./ExploreOverlays";

// ============================================================================
// ICONS
// ============================================================================
export const pointPickIcon = L.divIcon({
  className: "point-marker",
  html: `<div style="width:24px;height:24px;background:#1e293b;border-radius:50%;border:2px solid white;box-shadow:0 0 8px rgba(0,0,0,0.3)"></div>`,
  iconSize: [24, 24],
  iconAnchor: [12, 12],
});

export const toLetPickIcon = L.divIcon({
  className: "tolet-marker",
  html: `<div style="width:24px;height:24px;background:#10b981;border-radius:50%;border:2px solid white;box-shadow:0 0 8px rgba(0,0,0,0.3)"></div>`,
  iconSize: [24, 24],
  iconAnchor: [12, 12],
});

export const toLetHoverIcon = L.divIcon({
  className: "tolet-hover",
  html: `<div style="width:32px;height:32px;background:rgba(16,185,129,0.4);border-radius:50%;border:2px solid #10b981;box-shadow:0 0 12px rgba(16,185,129,0.6);animation:pulse 2s infinite"></div>`,
  iconSize: [32, 32],
  iconAnchor: [16, 16],
});

// ============================================================================
// HELPER COMPONENTS
// ============================================================================
function MapResizeHandler() {
  const map = useMap();
  useEffect(() => {
    const to = setTimeout(() => map.invalidateSize(), 300);
    return () => clearTimeout(to);
  }, [map]);
  return null;
}

function MapRefSetter({ mapRef }: { mapRef: React.MutableRefObject<L.Map | null> }) {
  const map = useMap();
  useEffect(() => {
    mapRef.current = map;
  }, [map, mapRef]);
  return null;
}

function MapPicker({ lat, lng, onPick }: { lat: number; lng: number; onPick: (lat: number, lng: number) => void }) {
  useMapEvents({
    click(e) {
      onPick(e.latlng.lat, e.latlng.lng);
    },
  });
  return null;
}

// ============================================================================
// CONSTANTS
// ============================================================================
const MAP_BOUNDS: L.LatLngBoundsExpression = [
  [27.60, 85.25], // SW corner (approximate Kathmandu limits)
  [27.75, 85.45], // NE corner
];

// ============================================================================
// MAIN COMPONENT
// ============================================================================
export const ExploreMap = () => {
    const lat = useExploreStore(state => state.lat);
    const lng = useExploreStore(state => state.lng);
    const pointList = useExploreStore(state => state.pointList);
    const toLetList = useExploreStore(state => state.toLetList);
    const selectedToLetList = useExploreStore(state => state.toLetList.filter((p: any) => state.toLetSelected[`${p.lat.toFixed(6)},${p.lng.toFixed(6)}`]));
    const analysisMode = useExploreStore(state => state.analysisMode);
    
    // Derived mapPickList
    const mapPickList = analysisMode === "point" 
        ? (Object.keys(useExploreStore(state => state.pointSelected)).length > 0
            ? pointList.filter((p: any) => useExploreStore.getState().pointSelected[`${p.lat.toFixed(6)},${p.lng.toFixed(6)}`])
            : pointList)
        : selectedToLetList;
        
    const hoverToLet = useExploreStore(state => state.hoverToLet);

    // Callbacks
    const setLat = useExploreStore(state => state.setLat);
    const setLng = useExploreStore(state => state.setLng);
    const setPointList = useExploreStore(state => state.setPointList);
    const setPointSelected = useExploreStore(state => state.setPointSelected);
    const setToLetList = useExploreStore(state => state.setToLetList);
    const setToLetSelected = useExploreStore(state => state.setToLetSelected);

    const mapRef = useRef<L.Map | null>(null);

    const toKey = (p: { lat: number; lng: number }) => `${p.lat.toFixed(6)},${p.lng.toFixed(6)}`;
    
    const addPointToActiveList = (p: { lat: number; lng: number }) => {
        setLat(p.lat);
        setLng(p.lng);
        if (analysisMode === "point") {
            const pointSelected = useExploreStore.getState().pointSelected;
            setPointList([...pointList, p]);
            setPointSelected({ ...pointSelected, [toKey(p)]: true });
        } else {
            const toLetSelected = useExploreStore.getState().toLetSelected;
            setToLetList([...toLetList, p]);
            setToLetSelected({ ...toLetSelected, [toKey(p)]: true });
        }
    };

    return (
        <div className="flex-1 w-full relative min-h-[480px] bg-transparent z-0 group">
            <MapContainer
                center={[lat, lng]}
                zoom={16} // Standard default zoom
                className="h-full w-full bg-transparent"
                scrollWheelZoom
                minZoom={13}
                maxBounds={MAP_BOUNDS}
                maxBoundsViscosity={1.0}
            >
                <TileLayer
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                    attribution='&copy; <a href="https://osm.org/copyright">OpenStreetMap</a>'
                />
                
                <MapResizeHandler />
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

                <ExploreOverlays />
            </MapContainer>
        </div>
    );
};