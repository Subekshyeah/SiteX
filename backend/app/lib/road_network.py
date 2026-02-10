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


def _haversine_pair(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Return haversine distance in meters between two points."""
    R = 6371000.0
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = phi2 - phi1
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2.0) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2.0) ** 2
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return R * c


class RoadNetwork:
    """Light-weight road graph that supports snapping points and shortest-path queries."""

    def __init__(self, graph: nx.Graph, node_coords: np.ndarray, snap_tolerance_m: float = 120.0):
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
    ) -> "RoadNetwork":
        source_path = os.fspath(geojson_path)
        cache_path = os.fspath(cache_path) if cache_path else None
        if cache_path and cls._cache_is_valid(cache_path, source_path):
            return cls._load_cache(cache_path, snap_tolerance_m)
        graph, coords = cls._build_graph_from_geojson(source_path)
        instance = cls(graph, coords, snap_tolerance_m)
        if cache_path:
            instance._save_cache(cache_path)
        return instance

    @property
    def node_count(self) -> int:
        return int(self.node_coords.shape[0])

    @property
    def edge_count(self) -> int:
        return int(self.graph.number_of_edges())

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

    def snap_points(
        self,
        lats: Sequence[float],
        lons: Sequence[float],
        max_snap_m: Optional[float] = None,
    ) -> Tuple[List[Optional[int]], List[float]]:
        nodes: List[Optional[int]] = []
        offsets: List[float] = []
        for lat, lon in zip(lats, lons):
            if lat is None or lon is None:
                nodes.append(None)
                offsets.append(float("inf"))
                continue
            try:
                lat_val = float(lat)
                lon_val = float(lon)
            except (TypeError, ValueError):
                nodes.append(None)
                offsets.append(float("inf"))
                continue
            node_id, offset = self.snap_point(lat_val, lon_val, max_snap_m=max_snap_m)
            nodes.append(node_id)
            offsets.append(float(offset) if offset is not None else float("inf"))
        return nodes, offsets

    def shortest_paths_from(self, node_id: int, cutoff: float) -> Dict[int, float]:
        if node_id not in self.graph:
            return {}
        return nx.single_source_dijkstra_path_length(self.graph, node_id, cutoff=cutoff, weight="weight")

    def distance_between(
        self,
        lat_a: float,
        lon_a: float,
        lat_b: float,
        lon_b: float,
        max_snap_m: Optional[float] = None,
    ) -> Optional[float]:
        source_node, source_offset = self.snap_point(lat_a, lon_a, max_snap_m=max_snap_m)
        target_node, target_offset = self.snap_point(lat_b, lon_b, max_snap_m=max_snap_m)
        if source_node is None or target_node is None:
            return None
        if source_node == target_node:
            return float((source_offset or 0.0) + (target_offset or 0.0))
        try:
            path_len = nx.shortest_path_length(
                self.graph,
                source=source_node,
                target=target_node,
                weight="weight",
            )
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            return None
        return float(path_len + (source_offset or 0.0) + (target_offset or 0.0))

    @staticmethod
    def _cache_is_valid(cache_path: str, source_path: str) -> bool:
        try:
            return os.path.exists(cache_path) and os.path.getmtime(cache_path) >= os.path.getmtime(source_path)
        except OSError:
            return False

    def _save_cache(self, cache_path: str) -> None:
        data = {
            "graph": self.graph,
            "node_coords": self.node_coords,
        }
        with open(cache_path, "wb") as fh:
            pickle.dump(data, fh)

    @classmethod
    def _load_cache(cls, cache_path: str, snap_tolerance_m: float) -> "RoadNetwork":
        with open(cache_path, "rb") as fh:
            data = pickle.load(fh)
        graph = data.get("graph")
        coords = data.get("node_coords")
        if graph is None or coords is None:
            raise ValueError("Invalid road network cache contents")
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
            if not props.get("highway") and not props.get("area:highway"):
                continue
            for coord_sequence in RoadNetwork._iter_lines(geom):
                RoadNetwork._add_line_to_graph(coord_sequence, graph, node_lookup, node_coords)
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
            node_id = RoadNetwork._get_or_create_node(lat_val, lon_val, graph, node_lookup, node_coords)
            if prev_node is not None and node_id != prev_node:
                prev_lat, prev_lon = node_coords[prev_node]
                dist = _haversine_pair(prev_lat, prev_lon, lat_val, lon_val)
                if dist < 0.5:
                    prev_node = node_id
                    continue
                existing = graph.get_edge_data(prev_node, node_id)
                if existing is None or dist < existing.get("weight", float("inf")):
                    graph.add_edge(prev_node, node_id, weight=float(dist))
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
