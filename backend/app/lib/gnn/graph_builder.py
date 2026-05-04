"""
graph_builder.py — Build a heterogeneous graph for the SiteX GNN.

Produces a GraphData object containing:

  Node types
  ----------
  junction   : OSMnx road intersections
  cafe       : each row from cafes_df (matched to a junction via snap_point)
  poi        : all POI rows concatenated from all categories

  Edge types
  ----------
  (junction, road,          junction)  — road segments from OSMnx
  (cafe,     located_at,   junction)  — cafe snapped to nearest junction
  (poi,      near,          junction)  — POI snapped to nearest junction
  (cafe,     competes_with, cafe)      — cafe pairs within competition_radius_m

Usage
-----
    from app.lib.gnn.graph_builder import SiteXGraphBuilder
    import pandas as pd

    cafes_df  = pd.read_csv("Data/CSV_Reference/master_cafes_metrics.csv")
    poi_dfs   = {
        "banks":     pd.read_csv("Data/CSV_Reference/banks.csv"),
        "education": pd.read_csv("Data/CSV_Reference/education.csv"),
        "health":    pd.read_csv("Data/CSV_Reference/health.csv"),
        "temples":   pd.read_csv("Data/CSV_Reference/temples.csv"),
        "other":     pd.read_csv("Data/CSV_Reference/other.csv"),
    }

    builder = SiteXGraphBuilder(road_network)
    gdata   = builder.build(cafes_df, poi_dfs)

    # Export to PyTorch Geometric (requires torch + torch_geometric)
    hetero_data = gdata.to_pyg()

    # Or work with plain numpy arrays:
    print(gdata.node_features["junction"].shape)  # (N_junctions, 4)
    print(gdata.edge_index["road"].shape)          # (2, E_road)
"""
from __future__ import annotations

import math
import warnings
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd

from app.lib.road_network import RoadNetwork
from app.lib.gnn.node_features import (
    NodeFeatureMeta,
    POI_CATEGORIES,
    junction_features,
    cafe_features,
    poi_features,
)
from app.lib.gnn.edge_features import (
    road_edge_features,
    located_at_edge_features,
    near_edge_features,
    competes_with_edge_features,
)


# ---------------------------------------------------------------------------
# Return type — plain NumPy graph (no PyG dependency at import time)
# ---------------------------------------------------------------------------

@dataclass
class GraphData:
    """Container for the heterogeneous graph in NumPy format.

    node_features  : dict mapping node_type → float32 array (N, F)
    edge_index     : dict mapping edge_type_str → int64 array (2, E)
                     edge_type_str is 'road', 'located_at', 'near', 'competes_with'
    edge_attr      : dict mapping edge_type_str → float32 array (E, F_e)  [optional]
    node_labels    : dict mapping node_type → float32 array (N,)  [for supervised learning]
    meta           : NodeFeatureMeta with normalisation parameters
    node_id_maps   : original IDs → graph integer index
    """
    node_features: Dict[str, np.ndarray] = field(default_factory=dict)
    edge_index: Dict[str, np.ndarray] = field(default_factory=dict)
    edge_attr: Dict[str, np.ndarray] = field(default_factory=dict)
    node_labels: Dict[str, np.ndarray] = field(default_factory=dict)
    meta: NodeFeatureMeta = field(default_factory=NodeFeatureMeta)
    node_id_maps: Dict[str, Any] = field(default_factory=dict)

    # -----------------------------------------------------------------------
    # Convenience properties
    # -----------------------------------------------------------------------

    @property
    def num_nodes(self) -> Dict[str, int]:
        return {k: v.shape[0] for k, v in self.node_features.items()}

    @property
    def num_edges(self) -> Dict[str, int]:
        return {k: v.shape[1] for k, v in self.edge_index.items()}

    def summary(self) -> str:
        lines = ["=== SiteX Heterogeneous Graph ==="]
        lines.append("Nodes:")
        for ntype, arr in self.node_features.items():
            label_info = ""
            if ntype in self.node_labels:
                label_info = f"  labels={self.node_labels[ntype].shape}"
            lines.append(f"  {ntype:15s}  x={arr.shape}{label_info}")
        lines.append("Edges:")
        for etype, ei in self.edge_index.items():
            attr_info = ""
            if etype in self.edge_attr:
                attr_info = f"  attr={self.edge_attr[etype].shape}"
            lines.append(f"  {etype:20s}  edge_index={ei.shape}{attr_info}")
        return "\n".join(lines)

    # -----------------------------------------------------------------------
    # PyTorch Geometric export
    # -----------------------------------------------------------------------

    def to_pyg(self):
        """Convert to a torch_geometric.data.HeteroData object.

        Requires:  pip install torch torch_geometric
        """
        try:
            import torch
            from torch_geometric.data import HeteroData
        except ImportError as exc:
            raise ImportError(
                "PyTorch Geometric is required for to_pyg(). "
                "Install with:  pip install torch torch_geometric"
            ) from exc

        data = HeteroData()

        # Node features
        for ntype, arr in self.node_features.items():
            data[ntype].x = torch.from_numpy(arr)
        for ntype, arr in self.node_labels.items():
            data[ntype].y = torch.from_numpy(arr)

        # Edge connectivity + attributes
        edge_type_map = {
            "road":          ("junction", "road",          "junction"),
            "located_at":    ("cafe",     "located_at",    "junction"),
            "near":          ("poi",      "near",          "junction"),
            "competes_with": ("cafe",     "competes_with", "cafe"),
        }
        for key, (src, rel, dst) in edge_type_map.items():
            if key in self.edge_index:
                ei = torch.from_numpy(self.edge_index[key]).long()
                data[src, rel, dst].edge_index = ei
            if key in self.edge_attr:
                data[src, rel, dst].edge_attr = torch.from_numpy(self.edge_attr[key])

        return data


# ---------------------------------------------------------------------------
# Builder
# ---------------------------------------------------------------------------

class SiteXGraphBuilder:
    """Builds the SiteX heterogeneous graph from OSMnx + POI data.

    Parameters
    ----------
    road_network : RoadNetwork
        Loaded OSMnx graph (from RoadNetwork.from_osmnx / from_geojson).
    competition_radius_m : float
        Maximum road-network distance between two cafes for a
        'competes_with' edge to be created (default 1 000 m).
    poi_snap_tolerance_m : float
        Maximum distance a POI can be from the road network to be
        included (default 300 m — looser than cafe snapping because
        POIs are often set back from roads).
    cafe_snap_tolerance_m : float
        Maximum snap distance for cafes (default 120 m).
    include_road_edge_attr : bool
        Whether to compute road edge feature vectors (adds compute time).
    """

    def __init__(
        self,
        road_network: RoadNetwork,
        competition_radius_m: float = 1000.0,
        poi_snap_tolerance_m: float = 300.0,
        cafe_snap_tolerance_m: float = 120.0,
        include_road_edge_attr: bool = True,
    ) -> None:
        self.rn = road_network
        self.competition_radius_m = float(competition_radius_m)
        self.poi_snap_tolerance_m = float(poi_snap_tolerance_m)
        self.cafe_snap_tolerance_m = float(cafe_snap_tolerance_m)
        self.include_road_edge_attr = include_road_edge_attr

    # -----------------------------------------------------------------------
    # Public API
    # -----------------------------------------------------------------------

    def build(
        self,
        cafes_df: pd.DataFrame,
        poi_dfs: Dict[str, pd.DataFrame],
        cafe_labels_col: Optional[str] = "poi_composite_score",
    ) -> GraphData:
        """Build and return a GraphData object.

        Parameters
        ----------
        cafes_df : pd.DataFrame
            The master_cafes_metrics.csv (or cafes.csv) dataframe.
        poi_dfs : dict
            Mapping from category name → DataFrame for each POI category.
            Keys should match POI_CATEGORIES: banks, education, health, temples, other.
        cafe_labels_col : str or None
            Column in cafes_df to use as the supervised label for each cafe node.
            Set to None to skip label assignment.
        """
        gdata = GraphData()
        meta = NodeFeatureMeta()

        print("Building SiteX heterogeneous graph...")

        # ── Step 1: Junction nodes ──────────────────────────────────────────
        print("  [1/6] Building junction nodes...")
        junction_node_ids, junction_x = self._build_junctions(meta)
        gdata.node_features["junction"] = junction_x
        # Map OSMnx node IDs → contiguous integer indices
        junction_id_to_idx: Dict[int, int] = {nid: i for i, nid in enumerate(junction_node_ids)}
        gdata.node_id_maps["junction"] = junction_id_to_idx

        # ── Step 2: Road edges ──────────────────────────────────────────────
        print("  [2/6] Building road edges...")
        road_ei, road_attr = self._build_road_edges(junction_id_to_idx)
        gdata.edge_index["road"] = road_ei
        if road_attr is not None:
            gdata.edge_attr["road"] = road_attr

        # ── Step 3: Cafe nodes ──────────────────────────────────────────────
        print("  [3/6] Building cafe nodes...")
        cafe_df_clean, cafe_snap_nodes, cafe_snap_dists = self._snap_cafes(cafes_df)
        cafe_x = cafe_features(cafe_df_clean, np.array(cafe_snap_dists), meta, fit=True)
        gdata.node_features["cafe"] = cafe_x
        gdata.node_id_maps["cafe_df_index"] = list(cafe_df_clean.index)

        # Cafe labels (supervised target)
        if cafe_labels_col and cafe_labels_col in cafe_df_clean.columns:
            labels = pd.to_numeric(cafe_df_clean[cafe_labels_col], errors="coerce").fillna(0).to_numpy(np.float32)
            gdata.node_labels["cafe"] = labels

        # ── Step 4: located_at edges (cafe → junction) ─────────────────────
        print("  [4/6] Building located_at edges (cafe → junction)...")
        located_ei, located_attr = self._build_located_at_edges(
            cafe_snap_nodes, cafe_snap_dists, junction_id_to_idx
        )
        gdata.edge_index["located_at"] = located_ei
        gdata.edge_attr["located_at"] = located_attr

        # ── Step 5: POI nodes + near edges ─────────────────────────────────
        print("  [5/6] Building POI nodes and near edges...")
        poi_x, near_ei, near_attr = self._build_pois(
            poi_dfs, junction_id_to_idx, meta
        )
        gdata.node_features["poi"] = poi_x
        gdata.edge_index["near"] = near_ei
        gdata.edge_attr["near"] = near_attr

        # ── Step 6: competes_with edges (cafe ↔ cafe) ──────────────────────
        print("  [6/6] Building competes_with edges (cafe ↔ cafe)...")
        comp_ei, comp_attr = self._build_competes_with_edges(
            cafe_df_clean, cafe_snap_nodes
        )
        gdata.edge_index["competes_with"] = comp_ei
        gdata.edge_attr["competes_with"] = comp_attr

        gdata.meta = meta
        print("Done.\n" + gdata.summary())
        return gdata

    # -----------------------------------------------------------------------
    # Step 1 — junctions
    # -----------------------------------------------------------------------

    def _build_junctions(
        self, meta: NodeFeatureMeta
    ) -> Tuple[List[int], np.ndarray]:
        node_ids = list(self.rn.graph.nodes())
        x = junction_features(self.rn.graph, node_ids, meta, fit=True)
        return node_ids, x

    # -----------------------------------------------------------------------
    # Step 2 — road edges
    # -----------------------------------------------------------------------

    def _build_road_edges(
        self, junction_id_to_idx: Dict[int, int]
    ) -> Tuple[np.ndarray, Optional[np.ndarray]]:
        src_list: List[int] = []
        dst_list: List[int] = []
        edge_pairs: List[Tuple[int, int]] = []

        for u, v in self.rn.graph.edges():
            u_idx = junction_id_to_idx.get(u)
            v_idx = junction_id_to_idx.get(v)
            if u_idx is None or v_idx is None:
                continue
            src_list.append(u_idx)
            dst_list.append(v_idx)
            edge_pairs.append((u, v))

        if not src_list:
            return np.zeros((2, 0), dtype=np.int64), None

        ei = np.array([src_list, dst_list], dtype=np.int64)

        attr = None
        if self.include_road_edge_attr and edge_pairs:
            attr = road_edge_features(self.rn.graph, edge_pairs)

        return ei, attr

    # -----------------------------------------------------------------------
    # Step 3 — snap cafes to junctions
    # -----------------------------------------------------------------------

    def _snap_cafes(
        self, cafes_df: pd.DataFrame
    ) -> Tuple[pd.DataFrame, List[Optional[int]], List[float]]:
        """Clean cafes DataFrame and snap each to the nearest junction."""
        df = cafes_df.copy().reset_index(drop=True)

        # Detect lat/lon columns
        lat_col = next((c for c in ("lat", "location_lat", "loc_lat") if c in df.columns), None)
        lon_col = next((c for c in ("lng", "loc_lng", "location_lng", "lon") if c in df.columns), None)
        if lat_col is None or lon_col is None:
            raise ValueError("cafes_df has no recognisable lat/lon columns")

        lats = pd.to_numeric(df[lat_col], errors="coerce")
        lons = pd.to_numeric(df[lon_col], errors="coerce")
        valid_mask = lats.notna() & lons.notna() & lats.between(-90, 90) & lons.between(-180, 180)
        df = df[valid_mask].copy()
        lats = lats[valid_mask].to_numpy(np.float64)
        lons = lons[valid_mask].to_numpy(np.float64)

        snap_nodes: List[Optional[int]] = []
        snap_dists: List[float] = []

        # Batch snap using existing snap_points method
        node_ids, offsets = self.rn.snap_points(
            lats.tolist(), lons.tolist(),
            max_snap_m=self.cafe_snap_tolerance_m,
        )
        # Widen tolerance for unsnapped cafes
        unsnapped = [i for i, n in enumerate(node_ids) if n is None]
        if unsnapped:
            wide_nodes, wide_offsets = self.rn.snap_points(
                [lats[i] for i in unsnapped],
                [lons[i] for i in unsnapped],
                max_snap_m=float("inf"),
            )
            for j, i in enumerate(unsnapped):
                if wide_nodes[j] is not None:
                    node_ids[i] = wide_nodes[j]
                    offsets[i] = wide_offsets[j]

        snap_nodes = node_ids
        snap_dists = [o if math.isfinite(o) else self.cafe_snap_tolerance_m for o in offsets]

        print(f"    Cafes: {len(df)} valid rows, "
              f"{sum(1 for n in snap_nodes if n is not None)} snapped to road network")

        return df, snap_nodes, snap_dists

    # -----------------------------------------------------------------------
    # Step 4 — located_at edges
    # -----------------------------------------------------------------------

    def _build_located_at_edges(
        self,
        cafe_snap_nodes: List[Optional[int]],
        cafe_snap_dists: List[float],
        junction_id_to_idx: Dict[int, int],
    ) -> Tuple[np.ndarray, np.ndarray]:
        src_list: List[int] = []   # cafe indices
        dst_list: List[int] = []   # junction indices
        dists: List[float] = []

        for cafe_idx, (node_id, dist) in enumerate(zip(cafe_snap_nodes, cafe_snap_dists)):
            if node_id is None:
                continue
            j_idx = junction_id_to_idx.get(node_id)
            if j_idx is None:
                continue
            src_list.append(cafe_idx)
            dst_list.append(j_idx)
            dists.append(dist)

        if not src_list:
            return np.zeros((2, 0), dtype=np.int64), np.zeros((0, 1), dtype=np.float32)

        ei = np.array([src_list, dst_list], dtype=np.int64)
        attr = located_at_edge_features(np.array(dists), max_snap_m=self.cafe_snap_tolerance_m)
        return ei, attr

    # -----------------------------------------------------------------------
    # Step 5 — POI nodes + near edges
    # -----------------------------------------------------------------------

    def _build_pois(
        self,
        poi_dfs: Dict[str, pd.DataFrame],
        junction_id_to_idx: Dict[int, int],
        meta: NodeFeatureMeta,
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        all_rows: List[pd.DataFrame] = []
        all_labels: List[int] = []
        all_subcats: List[float] = []
        all_snap_nodes: List[Optional[int]] = []
        all_snap_dists: List[float] = []
        all_net_dists: List[float] = []

        for cat_idx, cat in enumerate(POI_CATEGORIES):
            df = poi_dfs.get(cat)
            if df is None or df.empty:
                continue

            lat_col = next((c for c in ("lat", "location_lat", "loc_lat") if c in df.columns), None)
            lon_col = next((c for c in ("lng", "loc_lng", "location_lng", "lon") if c in df.columns), None)
            if lat_col is None or lon_col is None:
                warnings.warn(f"POI category '{cat}' has no lat/lon columns — skipped.")
                continue

            lats = pd.to_numeric(df[lat_col], errors="coerce")
            lons = pd.to_numeric(df[lon_col], errors="coerce")
            valid = lats.notna() & lons.notna() & lats.between(-90, 90) & lons.between(-180, 180)
            df = df[valid].copy().reset_index(drop=True)
            lats = lats[valid].to_numpy(np.float64)
            lons = lons[valid].to_numpy(np.float64)

            # Snap to road network
            node_ids, offsets = self.rn.snap_points(
                lats.tolist(), lons.tolist(),
                max_snap_m=self.poi_snap_tolerance_m,
            )
            # Widen for unsnapped POIs
            unsnapped = [i for i, n in enumerate(node_ids) if n is None]
            if unsnapped:
                wide_n, wide_o = self.rn.snap_points(
                    [lats[i] for i in unsnapped],
                    [lons[i] for i in unsnapped],
                    max_snap_m=float("inf"),
                )
                for j, i in enumerate(unsnapped):
                    if wide_n[j] is not None:
                        node_ids[i] = wide_n[j]
                        offsets[i] = wide_o[j]

            snap_dists = [o if math.isfinite(o) else self.poi_snap_tolerance_m for o in offsets]

            # Network distances (distance from POI junction to itself = snap offset only)
            # More precise: use shortest_paths_from the junction to get true routing dist.
            # For now, use snap_dist as network_dist approximation — graph_builder is stage 1.
            net_dists = snap_dists  # TODO: replace with proper routing if needed

            # subcategory weights
            if "_computed_weight" in df.columns:
                subcat_vals = pd.to_numeric(df["_computed_weight"], errors="coerce").fillna(0.5)
            elif "subcategory_weight" in df.columns:
                subcat_vals = pd.to_numeric(df["subcategory_weight"], errors="coerce").fillna(0.5)
            else:
                subcat_vals = pd.Series([0.5] * len(df))

            all_rows.append(df)
            all_labels.extend([cat_idx] * len(df))
            all_subcats.extend(subcat_vals.tolist())
            all_snap_nodes.extend(node_ids)
            all_snap_dists.extend(snap_dists)
            all_net_dists.extend(net_dists)

            print(f"    POI [{cat:12s}]: {len(df)} rows, "
                  f"{sum(1 for n in node_ids if n is not None)} snapped")

        if not all_rows:
            empty_x = np.zeros((0, meta.poi_dim), dtype=np.float32)
            return empty_x, np.zeros((2, 0), dtype=np.int64), np.zeros((0, 1), dtype=np.float32)

        combined_df = pd.concat(all_rows, ignore_index=True)
        labels_arr = np.array(all_labels, dtype=np.int64)
        subcats_arr = np.array(all_subcats, dtype=np.float32)
        snap_arr = np.array(all_snap_dists, dtype=np.float64)

        # POI node features
        poi_x = poi_features(combined_df, labels_arr, snap_arr, subcats_arr, meta, fit=True)

        # near edges: poi_idx → junction_idx
        src_list: List[int] = []
        dst_list: List[int] = []
        net_dist_list: List[float] = []

        for poi_idx, (node_id, net_d) in enumerate(zip(all_snap_nodes, all_net_dists)):
            if node_id is None:
                continue
            j_idx = junction_id_to_idx.get(node_id)
            if j_idx is None:
                continue
            src_list.append(poi_idx)
            dst_list.append(j_idx)
            net_dist_list.append(net_d)

        if not src_list:
            near_ei = np.zeros((2, 0), dtype=np.int64)
            near_attr = np.zeros((0, 1), dtype=np.float32)
        else:
            near_ei = np.array([src_list, dst_list], dtype=np.int64)
            near_attr = near_edge_features(
                np.array(net_dist_list), max_dist_m=self.poi_snap_tolerance_m
            )

        return poi_x, near_ei, near_attr

    # -----------------------------------------------------------------------
    # Step 6 — competes_with edges
    # -----------------------------------------------------------------------

    def _build_competes_with_edges(
        self,
        cafe_df: pd.DataFrame,
        cafe_snap_nodes: List[Optional[int]],
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Build cafe ↔ cafe competition edges using road-network distance."""
        lat_col = next((c for c in ("lat", "location_lat") if c in cafe_df.columns), None)
        lon_col = next((c for c in ("lng", "loc_lng", "lon") if c in cafe_df.columns), None)
        if lat_col is None or lon_col is None:
            return np.zeros((2, 0), dtype=np.int64), np.zeros((0, 2), dtype=np.float32)

        lats = pd.to_numeric(cafe_df[lat_col], errors="coerce").to_numpy(np.float64)
        lons = pd.to_numeric(cafe_df[lon_col], errors="coerce").to_numpy(np.float64)
        n = len(cafe_df)
        R = 6371000.0

        src_list: List[int] = []
        dst_list: List[int] = []
        hav_dists: List[float] = []
        net_dists: List[float] = []

        # Pre-compute shortest paths from each unique snapped node
        # to avoid redundant Dijkstra runs.
        unique_nodes = list({n for n in cafe_snap_nodes if n is not None})
        paths_cache: Dict[int, Dict[int, float]] = {}
        for node_id in unique_nodes:
            paths_cache[node_id] = self.rn.shortest_paths_from(
                node_id, cutoff=self.competition_radius_m
            )

        for i in range(n):
            if not (math.isfinite(lats[i]) and math.isfinite(lons[i])):
                continue
            node_i = cafe_snap_nodes[i] if i < len(cafe_snap_nodes) else None

            for j in range(i + 1, n):
                if not (math.isfinite(lats[j]) and math.isfinite(lons[j])):
                    continue

                # Quick haversine pre-filter — skip pairs obviously too far
                dlat = math.radians(lats[j] - lats[i])
                dlon = math.radians(lons[j] - lons[i])
                a = (math.sin(dlat / 2) ** 2
                     + math.cos(math.radians(lats[i]))
                     * math.cos(math.radians(lats[j]))
                     * math.sin(dlon / 2) ** 2)
                hav_m = R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

                # Pre-filter: only pursue road-network check if within 2× radius
                if hav_m > self.competition_radius_m * 2.0:
                    continue

                # Road-network distance
                node_j = cafe_snap_nodes[j] if j < len(cafe_snap_nodes) else None
                net_m: Optional[float] = None
                if node_i is not None and node_j is not None:
                    path_lengths = paths_cache.get(node_i, {})
                    if node_j in path_lengths:
                        net_m = path_lengths[node_j]

                if net_m is None:
                    # Fall back to haversine when no network path available
                    net_m = hav_m

                if net_m <= self.competition_radius_m:
                    # Add both directions (undirected competition)
                    src_list.extend([i, j])
                    dst_list.extend([j, i])
                    hav_dists.extend([hav_m, hav_m])
                    net_dists.extend([net_m, net_m])

        if not src_list:
            return np.zeros((2, 0), dtype=np.int64), np.zeros((0, 2), dtype=np.float32)

        ei = np.array([src_list, dst_list], dtype=np.int64)
        attr = competes_with_edge_features(
            np.array(hav_dists), np.array(net_dists),
            max_dist_m=self.competition_radius_m,
        )
        print(f"    competes_with edges: {ei.shape[1]} (bidirectional)")
        return ei, attr
