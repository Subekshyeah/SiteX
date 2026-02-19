from __future__ import annotations

import csv
import math
import os
import time
from dataclasses import dataclass
from functools import lru_cache
from io import StringIO
from pathlib import Path
from typing import Any, Dict, Iterable, List, Literal, Optional, Sequence, Tuple

import pandas as pd
import networkx as nx

from app.lib.road_network import RoadNetwork


def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def _weight(distance_km: float, radius_km: float, decay_scale_km: float) -> float:
    if radius_km <= 0:
        return 0.0
    try:
        base_weight = max(0.0, 1.0 - (float(distance_km) / float(radius_km)))
    except Exception:
        base_weight = 0.0
    if decay_scale_km <= 0:
        return float(base_weight)
    try:
        return float(base_weight * math.exp(-float(distance_km) / float(decay_scale_km)))
    except Exception:
        return float(base_weight)


@dataclass(frozen=True)
class PoiItem:
    name: str | None
    lat: float
    lon: float
    distance_km: float
    weight: float
    network_distance_km: float | None = None
    subcategory: str | None = None


class SiteAnalysisService:
    """Provides Business-Analyst-like analysis using local CSV POIs and an optional road network graph."""

    POI_FILES: Dict[str, str] = {
        "cafes": "cafe_final.csv",
        "banks": "banks_final.csv",
        "education": "education_final.csv",
        "health": "health_final.csv",
        "temples": "temples_final.csv",
        "other": "other_final.csv",
    }

    def __init__(
        self,
        data_root: Optional[Path] = None,
        road_snap_tolerance_m: float = 120.0,
        secondary_snap_tolerance_m: float = 300.0,
    ) -> None:
        self.data_root = data_root or Path(__file__).resolve().parents[2]
        self.road_geojson = self.data_root / "Data" / "Roadway.geojson"
        self.road_cache = self.road_geojson.with_suffix(".graph.pkl")
        self.road_snap_tolerance_m = float(road_snap_tolerance_m)
        self.secondary_snap_tolerance_m = float(secondary_snap_tolerance_m)

        self._df_cache: Dict[str, Tuple[float, pd.DataFrame]] = {}

    def resolve_poi_data_dir(self) -> Path:
        """Locate the POI CSV directory.

        This repo supports two layouts:
        - backend/Data/CSV_Reference/final/*.csv
        - backend/Data/CSV/*.csv
        """
        env_override = os.getenv("SITEX_POI_DATA_DIR")
        if env_override:
            candidate = Path(env_override).expanduser().resolve()
            if candidate.exists():
                return candidate

        primary = self.data_root / "Data" / "CSV_Reference" / "final"
        if primary.exists():
            return primary

        fallback = self.data_root / "Data" / "CSV"
        if fallback.exists():
            return fallback

        raise RuntimeError(f"POI data folder not found at {primary} or {fallback}")

    @lru_cache(maxsize=1)
    def get_road_network(self) -> Optional[RoadNetwork]:
        if not self.road_geojson.exists():
            return None
        try:
            return RoadNetwork.from_geojson(
                os.fspath(self.road_geojson),
                cache_path=os.fspath(self.road_cache),
                snap_tolerance_m=self.road_snap_tolerance_m,
            )
        except Exception as exc:
            print(f"Warning: Failed to load road network ({exc})")
            return None

    def _find_csv(self, data_dir: Path, expected_name: str) -> Optional[Path]:
        fpath = data_dir / expected_name
        if fpath.exists():
            return fpath
        # attempt fuzzy match (mirrors existing /pois endpoint behavior)
        base = expected_name[:-4].lower()
        for p in data_dir.glob("*.csv"):
            pn = p.name.lower()
            if base in pn or (base.endswith("s") and base[:-1] in pn) or (base.endswith("es") and base[:-2] in pn):
                return p
        return None

    def _normalize_poi_df(self, df: pd.DataFrame) -> pd.DataFrame:
        lat_col: Optional[str] = None
        lon_col: Optional[str] = None
        name_col: Optional[str] = None
        subcat_col: Optional[str] = None

        for c in df.columns:
            cl = str(c).lower()
            if cl in ("lat", "latitude", "y"):
                lat_col = c
            if cl in ("lon", "lng", "longitude", "x"):
                lon_col = c
            if cl in ("name", "title"):
                name_col = c
            if cl in ("subcategory", "sub_category", "type"):
                subcat_col = c

        if lat_col is None or lon_col is None:
            num_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
            if len(num_cols) >= 2:
                lat_col, lon_col = num_cols[0], num_cols[1]

        if lat_col is None or lon_col is None:
            return pd.DataFrame(columns=["lat", "lon", "name", "subcategory"])

        out = pd.DataFrame()
        out["lat"] = pd.to_numeric(df[lat_col], errors="coerce")
        out["lon"] = pd.to_numeric(df[lon_col], errors="coerce")
        out["name"] = df[name_col] if name_col and name_col in df.columns else None
        out["subcategory"] = df[subcat_col] if subcat_col and subcat_col in df.columns else None
        return out

    def load_category_df(self, category: str) -> pd.DataFrame:
        data_dir = self.resolve_poi_data_dir()
        expected = self.POI_FILES.get(category)
        if not expected:
            return pd.DataFrame(columns=["lat", "lon", "name", "subcategory"])
        fpath = self._find_csv(data_dir, expected)
        if fpath is None:
            return pd.DataFrame(columns=["lat", "lon", "name", "subcategory"])

        mtime = 0.0
        try:
            mtime = float(fpath.stat().st_mtime)
        except Exception:
            mtime = time.time()

        cached = self._df_cache.get(os.fspath(fpath))
        if cached and cached[0] >= mtime:
            return cached[1]

        df_raw = pd.read_csv(fpath).reset_index(drop=True)
        df = self._normalize_poi_df(df_raw)
        self._df_cache[os.fspath(fpath)] = (mtime, df)
        return df

    def _network_distance_map(
        self,
        road_net: RoadNetwork,
        center_lat: float,
        center_lon: float,
        poi_indices: Sequence[int],
        poi_lats: pd.Series,
        poi_lons: pd.Series,
        radius_m: float,
    ) -> Dict[int, float]:
        idx_list = [int(i) for i in list(poi_indices)]
        center_node, center_offset = road_net.snap_point(
            center_lat,
            center_lon,
            max_snap_m=self.road_snap_tolerance_m,
        )
        if center_node is None:
            center_node, center_offset = road_net.snap_point(
                center_lat, center_lon, max_snap_m=self.secondary_snap_tolerance_m
            )
        if center_node is None:
            center_node, center_offset = road_net.snap_point(center_lat, center_lon, max_snap_m=float("inf"))
        if center_node is None:
            return {}

        safe_lats: List[Optional[float]] = []
        safe_lons: List[Optional[float]] = []
        for a, b in zip(poi_lats, poi_lons):
            try:
                av = float(a)
                bv = float(b)
                if not math.isfinite(av) or not math.isfinite(bv):
                    safe_lats.append(None)
                    safe_lons.append(None)
                else:
                    safe_lats.append(av)
                    safe_lons.append(bv)
            except Exception:
                safe_lats.append(None)
                safe_lons.append(None)

        poi_nodes, poi_offsets = road_net.snap_points(safe_lats, safe_lons, max_snap_m=self.road_snap_tolerance_m)
        if any(n is None or not math.isfinite(o) for n, o in zip(poi_nodes, poi_offsets)):
            sec_nodes, sec_offsets = road_net.snap_points(
                safe_lats, safe_lons, max_snap_m=self.secondary_snap_tolerance_m
            )
            for i, (n, o) in enumerate(zip(poi_nodes, poi_offsets)):
                if (n is None or not math.isfinite(o)) and (sec_nodes[i] is not None and math.isfinite(sec_offsets[i])):
                    poi_nodes[i] = sec_nodes[i]
                    poi_offsets[i] = sec_offsets[i]
        if any(n is None or not math.isfinite(o) for n, o in zip(poi_nodes, poi_offsets)):
            inf_nodes, inf_offsets = road_net.snap_points(safe_lats, safe_lons, max_snap_m=float("inf"))
            for i, (n, o) in enumerate(zip(poi_nodes, poi_offsets)):
                if (n is None or not math.isfinite(o)) and (inf_nodes[i] is not None and math.isfinite(inf_offsets[i])):
                    poi_nodes[i] = inf_nodes[i]
                    poi_offsets[i] = inf_offsets[i]

        node_to_indices: Dict[int, List[int]] = {}
        for idx, node_id in enumerate(poi_nodes):
            if node_id is None:
                continue
            if not math.isfinite(poi_offsets[idx]):
                continue
            node_to_indices.setdefault(int(node_id), []).append(idx)
        if not node_to_indices:
            return {}

        lengths = road_net.shortest_paths_from(int(center_node), cutoff=float(radius_m))
        if not lengths:
            return {}
        center_offset_val = float(center_offset or 0.0)
        results: Dict[int, float] = {}
        for node_id, path_dist in lengths.items():
            indices = node_to_indices.get(int(node_id))
            if not indices:
                continue
            for poi_idx in indices:
                total_m = float(path_dist) + center_offset_val + float(poi_offsets[poi_idx])
                if total_m <= radius_m:
                    # Map back to the original DataFrame index so callers can look up
                    # by `original_idx` from `df2.iterrows()`.
                    if 0 <= int(poi_idx) < len(idx_list):
                        results[int(idx_list[int(poi_idx)])] = total_m / 1000.0
        return results

    def _resolve_center_node(self, road_net: RoadNetwork, lat: float, lon: float) -> Tuple[Optional[int], float]:
        node, offset = road_net.snap_point(lat, lon, max_snap_m=self.road_snap_tolerance_m)
        if node is None:
            node, offset = road_net.snap_point(lat, lon, max_snap_m=self.secondary_snap_tolerance_m)
        if node is None:
            node, offset = road_net.snap_point(lat, lon, max_snap_m=float("inf"))
        return (int(node) if node is not None else None), float(offset or 0.0)

    def _resolve_poi_node(self, road_net: RoadNetwork, lat: float, lon: float) -> Tuple[Optional[int], float]:
        node, offset = road_net.snap_point(lat, lon, max_snap_m=self.road_snap_tolerance_m)
        if node is None:
            node, offset = road_net.snap_point(lat, lon, max_snap_m=self.secondary_snap_tolerance_m)
        if node is None:
            node, offset = road_net.snap_point(lat, lon, max_snap_m=float("inf"))
        return (int(node) if node is not None else None), float(offset or 0.0)

    def path_between(
        self,
        *,
        center_lat: float,
        center_lon: float,
        poi_lat: float,
        poi_lon: float,
    ) -> Optional[List[Dict[str, float]]]:
        """Return a roadway-following shortest-path polyline between center and a POI.

        Output format matches the existing /pois endpoint: list of {lat, lon}.
        Returns None when the road network is unavailable or no path exists.
        """
        road_net = self.get_road_network()
        if road_net is None:
            return None

        center_node, _ = self._resolve_center_node(road_net, float(center_lat), float(center_lon))
        poi_node, _ = self._resolve_poi_node(road_net, float(poi_lat), float(poi_lon))
        if center_node is None or poi_node is None:
            return None

        try:
            if int(center_node) == int(poi_node):
                node_path = [int(center_node)]
            else:
                node_path = nx.shortest_path(
                    road_net.graph,
                    source=int(center_node),
                    target=int(poi_node),
                    weight="weight",
                )
        except Exception:
            return None

        coords: List[Dict[str, float]] = []
        coords.append({"lat": float(center_lat), "lon": float(center_lon)})
        for n in node_path:
            lat_val, lon_val = road_net.node_coords[int(n)]
            coords.append({"lat": float(lat_val), "lon": float(lon_val)})
        coords.append({"lat": float(poi_lat), "lon": float(poi_lon)})
        return coords

    def nearby(
        self,
        lat: float,
        lon: float,
        *,
        radius_km: float = 1.0,
        limit: int = 10,
        categories: Optional[Sequence[str]] = None,
        decay_scale_km: float = 1.0,
        include_network: bool = True,
        sort_by: Literal["auto", "haversine", "network"] = "auto",
    ) -> Dict[str, List[Dict[str, Any]]]:
        cats = list(categories) if categories else list(self.POI_FILES.keys())
        out: Dict[str, List[Dict[str, Any]]] = {}

        road_net = self.get_road_network() if include_network else None
        max_radius_m = float(radius_km) * 1000.0

        for cat in cats:
            df = self.load_category_df(cat)
            if df.empty:
                continue
            # filter obvious invalids
            df2 = df.dropna(subset=["lat", "lon"]).copy()
            df2 = df2[df2["lat"].map(lambda v: math.isfinite(float(v)) if v is not None else False)]
            df2 = df2[df2["lon"].map(lambda v: math.isfinite(float(v)) if v is not None else False)]
            if df2.empty:
                continue

            # compute haversine for all
            dists = []
            for plat, plon in zip(df2["lat"].tolist(), df2["lon"].tolist()):
                dists.append(_haversine_km(float(lat), float(lon), float(plat), float(plon)))
            df2["_haversine_km"] = dists
            df2 = df2[df2["_haversine_km"] <= float(radius_km)]
            if df2.empty:
                continue

            network_map: Dict[int, float] = {}
            if road_net is not None:
                try:
                    # Important: indices in df2 refer to original indices in df; keep them by using df2.index
                    network_map = self._network_distance_map(
                        road_net,
                        float(lat),
                        float(lon),
                        df2.index.tolist(),
                        df.loc[df2.index, "lat"],
                        df.loc[df2.index, "lon"],
                        max_radius_m,
                    )
                except Exception as exc:
                    print(f"Warning: network distance failed for {cat}: {exc}")
                    network_map = {}

            items: List[Dict[str, Any]] = []
            for original_idx, row in df2.iterrows():
                hav_km = float(row["_haversine_km"])
                net_km = network_map.get(int(original_idx))
                # Network distances can be unavailable for a subset of POIs if the road graph
                # is disconnected or no valid path exists. When include_network=True, we still
                # return a numeric value by falling back to haversine.
                net_km_out: Optional[float]
                if include_network:
                    net_km_out = float(net_km) if net_km is not None else hav_km
                else:
                    net_km_out = None

                if sort_by == "network":
                    chosen_km = float(net_km_out) if net_km_out is not None else hav_km
                elif sort_by == "haversine":
                    chosen_km = hav_km
                else:
                    # auto: prefer network when available
                    chosen_km = float(net_km_out) if net_km_out is not None else hav_km

                weight_val = _weight(chosen_km, float(radius_km), float(decay_scale_km))

                items.append(
                    {
                        "name": row.get("name"),
                        "lat": float(row["lat"]),
                        "lon": float(row["lon"]),
                        "distance_km": round(hav_km, 4),
                        "network_distance_km": round(float(net_km_out), 4) if net_km_out is not None else None,
                        "chosen_distance_km": round(float(chosen_km), 4),
                        "weight": round(float(weight_val), 4),
                        "subcategory": row.get("subcategory"),
                    }
                )

            # sort and limit
            items.sort(key=lambda it: float(it.get("chosen_distance_km") or 1e9))
            out[cat] = items[: max(1, int(limit))]

        return out

    def ring_summary(
        self,
        lat: float,
        lon: float,
        *,
        radii_km: Sequence[float] = (0.25, 0.5, 1.0),
        categories: Optional[Sequence[str]] = None,
        decay_scale_km: float = 1.0,
        include_network: bool = True,
        sort_by: Literal["auto", "haversine", "network"] = "auto",
    ) -> Dict[str, Any]:
        radii = [float(r) for r in radii_km if r and float(r) > 0]
        radii = sorted(set(round(r, 6) for r in radii))
        if not radii:
            radii = [1.0]

        cats = list(categories) if categories else list(self.POI_FILES.keys())
        road_net = self.get_road_network() if include_network else None
        max_radius_km = max(radii)
        max_radius_m = float(max_radius_km) * 1000.0

        # Precompute distances per category at max radius.
        per_cat_points: Dict[str, Dict[str, Any]] = {}
        for cat in cats:
            df = self.load_category_df(cat)
            if df.empty:
                continue
            df2 = df.dropna(subset=["lat", "lon"]).copy()
            if df2.empty:
                continue

            hav = []
            for plat, plon in zip(df2["lat"].tolist(), df2["lon"].tolist()):
                try:
                    hav.append(_haversine_km(float(lat), float(lon), float(plat), float(plon)))
                except Exception:
                    hav.append(float("inf"))
            df2["_haversine_km"] = hav
            df2 = df2[df2["_haversine_km"] <= float(max_radius_km)]
            if df2.empty:
                continue

            net_map: Dict[int, float] = {}
            if road_net is not None:
                try:
                    net_map = self._network_distance_map(
                        road_net,
                        float(lat),
                        float(lon),
                        df2.index.tolist(),
                        df.loc[df2.index, "lat"],
                        df.loc[df2.index, "lon"],
                        max_radius_m,
                    )
                except Exception as exc:
                    print(f"Warning: network distance failed for {cat}: {exc}")
                    net_map = {}

            per_cat_points[cat] = {"df": df2, "net": net_map}

        rings: List[Dict[str, Any]] = []
        for r in radii:
            ring: Dict[str, Any] = {"radius_km": float(r), "categories": {}, "totals": {}}
            total_count = 0
            total_weight = 0.0
            for cat, payload in per_cat_points.items():
                df2 = payload["df"]
                net_map = payload["net"]
                items = []
                for original_idx, row in df2.iterrows():
                    hav_km = float(row["_haversine_km"])
                    net_km = net_map.get(int(original_idx))
                    if sort_by == "network":
                        chosen_km = float(net_km) if net_km is not None else hav_km
                    elif sort_by == "haversine":
                        chosen_km = hav_km
                    else:
                        chosen_km = float(net_km) if net_km is not None else hav_km

                    if chosen_km <= float(r):
                        items.append(chosen_km)
                count = int(len(items))
                if count == 0:
                    continue
                weights = [_weight(d, float(r), float(decay_scale_km)) for d in items]
                sum_w = float(sum(weights))

                ring["categories"][cat] = {
                    "count": count,
                    "sum_weight": round(sum_w, 4),
                    "avg_distance_km": round(float(sum(items)) / float(count), 4),
                    "min_distance_km": round(float(min(items)), 4),
                }
                total_count += count
                total_weight += sum_w

            ring["totals"] = {
                "total_poi_count": int(total_count),
                "total_weight": round(float(total_weight), 4),
            }
            # ratios
            ratios: Dict[str, float] = {}
            if total_count > 0:
                for cat, v in ring["categories"].items():
                    ratios[f"{cat}_share"] = round(float(v["count"]) / float(total_count), 4)
            ring["ratios"] = ratios
            rings.append(ring)

        return {"center": {"lat": float(lat), "lon": float(lon)}, "rings": rings}

    def competition_index(
        self,
        lat: float,
        lon: float,
        *,
        radius_km: float = 1.0,
        decay_scale_km: float = 1.0,
        include_network: bool = True,
        sort_by: Literal["auto", "haversine", "network"] = "auto",
    ) -> Dict[str, Any]:
        summary = self.ring_summary(
            lat,
            lon,
            radii_km=(radius_km,),
            decay_scale_km=decay_scale_km,
            include_network=include_network,
            sort_by=sort_by,
        )
        ring = (summary.get("rings") or [{}])[0]
        cats = ring.get("categories") or {}
        totals = ring.get("totals") or {}
        cafe = cats.get("cafes") or {"count": 0, "sum_weight": 0.0}

        total_count = int(totals.get("total_poi_count") or 0)
        cafes_count = int(cafe.get("count") or 0)
        cafes_weight = float(cafe.get("sum_weight") or 0.0)
        other_count = max(0, total_count - cafes_count)

        share = float(cafes_count) / float(total_count) if total_count else 0.0
        area_sqkm = math.pi * float(radius_km) * float(radius_km)
        density = float(cafes_count) / area_sqkm if area_sqkm > 0 else 0.0

        return {
            "center": {"lat": float(lat), "lon": float(lon)},
            "radius_km": float(radius_km),
            "cafes_count": cafes_count,
            "cafes_sum_weight": round(cafes_weight, 4),
            "total_poi_count": total_count,
            "other_poi_count": other_count,
            "cafe_share": round(float(share), 4),
            "cafes_per_sqkm": round(float(density), 4),
        }

    @staticmethod
    def to_csv(rows: Sequence[Dict[str, Any]], fieldnames: Sequence[str]) -> str:
        buf = StringIO()
        writer = csv.DictWriter(buf, fieldnames=list(fieldnames))
        writer.writeheader()
        for r in rows:
            writer.writerow({k: r.get(k) for k in fieldnames})
        return buf.getvalue()
