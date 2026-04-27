import { create } from 'zustand';

interface ToLetEntry {
  key: string;
  lat: number;
  lng: number;
  title: string;
  url?: string;
  images?: string[];
  [key: string]: any;
}

interface GeoData {
  id: string;
  name: string;
  data: any;
}

export const DATASETS = [
    { id: 'all', name: 'All', path: '' },
    { id: 'cafes', name: 'Cafes', path: '/data/cafes.geojson' },
    { id: 'temples', name: 'Temples', path: '/data/temples.geojson' },
    { id: 'banks', name: 'Banks', path: '/data/banks.geojson' },
    { id: 'education', name: 'Education', path: '/data/education.geojson' },
    { id: 'health', name: 'Health', path: '/data/health.geojson' },
    { id: 'other', name: 'Other', path: '/data/other.geojson' },
  ];

interface ExploreState {
  // Map parameters
  lat: number;
  lng: number;
  radiusKm: number;
  setLat: (val: number) => void;
  setLng: (val: number) => void;
  setRadiusKm: (val: number) => void;

  // Analysis Modes
  analysisMode: "point" | "tolet";
  setAnalysisMode: (mode: "point" | "tolet") => void;

  // Lists and Data
  pointList: Array<{ lat: number; lng: number }>;
  setPointList: (list: Array<{ lat: number; lng: number }>) => void;
  toLetList: Array<{ lat: number; lng: number }>;
  setToLetList: (list: Array<{ lat: number; lng: number }>) => void;
  toLetEntries: ToLetEntry[];
  setToLetEntries: (entries: ToLetEntry[]) => void;
  
  // Selection & Hover
  toLetSelected: Record<string, boolean>;
  setToLetSelected: (sel: Record<string, boolean>) => void;
  pointSelected: Record<string, boolean>;
  setPointSelected: (sel: Record<string, boolean>) => void;
  hoverToLet: { lat: number; lng: number } | null;
  setHoverToLet: (val: { lat: number; lng: number } | null) => void;

  // POI & Datasets
  poisData: any | null;
  setPoisData: (data: any | null) => void;
  poisFlat: Array<any>;
  setPoisFlat: (data: Array<any>) => void;
  poiLoading: boolean;
  setPoiLoading: (val: boolean) => void;
  
  expandedPoi: string | null;
  setExpandedPoi: (id: string | null) => void;

  datasetId: string;
  setDatasetId: (id: string) => void;
  geoDataList: GeoData[];
  setGeoDataList: (list: GeoData[]) => void;
  
  // Display Flags
  showPlaces: boolean;
  setShowPlaces: (val: boolean) => void;
  showWithinRadius: boolean;
  setShowWithinRadius: (val: boolean) => void;
  geoLoading: boolean;
  setGeoLoading: (val: boolean) => void;
  
  // CSV & Features
  searchQuery: string;
  setSearchQuery: (query: string) => void;
  selectedFeatureId: string | number | null;
  setSelectedFeatureId: (id: string | number | null) => void;
  
  poiLat: number;
  setPoiLat: (val: number) => void;
  poiLng: number;
  setPoiLng: (val: number) => void;
  
  csvRows: Array<Record<string, string>> | null;
  setCsvRows: (rows: Array<Record<string, string>> | null) => void;
  selectedCsvRow: Record<string, string> | null;
  setSelectedCsvRow: (row: Record<string, string> | null) => void;
}

export const useExploreStore = create<ExploreState>((set) => ({
  lat: 27.670587,
  lng: 85.420868,
  radiusKm: 0.5,
  setLat: (lat) => set({ lat }),
  setLng: (lng) => set({ lng }),
  setRadiusKm: (radiusKm) => set({ radiusKm }),

  analysisMode: "point",
  setAnalysisMode: (analysisMode) => set({ analysisMode }),

  pointList: [],
  setPointList: (pointList) => set({ pointList }),
  toLetList: [], 
  setToLetList: (toLetList) => set({ toLetList }),
  toLetEntries: [],
  setToLetEntries: (toLetEntries) => set({ toLetEntries }),

  toLetSelected: {},
  setToLetSelected: (toLetSelected) => set({ toLetSelected }),
  pointSelected: {},
  setPointSelected: (pointSelected) => set({ pointSelected }),
  hoverToLet: null,
  setHoverToLet: (hoverToLet) => set({ hoverToLet }),

  poisData: null,
  setPoisData: (poisData) => set({ poisData }),
  poisFlat: [],
  setPoisFlat: (poisFlat) => set({ poisFlat }),
  poiLoading: false,
  setPoiLoading: (poiLoading) => set({ poiLoading }),
  
  expandedPoi: null,
  setExpandedPoi: (expandedPoi) => set({ expandedPoi }),

  datasetId: 'all',
  setDatasetId: (datasetId) => set({ datasetId }),
  geoDataList: [],
  setGeoDataList: (geoDataList) => set({ geoDataList }),

  showPlaces: false,
  setShowPlaces: (showPlaces) => set({ showPlaces }),
  showWithinRadius: true,
  setShowWithinRadius: (showWithinRadius) => set({ showWithinRadius }),
  geoLoading: false,
  setGeoLoading: (geoLoading) => set({ geoLoading }),

  searchQuery: "",
  setSearchQuery: (searchQuery) => set({ searchQuery }),
  selectedFeatureId: null,
  setSelectedFeatureId: (selectedFeatureId) => set({ selectedFeatureId }),

  poiLat: 0,
  setPoiLat: (poiLat) => set({ poiLat }),
  poiLng: 0,
  setPoiLng: (poiLng) => set({ poiLng }),

  csvRows: null,
  setCsvRows: (csvRows) => set({ csvRows }),
  selectedCsvRow: null,
  setSelectedCsvRow: (selectedCsvRow) => set({ selectedCsvRow }),
}));
