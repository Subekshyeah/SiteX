import React, { createContext, useContext, useState } from 'react';
import type { ReactNode } from 'react';
import type { Map as LeafletMap } from 'leaflet';

type MapState = {
  map?: LeafletMap | null;
  sidebarOpen: boolean;
  selectedPlace?: string | null;
};

type MapContextValue = {
  mapState: MapState;
  setMapState: React.Dispatch<React.SetStateAction<MapState>>;
};

export const MapContext = createContext<MapContextValue>({
  mapState: { map: null, sidebarOpen: true, selectedPlace: null },
  // eslint-disable-next-line @typescript-eslint/no-empty-function
  setMapState: () => {},
});

export const MapProvider = ({ children }: { children: ReactNode }) => {
  const [mapState, setMapState] = useState<MapState>({
    map: null,
    sidebarOpen: true,
    selectedPlace: null,
  });

  return (
    <MapContext.Provider value={{ mapState, setMapState }}>
      {children}
    </MapContext.Provider>
  );
};

export const useMap = (): MapContextValue => {
    const context = useContext(MapContext);
    if (!context) {
        throw new Error('useMap must be used within a MapProvider');
    }
    return context;
};