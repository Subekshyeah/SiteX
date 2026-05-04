"""
edge_features.py — Per-edge feature vector computation for the SiteX GNN.

Four edge types are handled:

  road             ('junction', 'road', 'junction')
    features: [length_norm, is_oneway, speed_norm, <highway one-hot: 10 dims>]

  located_at       ('cafe', 'located_at', 'junction')
    features: [snap_dist_norm]

  near             ('poi', 'near', 'junction')
    features: [network_dist_norm]

  competes_with    ('cafe', 'competes_with', 'cafe')
    features: [haversine_dist_norm, network_dist_norm]
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np


# ---------------------------------------------------------------------------
# Highway type vocabulary — top OSM classes for Kathmandu
# ---------------------------------------------------------------------------

HIGHWAY_TYPES: List[str] = [
    "motorway", "trunk", "primary", "secondary", "tertiary",
    "residential", "unclassified", "service", "footway", "path",
]
HIGHWAY_INDEX: Dict[str, int] = {h: i for i, h in enumerate(HIGHWAY_TYPES)}
N_HIGHWAY = len(HIGHWAY_TYPES)

# Assumed speed limits (km/h) per highway type — used when maxspeed is absent
DEFAULT_SPEED: Dict[str, float] = {
    "motorway": 80.0, "trunk": 60.0, "primary": 50.0,
    "secondary": 40.0, "tertiary": 30.0, "residential": 20.0,
    "unclassified": 20.0, "service": 15.0, "footway": 5.0, "path": 5.0,
}
MAX_SPEED = 80.0   # km/h — for normalisation


def _minmax(arr: np.ndarray, lo: float, hi: float) -> np.ndarray:
    span = hi - lo
    if span < 1e-9:
        return np.zeros_like(arr, dtype=np.float32)
    return np.clip((arr - lo) / span, 0.0, 1.0).astype(np.float32)


def _highway_onehot(highway_val: Any) -> np.ndarray:
    """Return a one-hot vector (length N_HIGHWAY) for a highway tag value.

    OSMnx sometimes stores it as a list when a segment has multiple tags.
    """
    vec = np.zeros(N_HIGHWAY, dtype=np.float32)
    if isinstance(highway_val, (list, tuple)):
        # multi-tagged — activate all matching slots
        for h in highway_val:
            idx = HIGHWAY_INDEX.get(str(h).strip().lower())
            if idx is not None:
                vec[idx] = 1.0
    elif isinstance(highway_val, str):
        idx = HIGHWAY_INDEX.get(highway_val.strip().lower())
        if idx is not None:
            vec[idx] = 1.0
    return vec


# ---------------------------------------------------------------------------
# Road edge features
# ---------------------------------------------------------------------------

def road_edge_features(
    graph,                  # nx.MultiDiGraph from OSMnx
    edge_list: Sequence[Tuple[int, int]],   # list of (u, v) node id pairs
    max_length_m: Optional[float] = None,
) -> np.ndarray:
    """Return float32 array of shape (E_road, 2 + N_HIGHWAY).

    Features per edge:
      [0]   length_norm          (0–1, normalised over dataset)
      [1]   is_oneway            (0 or 1)
      [2]   speed_norm           (0–1, from maxspeed tag or DEFAULT_SPEED)
      [3:]  highway one-hot      (N_HIGHWAY = 10 dims)
    """
    lengths: List[float] = []
    oneways: List[float] = []
    speeds: List[float] = []
    onehots: List[np.ndarray] = []

    for u, v in edge_list:
        # MultiDiGraph: get_edge_data returns dict keyed by edge key (0, 1, …)
        edata = graph.get_edge_data(u, v)
        if edata is None:
            edata = {}
        elif isinstance(edata, dict) and 0 in edata:
            edata = edata[0]

        length = float(edata.get("length", 0.0))
        oneway = float(bool(edata.get("oneway", False)))
        highway = edata.get("highway", "unclassified")
        # Resolve speed
        raw_speed = edata.get("maxspeed")
        if raw_speed is not None:
            try:
                speed = float(str(raw_speed).split()[0])
            except (ValueError, TypeError):
                speed = None
        else:
            speed = None
        if speed is None:
            h_str = highway[0] if isinstance(highway, list) else str(highway)
            speed = DEFAULT_SPEED.get(h_str.strip().lower(), 20.0)

        lengths.append(length)
        oneways.append(oneway)
        speeds.append(speed)
        onehots.append(_highway_onehot(highway))

    lengths_arr = np.array(lengths, dtype=np.float64)
    speeds_arr = np.array(speeds, dtype=np.float64)
    oneways_arr = np.array(oneways, dtype=np.float32)

    if max_length_m is None:
        max_length_m = float(lengths_arr.max()) if lengths_arr.size > 0 else 1000.0

    len_norm = _minmax(lengths_arr, 0.0, max(max_length_m, 1.0))
    spd_norm = _minmax(speeds_arr, 0.0, MAX_SPEED)
    onehot_arr = np.stack(onehots, axis=0) if onehots else np.zeros((0, N_HIGHWAY), dtype=np.float32)

    scalar_part = np.stack([len_norm, oneways_arr, spd_norm], axis=1)
    return np.concatenate([scalar_part, onehot_arr], axis=1)


# ---------------------------------------------------------------------------
# located_at edge features  (cafe → junction)
# ---------------------------------------------------------------------------

def located_at_edge_features(
    snap_distances_m: np.ndarray,
    max_snap_m: float = 120.0,
) -> np.ndarray:
    """Return float32 array of shape (E_located_at, 1).

    Single feature: normalised snap distance from cafe to its nearest junction.
    """
    snap = np.asarray(snap_distances_m, dtype=np.float64)
    norm = _minmax(np.nan_to_num(snap, nan=max_snap_m), 0.0, max(max_snap_m, 1.0))
    return norm.reshape(-1, 1)


# ---------------------------------------------------------------------------
# near edge features  (poi → junction)
# ---------------------------------------------------------------------------

def near_edge_features(
    network_distances_m: np.ndarray,
    max_dist_m: float = 1500.0,
) -> np.ndarray:
    """Return float32 array of shape (E_near, 1).

    Single feature: normalised road-network distance from POI to its junction.
    """
    dists = np.asarray(network_distances_m, dtype=np.float64)
    norm = _minmax(np.nan_to_num(dists, nan=max_dist_m), 0.0, max(max_dist_m, 1.0))
    return norm.reshape(-1, 1)


# ---------------------------------------------------------------------------
# competes_with edge features  (cafe → cafe)
# ---------------------------------------------------------------------------

def competes_with_edge_features(
    haversine_distances_m: np.ndarray,
    network_distances_m: np.ndarray,
    max_dist_m: float = 1500.0,
) -> np.ndarray:
    """Return float32 array of shape (E_competes, 2).

    Features: [haversine_dist_norm, network_dist_norm]
    The two distances together signal how much spatial vs road-network
    separation exists between competing cafes.
    """
    hav = np.asarray(haversine_distances_m, dtype=np.float64)
    net = np.asarray(network_distances_m, dtype=np.float64)
    cap = max(max_dist_m, 1.0)
    hav_norm = _minmax(np.nan_to_num(hav, nan=cap), 0.0, cap)
    net_norm = _minmax(np.nan_to_num(net, nan=cap), 0.0, cap)
    return np.stack([hav_norm, net_norm], axis=1)
