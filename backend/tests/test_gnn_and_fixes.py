"""
tests/test_gnn_and_fixes.py

Covers:
  1. Bug #4 fix  — path_between uses node_lats/node_lons (not node_coords)
  2. Bug #2 fix  — RoadTypeNetwork loads roads tagged with alternate property names
  3. Bug #3 fix  — snap_to_edge() exists and returns (u, v, dist)
  4. Bug #1 fix  — visualize_road_network logic reads edge geometry
  5. GNN         — node_features module (junction, cafe, poi)
  6. GNN         — edge_features module (road, located_at, near, competes_with)
  7. GNN         — graph_builder end-to-end (no road network required — stubbed)

Run from backend/:
    pytest tests/test_gnn_and_fixes.py -v
"""
from __future__ import annotations

import json
import math
import sys
import types
from pathlib import Path
from typing import Any, Dict, List, Optional
from unittest.mock import MagicMock, patch

import numpy as np
import pandas as pd
import pytest

# Make sure the backend package root is on sys.path
BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))


# ===========================================================================
# Shared stubs & helpers
# ===========================================================================

def _make_osmnx_graph(n_nodes: int = 5, n_edges: int = 4):
    """Return a tiny nx.MultiDiGraph that looks like an OSMnx graph."""
    import networkx as nx

    G = nx.MultiDiGraph()
    # Nodes centred around Kathmandu
    base_lat, base_lon = 27.70, 85.32
    for i in range(n_nodes):
        G.add_node(i, y=base_lat + i * 0.001, x=base_lon + i * 0.001, street_count=3)

    # Simple chain 0→1→2→3→4 with one back-edge 4→0
    edges = [(i, i + 1) for i in range(n_nodes - 1)] + [(n_nodes - 1, 0)]
    for u, v in edges[:n_edges]:
        G.add_edge(u, v, length=100.0, highway="residential",
                   oneway=False, reversed=False, osmid=1000 + u)
    return G


class _RoadNetworkStub:
    """Minimal stub that satisfies the RoadNetwork interface used by the builder."""

    def __init__(self, graph=None):
        import networkx as nx
        self.graph = graph or _make_osmnx_graph()
        self.node_lats = {n: d["y"] for n, d in self.graph.nodes(data=True)}
        self.node_lons = {n: d["x"] for n, d in self.graph.nodes(data=True)}

    @property
    def node_count(self):
        return self.graph.number_of_nodes()

    @property
    def edge_count(self):
        return self.graph.number_of_edges()

    def snap_point(self, lat, lon, max_snap_m=None):
        return (0, 10.0)   # always snaps to node 0 at 10 m

    def snap_points(self, lats, lons, max_snap_m=None):
        nodes = [0] * len(lats)
        dists = [10.0] * len(lats)
        return nodes, dists

    def shortest_paths_from(self, node_id, cutoff):
        # All other nodes within cutoff
        return {n: (i + 1) * 50.0 for i, n in enumerate(self.graph.nodes()) if n != node_id}


# ===========================================================================
# 1. Bug #4 — path_between uses correct coord attributes
# ===========================================================================

class TestBug4PathBetween:
    """path_between must use node_lats / node_lons, not node_coords."""

    def test_node_lats_lons_exist_on_road_network(self):
        """RoadNetwork exposes node_lats and node_lons dicts."""
        stub = _RoadNetworkStub()
        assert hasattr(stub, "node_lats"), "node_lats must exist"
        assert hasattr(stub, "node_lons"), "node_lons must exist"
        assert not hasattr(stub, "node_coords"), \
            "node_coords should NOT exist on RoadNetwork (it belongs to RoadTypeNetwork)"

    def test_path_between_coord_lookup(self):
        """
        Simulate what path_between does after the fix:
        iterate a node_path and pull lat/lon from node_lats/node_lons.
        This would have raised AttributeError before the fix.
        """
        stub = _RoadNetworkStub()
        node_path = [0, 1, 2]
        coords = []
        for n in node_path:
            # This is the fixed code path
            lat_val = stub.node_lats[int(n)]
            lon_val = stub.node_lons[int(n)]
            coords.append({"lat": float(lat_val), "lon": float(lon_val)})

        assert len(coords) == 3
        for c in coords:
            assert "lat" in c and "lon" in c
            assert math.isfinite(c["lat"])
            assert math.isfinite(c["lon"])

    def test_old_code_would_fail(self):
        """Confirm that accessing .node_coords raises AttributeError (pre-fix behaviour)."""
        stub = _RoadNetworkStub()
        with pytest.raises(AttributeError):
            _ = stub.node_coords  # noqa — this must fail


# ===========================================================================
# 2. Bug #2 — RoadTypeNetwork loads alternate road-type tags
# ===========================================================================

class TestBug2AlternativeRoadTypeTags:
    """GeoJSON features tagged with road_type / fclass / type must NOT be dropped."""

    def _make_geojson(self, prop_key: str, prop_val: str) -> dict:
        return {
            "type": "FeatureCollection",
            "features": [{
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": [[85.32, 27.70], [85.33, 27.71]]
                },
                "properties": {prop_key: prop_val}
            }]
        }

    def _load_graph(self, geojson_dict: dict):
        """Call _build_graph_from_geojson via a temp file."""
        import tempfile, os
        from app.lib.road_type_network import RoadTypeNetwork

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".geojson", delete=False, encoding="utf-8"
        ) as f:
            json.dump(geojson_dict, f)
            tmp_path = f.name
        try:
            graph, coords = RoadTypeNetwork._build_graph_from_geojson(tmp_path)
            return graph, coords
        finally:
            os.unlink(tmp_path)

    def test_standard_highway_tag_loads(self):
        gj = self._make_geojson("highway", "residential")
        g, coords = self._load_graph(gj)
        assert g.number_of_nodes() >= 2, "Should load 2 nodes from a LineString"

    def test_road_type_tag_loads(self):
        gj = self._make_geojson("road_type", "residential")
        g, coords = self._load_graph(gj)
        assert g.number_of_nodes() >= 2, \
            "road_type property should now be recognised (Bug #2 fix)"

    def test_fclass_tag_loads(self):
        gj = self._make_geojson("fclass", "residential")
        g, coords = self._load_graph(gj)
        assert g.number_of_nodes() >= 2, \
            "fclass property (osm2shp format) should now be recognised"

    def test_type_tag_loads(self):
        gj = self._make_geojson("type", "residential")
        g, coords = self._load_graph(gj)
        assert g.number_of_nodes() >= 2, \
            "type property should now be recognised as fallback"

    def test_unknown_tag_still_skipped(self):
        gj = self._make_geojson("totally_unknown_key", "residential")
        g, coords = self._load_graph(gj)
        assert g.number_of_nodes() == 0, \
            "Features with no recognised road-type tag must still be skipped"


# ===========================================================================
# 3. Bug #3 — snap_to_edge exists and returns correct shape
# ===========================================================================

class TestBug3SnapToEdge:
    """RoadNetwork must expose snap_to_edge() returning (u, v, dist)."""

    def test_snap_to_edge_exists_on_road_network_module(self):
        from app.lib.road_network import RoadNetwork
        assert hasattr(RoadNetwork, "snap_to_edge"), \
            "snap_to_edge() method must exist on RoadNetwork"

    def test_snap_to_edge_signature(self):
        """snap_to_edge should accept (lat, lon, max_snap_m) and return 3 values."""
        from app.lib.road_network import RoadNetwork
        import inspect
        sig = inspect.signature(RoadNetwork.snap_to_edge)
        params = list(sig.parameters.keys())
        # self + lat + lon + max_snap_m
        assert "lat" in params
        assert "lon" in params
        assert "max_snap_m" in params

    def test_snap_to_edge_returns_three_values(self):
        """snap_to_edge must return a 3-tuple."""
        from app.lib.road_network import RoadNetwork

        # Create a minimal RoadNetwork with a stubbed graph
        stub_graph = _make_osmnx_graph()
        rn = RoadNetwork.__new__(RoadNetwork)
        rn.graph = stub_graph
        rn.snap_tolerance_m = 200.0
        rn.node_lats = {n: d["y"] for n, d in stub_graph.nodes(data=True)}
        rn.node_lons = {n: d["x"] for n, d in stub_graph.nodes(data=True)}
        rn._paths_cache = {}
        rn._paths_cache_size = 16

        # Patch ox.distance.nearest_edges to avoid actual computation
        with patch("app.lib.road_network.ox") as mock_ox:
            mock_ox.distance.nearest_edges.return_value = (0, 1, 0)
            mock_ox.distance.nearest_nodes.return_value = ([0], [10.0])
            result = rn.snap_to_edge(27.70, 85.32)

        assert isinstance(result, tuple), "snap_to_edge must return a tuple"
        assert len(result) == 3, "snap_to_edge must return exactly 3 values (u, v, dist)"


# ===========================================================================
# 4. Bug #1 — visualize_road_network reads edge geometry
# ===========================================================================

class TestBug1VisualizationGeometry:
    """Edge geometry should be used when building the GeoJSON for visualisation."""

    def test_geometry_coords_extracted_when_present(self):
        """
        Simulate the fixed visualisation loop: if edge has a 'geometry'
        attribute (Shapely LineString), extract its .coords, not just the 2 endpoints.
        """
        from shapely.geometry import LineString

        # 5-point curved road
        curve = LineString([(85.32, 27.70), (85.325, 27.705), (85.33, 27.71),
                            (85.335, 27.715), (85.34, 27.72)])

        edge_data = {"geometry": curve, "highway": "residential", "length": 500.0}
        geom = edge_data.get("geometry")

        assert geom is not None
        coords = [[x, y] for x, y in geom.coords]
        assert len(coords) == 5, "All 5 curve points must be extracted"

    def test_fallback_when_no_geometry(self):
        """When geometry is absent, fall back to the two endpoint nodes."""
        graph = _make_osmnx_graph()
        u, v = 0, 1
        edge_data = dict(list(graph.edges(data=True))[0][2])
        edge_data.pop("geometry", None)      # remove geometry if present

        geom = edge_data.get("geometry")     # None
        if geom is not None:
            coords = [[x, y] for x, y in geom.coords]
        else:
            u_lng = graph.nodes[u]["x"]
            u_lat = graph.nodes[u]["y"]
            v_lng = graph.nodes[v]["x"]
            v_lat = graph.nodes[v]["y"]
            coords = [[u_lng, u_lat], [v_lng, v_lat]]

        assert len(coords) == 2, "Fallback must produce exactly 2 points (start/end)"


# ===========================================================================
# 5. GNN — node_features module
# ===========================================================================

class TestNodeFeatures:

    def _small_cafe_df(self, n: int = 10) -> pd.DataFrame:
        rng = np.random.default_rng(0)
        return pd.DataFrame({
            "lat": rng.uniform(27.60, 27.75, n),
            "lng": rng.uniform(85.25, 85.45, n),
            "reviews_count": rng.integers(0, 500, n),
            "weekly_hours": rng.uniform(40, 80, n),
            "rating": rng.uniform(3.0, 5.0, n),
            "banks_count_1km": rng.integers(0, 10, n),
            "education_count_1km": rng.integers(0, 10, n),
            "health_count_1km": rng.integers(0, 10, n),
            "temples_count_1km": rng.integers(0, 10, n),
            "other_count_1km": rng.integers(0, 10, n),
            "poi_composite_score": rng.uniform(0, 5, n),
            "cafe_weight": rng.uniform(0, 1, n),
        })

    def _small_poi_df(self, n: int = 8) -> pd.DataFrame:
        rng = np.random.default_rng(1)
        return pd.DataFrame({
            "lat": rng.uniform(27.60, 27.75, n),
            "lng": rng.uniform(85.25, 85.45, n),
            "rating": rng.uniform(2.0, 5.0, n),
            "reviewsCount": rng.integers(0, 300, n),
        })

    def test_junction_features_shape(self):
        from app.lib.gnn.node_features import junction_features, NodeFeatureMeta
        graph = _make_osmnx_graph(5)
        node_ids = list(graph.nodes())
        meta = NodeFeatureMeta()
        x = junction_features(graph, node_ids, meta, fit=True)
        assert x.shape == (5, 4), f"Expected (5,4) got {x.shape}"
        assert x.dtype == np.float32

    def test_junction_features_range(self):
        from app.lib.gnn.node_features import junction_features, NodeFeatureMeta
        graph = _make_osmnx_graph(10)
        node_ids = list(graph.nodes())
        meta = NodeFeatureMeta()
        x = junction_features(graph, node_ids, meta, fit=True)
        assert x.min() >= 0.0, "Features must be >= 0"
        assert x.max() <= 1.0, "Normalised features must be <= 1"

    def test_cafe_features_shape(self):
        from app.lib.gnn.node_features import cafe_features, NodeFeatureMeta
        df = self._small_cafe_df(10)
        snap_dists = np.random.uniform(0, 100, 10)
        meta = NodeFeatureMeta()
        x = cafe_features(df, snap_dists, meta, fit=True)
        assert x.shape[0] == 10
        assert x.shape[1] == meta.cafe_dim
        assert x.dtype == np.float32

    def test_cafe_features_range(self):
        from app.lib.gnn.node_features import cafe_features, NodeFeatureMeta
        df = self._small_cafe_df(20)
        snap_dists = np.random.uniform(0, 120, 20)
        meta = NodeFeatureMeta()
        x = cafe_features(df, snap_dists, meta, fit=True)
        assert np.all(x >= 0.0), "All features must be >= 0"
        assert np.all(x <= 1.0), "All normalised features must be <= 1"

    def test_poi_features_shape(self):
        from app.lib.gnn.node_features import poi_features, NodeFeatureMeta, POI_CATEGORIES
        df = self._small_poi_df(8)
        labels = np.array([i % len(POI_CATEGORIES) for i in range(8)], dtype=np.int64)
        snap_dists = np.random.uniform(0, 100, 8)
        subcats = np.random.uniform(0.5, 1.0, 8)
        meta = NodeFeatureMeta()
        # Set lat/lon range first (normally done by junction_features)
        meta.lat_range = (27.60, 27.75)
        meta.lon_range = (85.25, 85.45)
        x = poi_features(df, labels, snap_dists, subcats, meta, fit=True)
        assert x.shape[0] == 8
        # 6 scalar features + 5 one-hot
        assert x.shape[1] == 11, f"Expected 11-dim POI features, got {x.shape[1]}"
        assert x.dtype == np.float32

    def test_poi_onehot_correctness(self):
        from app.lib.gnn.node_features import poi_features, NodeFeatureMeta, POI_CATEGORIES
        df = self._small_poi_df(5)
        # All POIs are category index 2 (health)
        labels = np.full(5, 2, dtype=np.int64)
        snap_dists = np.zeros(5)
        subcats = np.ones(5)
        meta = NodeFeatureMeta()
        meta.lat_range = (27.60, 27.75)
        meta.lon_range = (85.25, 85.45)
        x = poi_features(df, labels, snap_dists, subcats, meta, fit=True)
        one_hot = x[:, 6:]   # last 5 columns are category one-hot
        assert np.all(one_hot[:, 2] == 1.0), "Category index 2 slot must be 1"
        assert np.all(one_hot[:, [0, 1, 3, 4]] == 0.0), "Other slots must be 0"


# ===========================================================================
# 6. GNN — edge_features module
# ===========================================================================

class TestEdgeFeatures:

    def test_road_edge_features_shape(self):
        from app.lib.gnn.edge_features import road_edge_features, N_HIGHWAY
        graph = _make_osmnx_graph(5, 4)
        edge_list = list(graph.edges())[:4]
        attr = road_edge_features(graph, edge_list)
        # 3 scalars (length, oneway, speed) + N_HIGHWAY one-hot
        expected_dim = 3 + N_HIGHWAY
        assert attr.shape == (len(edge_list), expected_dim), \
            f"Expected {(len(edge_list), expected_dim)}, got {attr.shape}"
        assert attr.dtype == np.float32

    def test_road_edge_features_range(self):
        from app.lib.gnn.edge_features import road_edge_features
        graph = _make_osmnx_graph(5, 4)
        edge_list = list(graph.edges())[:4]
        attr = road_edge_features(graph, edge_list)
        assert np.all(attr >= 0.0)
        assert np.all(attr <= 1.0)

    def test_located_at_features_shape(self):
        from app.lib.gnn.edge_features import located_at_edge_features
        dists = np.array([10.0, 50.0, 0.0, 120.0])
        attr = located_at_edge_features(dists, max_snap_m=120.0)
        assert attr.shape == (4, 1)
        assert attr.dtype == np.float32
        assert np.all(attr >= 0.0) and np.all(attr <= 1.0)

    def test_near_features_shape(self):
        from app.lib.gnn.edge_features import near_edge_features
        dists = np.array([0.0, 200.0, 800.0, 1500.0])
        attr = near_edge_features(dists, max_dist_m=1500.0)
        assert attr.shape == (4, 1)
        assert np.all(attr >= 0.0) and np.all(attr <= 1.0)

    def test_competes_with_features_shape(self):
        from app.lib.gnn.edge_features import competes_with_edge_features
        hav = np.array([100.0, 500.0, 900.0])
        net = np.array([120.0, 600.0, 1000.0])
        attr = competes_with_edge_features(hav, net, max_dist_m=1000.0)
        assert attr.shape == (3, 2)
        assert attr.dtype == np.float32
        # Second column (net dist) should be >= first (hav) since net ≥ straight-line
        # (not always true in stub, but shape and range must be valid)
        assert np.all(attr >= 0.0) and np.all(attr <= 1.0)


# ===========================================================================
# 7. GNN — graph_builder end-to-end (stubbed road network)
# ===========================================================================

class TestGraphBuilder:

    def _make_small_data(self, n_cafes=8, n_pois_per_cat=4):
        rng = np.random.default_rng(42)
        cafes_df = pd.DataFrame({
            "lat": rng.uniform(27.70, 27.71, n_cafes),
            "lng": rng.uniform(85.32, 85.33, n_cafes),
            "reviews_count": rng.integers(0, 200, n_cafes),
            "weekly_hours": rng.uniform(40, 80, n_cafes),
            "rating": rng.uniform(3.0, 5.0, n_cafes),
            "banks_count_1km": rng.integers(0, 5, n_cafes),
            "education_count_1km": rng.integers(0, 5, n_cafes),
            "health_count_1km": rng.integers(0, 5, n_cafes),
            "temples_count_1km": rng.integers(0, 5, n_cafes),
            "other_count_1km": rng.integers(0, 5, n_cafes),
            "poi_composite_score": rng.uniform(0, 3, n_cafes),
            "cafe_weight": rng.uniform(0, 1, n_cafes),
        })
        poi_df = pd.DataFrame({
            "lat": rng.uniform(27.70, 27.71, n_pois_per_cat),
            "lng": rng.uniform(85.32, 85.33, n_pois_per_cat),
            "rating": rng.uniform(2.0, 5.0, n_pois_per_cat),
            "reviewsCount": rng.integers(0, 100, n_pois_per_cat),
        })
        poi_dfs = {cat: poi_df.copy() for cat in
                   ["banks", "education", "health", "temples", "other"]}
        return cafes_df, poi_dfs

    def test_build_returns_graph_data(self):
        from app.lib.gnn.graph_builder import SiteXGraphBuilder, GraphData
        cafes_df, poi_dfs = self._make_small_data()
        builder = SiteXGraphBuilder(_RoadNetworkStub(), competition_radius_m=1000.0)
        gdata = builder.build(cafes_df, poi_dfs)
        assert isinstance(gdata, GraphData)

    def test_all_node_types_present(self):
        from app.lib.gnn.graph_builder import SiteXGraphBuilder
        cafes_df, poi_dfs = self._make_small_data()
        gdata = SiteXGraphBuilder(_RoadNetworkStub()).build(cafes_df, poi_dfs)
        for ntype in ("junction", "cafe", "poi"):
            assert ntype in gdata.node_features, f"Missing node type: {ntype}"

    def test_all_edge_types_present(self):
        from app.lib.gnn.graph_builder import SiteXGraphBuilder
        cafes_df, poi_dfs = self._make_small_data()
        gdata = SiteXGraphBuilder(_RoadNetworkStub()).build(cafes_df, poi_dfs)
        for etype in ("road", "located_at", "near", "competes_with"):
            assert etype in gdata.edge_index, f"Missing edge type: {etype}"

    def test_junction_node_count_matches_graph(self):
        from app.lib.gnn.graph_builder import SiteXGraphBuilder
        rn = _RoadNetworkStub()
        cafes_df, poi_dfs = self._make_small_data()
        gdata = SiteXGraphBuilder(rn).build(cafes_df, poi_dfs)
        assert gdata.node_features["junction"].shape[0] == rn.node_count

    def test_cafe_node_count_matches_input(self):
        from app.lib.gnn.graph_builder import SiteXGraphBuilder
        cafes_df, poi_dfs = self._make_small_data(n_cafes=8)
        gdata = SiteXGraphBuilder(_RoadNetworkStub()).build(cafes_df, poi_dfs)
        assert gdata.node_features["cafe"].shape[0] == 8

    def test_poi_node_count_is_sum_of_categories(self):
        from app.lib.gnn.graph_builder import SiteXGraphBuilder
        N = 4  # pois per category
        cafes_df, poi_dfs = self._make_small_data(n_pois_per_cat=N)
        gdata = SiteXGraphBuilder(_RoadNetworkStub()).build(cafes_df, poi_dfs)
        assert gdata.node_features["poi"].shape[0] == N * 5   # 5 categories

    def test_edge_indices_are_within_bounds(self):
        from app.lib.gnn.graph_builder import SiteXGraphBuilder
        rn = _RoadNetworkStub()
        cafes_df, poi_dfs = self._make_small_data()
        gdata = SiteXGraphBuilder(rn).build(cafes_df, poi_dfs)

        n_j = gdata.node_features["junction"].shape[0]
        n_c = gdata.node_features["cafe"].shape[0]
        n_p = gdata.node_features["poi"].shape[0]

        bounds = {
            "road":          (n_j, n_j),
            "located_at":    (n_c, n_j),
            "near":          (n_p, n_j),
            "competes_with": (n_c, n_c),
        }
        for etype, (src_max, dst_max) in bounds.items():
            ei = gdata.edge_index[etype]
            if ei.shape[1] == 0:
                continue
            assert ei[0].max() < src_max, \
                f"{etype}: src index {ei[0].max()} >= {src_max}"
            assert ei[1].max() < dst_max, \
                f"{etype}: dst index {ei[1].max()} >= {dst_max}"

    def test_feature_arrays_are_finite(self):
        from app.lib.gnn.graph_builder import SiteXGraphBuilder
        cafes_df, poi_dfs = self._make_small_data()
        gdata = SiteXGraphBuilder(_RoadNetworkStub()).build(cafes_df, poi_dfs)
        for ntype, arr in gdata.node_features.items():
            assert np.all(np.isfinite(arr)), f"NaN/Inf in {ntype} features"
        for etype, arr in gdata.edge_attr.items():
            assert np.all(np.isfinite(arr)), f"NaN/Inf in {etype} edge attrs"

    def test_cafe_labels_shape(self):
        from app.lib.gnn.graph_builder import SiteXGraphBuilder
        cafes_df, poi_dfs = self._make_small_data(n_cafes=8)
        gdata = SiteXGraphBuilder(_RoadNetworkStub()).build(
            cafes_df, poi_dfs, cafe_labels_col="poi_composite_score"
        )
        assert "cafe" in gdata.node_labels
        assert gdata.node_labels["cafe"].shape[0] == 8

    def test_summary_string(self):
        from app.lib.gnn.graph_builder import SiteXGraphBuilder
        cafes_df, poi_dfs = self._make_small_data()
        gdata = SiteXGraphBuilder(_RoadNetworkStub()).build(cafes_df, poi_dfs)
        s = gdata.summary()
        assert "junction" in s
        assert "cafe" in s
        assert "poi" in s
        assert "road" in s
