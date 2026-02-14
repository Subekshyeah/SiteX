import json
import math
import os
import pickle
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

import networkx as nx
import numpy as np

try:
    from scipy.spatial import cKDTree
except ImportError:  # pragma: no cover
    cKDTree = None


ROAD_TYPE_WEIGHTS: Dict[str, float] = {
    "motorway": 1.6,
    "trunk": 1.5,
    "primary": 1.4,
    "secondary": 1.3,
    "tertiary": 1.2,
    "residential": 1.0,
    "unclassified": 1.0,
    "road": 1.0,
    "service": 0.9,
    "living_street": 0.9,
    "track": 0.8,
    "path": 0.8,
    "cycleway": 0.8,
    "footway": 0.7,
    "pedestrian": 0.7,
    "steps": 0.7,
    "construction": 1.1,
}


def _haversine_pair(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Return haversine distance in meters between two points."""
    r = 6371000.0
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = phi2 - phi1
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2.0) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2.0) ** 2
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return r * c


def _haversine_vec(
    lat1: np.ndarray, lon1: np.ndarray, lat2: np.ndarray, lon2: np.ndarray
) -> np.ndarray:
    """Vectorized haversine distance in meters for arrays."""
    r = 6371000.0
    phi1 = np.radians(lat1)
    phi2 = np.radians(lat2)
    dphi = phi2 - phi1
    dlambda = np.radians(lon2 - lon1)
    a = np.sin(dphi / 2.0) ** 2 + np.cos(phi1) * np.cos(phi2) * np.sin(dlambda / 2.0) ** 2
    c = 2.0 * np.arctan2(np.sqrt(a), np.sqrt(1.0 - a))
    return r * c


def _normalize_road_type(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, (list, tuple)):
        if not value:
            return None
        value = value[0]
    if not isinstance(value, str):
        value = str(value)
    value = value.strip().lower()
    return value or None


class RoadTypeNetwork:
    """Road network graph that tracks road types and weighted travel distances."""

    _CACHE_SCHEMA_VERSION = 1

    def __init__(
        self,
        graph: nx.Graph,
        node_coords: np.ndarray,
        snap_tolerance_m: float = 120.0,
    ) -> None:
        self.graph = graph
        self.node_coords = node_coords.astype(np.float64)
        self.snap_tolerance_m = max(float(snap_tolerance_m), 0.0)
        self._tree = self._build_tree()

    @classmethod
    def from_geojson(
        cls,
        geojson_path: str,
        cache_path: Optional[str] = None,
        snap_tolerance_m: float = 120.0,
    ) -> "RoadTypeNetwork":
        source_path = os.fspath(geojson_path)
        cache_path = os.fspath(cache_path) if cache_path else None
        if cache_path and cls._cache_is_valid(cache_path, source_path):
            try:
                return cls._load_cache(cache_path, snap_tolerance_m)
            except Exception:
                pass
        graph, coords = cls._build_graph_from_geojson(source_path)
        instance = cls(graph, coords, snap_tolerance_m)
        if cache_path:
            instance._save_cache(cache_path)
        return instance

    @property
    def node_count(self) -> int:
        return int(self.node_coords.shape[0])

    def snap_point(self, lat: float, lon: float, max_snap_m: Optional[float] = None) -> Tuple[Optional[int], Optional[float]]:
        if self.node_count == 0:
            return None, None
        idx = self._nearest_node_index(lat, lon)
        if idx is None:
            return None, None
        node_lat, node_lon = self.node_coords[idx]
        dist = _haversine_pair(lat, lon, float(node_lat), float(node_lon))
        threshold = max_snap_m if max_snap_m is not None else self.snap_tolerance_m
        if threshold <= 0.0 or dist <= threshold:
            return int(idx), float(dist)
        return None, None

    def road_types_for_node(self, node_id: int) -> List[str]:
        data = self.graph.nodes.get(int(node_id))
        if not data:
            return []
        types = data.get("road_types")
        if isinstance(types, set):
            return sorted(types)
        if isinstance(types, (list, tuple)):
            return sorted(set(types))
        if isinstance(types, str):
            return [types]
        return []

    def road_type_distance_map(
        self,
        center_lat: float,
        center_lon: float,
        radius_m: float,
        secondary_snap_tolerance_m: float = 300.0,
    ) -> Optional[Dict[str, Any]]:
        center_node, center_offset = self.snap_point(
            center_lat,
            center_lon,
            max_snap_m=self.snap_tolerance_m,
        )
        if center_node is None:
            center_node, center_offset = self.snap_point(
                center_lat, center_lon, max_snap_m=secondary_snap_tolerance_m
            )
        if center_node is None:
            center_node, center_offset = self.snap_point(
                center_lat, center_lon, max_snap_m=float("inf")
            )
        if center_node is None:
            return None

        start_types = self.road_types_for_node(center_node)

        def edge_weight(_u: int, _v: int, data: Dict[str, Any]) -> float:
            base = float(data.get("weight", 0.0))
            road_type = _normalize_road_type(data.get("road_type"))
            factor = ROAD_TYPE_WEIGHTS.get(road_type or "", 1.0)
            return base * factor

        lengths = nx.single_source_dijkstra_path_length(
            self.graph,
            center_node,
            cutoff=radius_m,
            weight=edge_weight,
        )
        offset_m = float(center_offset or 0.0)
        distances: Dict[str, float] = {}
        points: Dict[str, Dict[str, float]] = {}
        for node_id, dist_m in lengths.items():
            road_types = self.road_types_for_node(node_id)
            if not road_types:
                continue
            total_m = float(dist_m) + offset_m
            for road_type in road_types:
                current = distances.get(road_type)
                if current is None or total_m < current:
                    distances[road_type] = total_m
                    lat_val, lon_val = self.node_coords[int(node_id)]
                    points[road_type] = {
                        "node_id": int(node_id),
                        "lat": float(lat_val),
                        "lon": float(lon_val),
                    }

        return {
            "node_id": int(center_node),
            "snap_distance_m": offset_m,
            "start_types": start_types,
            "distances": distances,
            "points": points,
        }

    @staticmethod
    def _cache_is_valid(cache_path: str, source_path: str) -> bool:
        try:
            return os.path.exists(cache_path) and os.path.getmtime(cache_path) >= os.path.getmtime(source_path)
        except OSError:
            return False

    def _save_cache(self, cache_path: str) -> None:
        data = {
            "schema_version": self._CACHE_SCHEMA_VERSION,
            "graph": self.graph,
            "node_coords": self.node_coords,
        }
        with open(cache_path, "wb") as fh:
            pickle.dump(data, fh)

    @classmethod
    def _load_cache(cls, cache_path: str, snap_tolerance_m: float) -> "RoadTypeNetwork":
        with open(cache_path, "rb") as fh:
            data = pickle.load(fh)
        if data.get("schema_version") != cls._CACHE_SCHEMA_VERSION:
            raise ValueError("Road type network cache schema version mismatch")
        graph = data.get("graph")
        coords = data.get("node_coords")
        if graph is None or coords is None:
            raise ValueError("Invalid road type network cache contents")
        if not isinstance(coords, np.ndarray):
            coords = np.array(coords, dtype=np.float64)
        return cls(graph, coords, snap_tolerance_m)

    def _build_tree(self):
        if self.node_count == 0 or cKDTree is None:
            return None
        return cKDTree(self.node_coords)

    def _nearest_node_index(self, lat: float, lon: float) -> Optional[int]:
        if self.node_count == 0:
            return None
        if self._tree is not None:
            _, idx = self._tree.query([lat, lon], k=1)
            return int(idx)
        diffs = self.node_coords - np.array([lat, lon], dtype=np.float64)
        sq = np.sum(diffs * diffs, axis=1)
        return int(np.argmin(sq))

    @staticmethod
    def _build_graph_from_geojson(path: str) -> Tuple[nx.Graph, np.ndarray]:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Roadway GeoJSON not found at {path}")
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        features = data.get("features", [])
        graph = nx.Graph()
        node_lookup: Dict[Tuple[float, float], int] = {}
        node_coords: List[Tuple[float, float]] = []
        for feature in features:
            geom = feature.get("geometry")
            props = feature.get("properties") or {}
            if geom is None or not geom.get("coordinates"):
                continue
            road_type = props.get("highway") or props.get("area:highway")
            road_type = _normalize_road_type(road_type)
            if not road_type:
                continue
            for coord_sequence in RoadTypeNetwork._iter_lines(geom):
                RoadTypeNetwork._add_line_to_graph(coord_sequence, graph, node_lookup, node_coords, road_type)
        if not node_coords:
            coords_array = np.zeros((0, 2), dtype=np.float64)
        else:
            coords_array = np.array(node_coords, dtype=np.float64)
        return graph, coords_array

    @staticmethod
    def _iter_lines(geometry: Dict[str, Any]) -> Iterable[List[List[float]]]:
        gtype = geometry.get("type")
        coords = geometry.get("coordinates")
        if not coords:
            return
        if gtype == "LineString":
            yield coords
        elif gtype == "MultiLineString":
            for line in coords:
                yield line
        elif gtype == "Polygon":
            for ring in coords:
                yield ring
        elif gtype == "MultiPolygon":
            for poly in coords:
                for ring in poly:
                    yield ring

    @staticmethod
    def _add_line_to_graph(
        coords: List[Sequence[float]],
        graph: nx.Graph,
        node_lookup: Dict[Tuple[float, float], int],
        node_coords: List[Tuple[float, float]],
        road_type: str,
    ) -> None:
        prev_node: Optional[int] = None
        for coord in coords:
            if len(coord) < 2:
                continue
            lon, lat = coord[0], coord[1]
            if lon is None or lat is None:
                continue
            try:
                lat_val = float(lat)
                lon_val = float(lon)
            except (TypeError, ValueError):
                continue
            node_id = RoadTypeNetwork._get_or_create_node(lat_val, lon_val, graph, node_lookup, node_coords)
            node_data = graph.nodes[node_id]
            node_data.setdefault("road_types", set()).add(road_type)
            if prev_node is not None and node_id != prev_node:
                prev_lat, prev_lon = node_coords[prev_node]
                dist = _haversine_pair(prev_lat, prev_lon, lat_val, lon_val)
                if dist < 0.5:
                    prev_node = node_id
                    continue
                existing = graph.get_edge_data(prev_node, node_id)
                if existing is None or dist < existing.get("weight", float("inf")):
                    graph.add_edge(prev_node, node_id, weight=float(dist), road_type=road_type)
            prev_node = node_id

    @staticmethod
    def _get_or_create_node(
        lat: float,
        lon: float,
        graph: nx.Graph,
        node_lookup: Dict[Tuple[float, float], int],
        node_coords: List[Tuple[float, float]],
    ) -> int:
        key = (round(lat, 6), round(lon, 6))
        node_id = node_lookup.get(key)
        if node_id is not None:
            return node_id
        node_id = len(node_coords)
        node_lookup[key] = node_id
        node_coords.append((lat, lon))
        graph.add_node(node_id)
        return node_id
