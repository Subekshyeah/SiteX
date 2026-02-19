import os
import re
from collections import Counter
from functools import lru_cache
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple, Literal

import joblib
import pandas as pd
import xgboost as xgb

from app.lib.road_type_network import ROAD_TYPE_WEIGHTS, RoadTypeNetwork
from app.services.site_analysis_service import SiteAnalysisService


ROAD_ACCESS_SCORE_FEATURES_0_100 = {
    "road_access_score",
    "road_access_score_0_100",
    "road_accessibility_score",
}
ROAD_ACCESS_SCORE_FEATURES_0_1 = {
    "road_access_score_0_1",
    "road_accessibility",
}
DEFAULT_ROAD_SNAP_WEIGHT_SHARE = 0.9
SCORE_BOOST_START = 1.8
SCORE_MAX_FOR_SHAPING = 3.0
SCORE_CURVE_POWER = 1.35
SCORE_TAIL_BOOST = 0.35
ACCESS_BONUS_THRESHOLD = 0.6
ACCESS_BONUS_SCALE = 0.25

class PredictionService:
    _instance = None
    
    def __init__(self):
        self.model = None
        self.feature_names = None
        self.reference_df = None
        # Paths relative to this file: backend/app/services/prediction_service.py
        self.backend_root = Path(__file__).resolve().parent.parent.parent
        self.model_dir = self.backend_root / "models"
        self.data_dir = self._resolve_data_dir()
        self._load_resources()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def _resolve_data_dir(self) -> Path:
        """Locate the directory containing reference CSV outputs."""
        env_override = os.getenv("SITEX_DATA_DIR")
        if env_override:
            candidate = Path(env_override).expanduser().resolve()
            if (candidate / "master_cafes_minimal.csv").is_file():
                return candidate
            print(
                f"Warning: SITEX_DATA_DIR={candidate} missing master_cafes_minimal.csv; falling back to defaults."
            )

        candidates = [
            self.backend_root / "Data" / "CSV_Reference" / "final",
            self.backend_root / "Data" / "CSV" / "final",
            self.backend_root / "Data" / "CSV_Reference",
            self.backend_root / "Data" / "CSV",
        ]

        for candidate in candidates:
            candidate = candidate.resolve()
            if (candidate / "master_cafes_minimal.csv").is_file():
                return candidate

        print(
            "Warning: Could not locate master_cafes_minimal.csv in default locations. "
            "Continuing with backend/Data/CSV_Reference/final."
        )
        return candidates[0]

    def _load_resources(self):
        # Load Model
        model_path = self.model_dir / "xgb_baseline.pkl"
        if model_path.exists():
            try:
                loaded_obj = joblib.load(model_path)
                
                # Handle case where loaded object is a dictionary containing the model
                if isinstance(loaded_obj, dict):
                    print(f"Loaded object is a dict with keys: {loaded_obj.keys()}")
                    # Try to find the model in common keys
                    if 'model' in loaded_obj:
                        self.model = loaded_obj['model']
                    elif 'regressor' in loaded_obj:
                        self.model = loaded_obj['regressor']
                    elif 'xgb_model' in loaded_obj:
                        self.model = loaded_obj['xgb_model']
                    else:
                        # Fallback: check values for a predict method
                        for key, value in loaded_obj.items():
                            if hasattr(value, 'predict'):
                                self.model = value
                                print(f"Found model in key: {key}")
                                break
                        
                        if self.model is None:
                            print("Error: Could not find model object with 'predict' method in loaded dictionary.")
                            self.model = loaded_obj # Keep it as is, will fail later but we logged the keys
                    
                    # Also try to load features from the dict if available
                    if 'features' in loaded_obj and self.feature_names is None:
                        self.feature_names = loaded_obj['features']
                        print(f"Loaded feature names from pickle dict: {len(self.feature_names)} features")
                else:
                    self.model = loaded_obj
                    
                print(f"Loaded model from {model_path}, type: {type(self.model)}")
            except Exception as e:
                print(f"Error loading model: {e}")
        else:
            print(f"Warning: Model not found at {model_path}")

        # Load Feature Names
        features_path = self.model_dir / "model_features.pkl"
        if features_path.exists():
            try:
                self.feature_names = joblib.load(features_path)
                print(f"Loaded feature names from {features_path}")
            except Exception as e:
                print(f"Error loading feature names: {e}")
        else:
            print(f"Warning: Feature names not found at {features_path}")

        # Load Reference Data for k-NN
        data_path = self.data_dir / "master_cafes_minimal.csv"
        if data_path.exists():
            try:
                self.reference_df = pd.read_csv(data_path)
                # Ensure we have lat/lng
                required_cols = ['lat', 'lng']
                if not all(col in self.reference_df.columns for col in required_cols):
                     print("Warning: Reference data missing lat/lng columns")
                print(f"Loaded reference data from {data_path} with {len(self.reference_df)} rows")
            except Exception as e:
                print(f"Error loading reference data: {e}")
        else:
            print(f"Warning: Reference data not found at {data_path}")

    @staticmethod
    @lru_cache(maxsize=1)
    def _get_road_type_network() -> Optional[RoadTypeNetwork]:
        data_root = Path(__file__).resolve().parents[2]
        road_geojson = data_root / "Data" / "Roadway.geojson"
        road_cache = road_geojson.with_suffix(".roadtypes.pkl")
        if not road_geojson.exists():
            return None
        try:
            return RoadTypeNetwork.from_geojson(
                road_geojson,
                cache_path=road_cache,
                snap_tolerance_m=120.0,
            )
        except Exception:
            return None

    def _compute_road_access_score(
        self,
        lat: float,
        lng: float,
        radius_km: float,
        snap_weight_share: float = DEFAULT_ROAD_SNAP_WEIGHT_SHARE,
    ) -> Optional[Dict[str, Any]]:
        network = self._get_road_type_network()
        if network is None:
            return None

        radius_m = float(radius_km) * 1000.0
        result = network.road_type_distance_map(
            lat,
            lng,
            radius_m,
            secondary_snap_tolerance_m=300.0,
        )
        if result is None:
            return None

        start_types = result.get("start_types") or []
        distances = result.get("distances") or {}

        weights = list(ROAD_TYPE_WEIGHTS.values())
        min_weight = min(weights) if weights else 0.0
        max_weight = max(weights) if weights else 1.0

        def normalize(weight: float) -> float:
            if max_weight <= min_weight:
                return 0.0
            return max(0.0, min(1.0, (weight - min_weight) / (max_weight - min_weight)))

        start_weight = 0.0
        for road_type in start_types:
            start_weight = max(start_weight, float(ROAD_TYPE_WEIGHTS.get(road_type, 1.0)))
        snap_score = normalize(start_weight)

        reachable_scores: List[float] = []
        for road_type, dist_m in distances.items():
            if road_type in start_types:
                continue
            distance_km = float(dist_m) / 1000.0
            normalized_score = max(0.0, 1.0 - (distance_km / float(radius_km)))
            weight = float(ROAD_TYPE_WEIGHTS.get(road_type, 1.0))
            weighted_score = normalize(weight) * normalized_score
            reachable_scores.append(weighted_score)

        reachable_score = (sum(reachable_scores) / len(reachable_scores)) if reachable_scores else 0.0
        share = float(snap_weight_share)
        score_0_1 = (snap_score * share) + (reachable_score * (1.0 - share))
        score_0_100 = max(0.0, min(100.0, score_0_1 * 100.0))

        return {
            "score_0_1": round(score_0_1, 6),
            "score_0_100": round(score_0_100, 6),
            "snap_score": round(snap_score, 6),
            "reachable_score": round(reachable_score, 6),
            "snap_weight_share": share,
            "snap": {
                "node_id": result.get("node_id"),
                "snap_distance_m": result.get("snap_distance_m"),
                "road_types": start_types,
            },
        }

    def _shape_score(self, raw_score: float, access_score_0_1: Optional[float]) -> float:
        score = float(raw_score)
        max_score = float(SCORE_MAX_FOR_SHAPING)
        if max_score > 0:
            norm = max(0.0, min(score / max_score, 1.0))
            base = pow(norm, SCORE_CURVE_POWER)
            tail_start = float(SCORE_BOOST_START) / max_score
            tail = max(0.0, norm - tail_start)
            boosted = min(1.0, base + SCORE_TAIL_BOOST * pow(tail, 0.6))
            score = boosted * max_score

        if access_score_0_1 is not None and access_score_0_1 > ACCESS_BONUS_THRESHOLD:
            bonus = (float(access_score_0_1) - ACCESS_BONUS_THRESHOLD) * ACCESS_BONUS_SCALE * max_score
            score += bonus

        return float(score)

    def _resolve_model_feature_names(self) -> Optional[list[str]]:
        if self.feature_names:
            return list(self.feature_names)
        if self.model is None:
            return None
        # sklearn-style attribute
        feature_names_in = getattr(self.model, "feature_names_in_", None)
        if feature_names_in is not None:
            return list(feature_names_in)
        # xgboost Booster feature names
        if hasattr(self.model, "get_booster"):
            try:
                booster = self.model.get_booster()
                if booster is not None and booster.feature_names:
                    return list(booster.feature_names)
            except Exception:
                pass
        if isinstance(self.model, xgb.Booster) and self.model.feature_names:
            return list(self.model.feature_names)
        return None

    def _extract_poi_feature_specs(self, feature_names: List[str]) -> Tuple[Dict[str, Dict[str, Any]], Optional[str]]:
        pattern = re.compile(r"^(?P<category>.+)_(?P<kind>count|weight)_(?P<dist>\d+(?:\.\d+)?)_km$")
        specs: Dict[str, Dict[str, Any]] = {}
        counts = Counter()
        for name in feature_names:
            match = pattern.match(name)
            if not match:
                continue
            dist_label = match.group("dist")
            try:
                dist_km = float(dist_label)
            except Exception:
                continue
            spec = specs.setdefault(
                dist_label,
                {"distance_km": dist_km, "categories": set(), "kinds": set()},
            )
            spec["categories"].add(match.group("category"))
            spec["kinds"].add(match.group("kind"))
            counts[dist_label] += 1
        primary = counts.most_common(1)[0][0] if counts else None
        return specs, primary

    def _compute_ring_metrics(
        self,
        lat: float,
        lng: float,
        radius_km: float,
        decay_scale_km: Optional[float],
        include_network: bool,
        sort_by: Literal["auto", "haversine", "network"],
    ) -> Dict[str, Any]:
        svc = SiteAnalysisService()
        effective_decay = float(decay_scale_km) if decay_scale_km is not None else float(radius_km)
        summary = svc.ring_summary(
            lat,
            lng,
            radii_km=(float(radius_km),),
            categories=list(svc.POI_FILES.keys()),
            decay_scale_km=effective_decay,
            include_network=include_network,
            sort_by=sort_by,
        )
        rings = summary.get("rings") or []
        return rings[0] if rings else {"categories": {}, "totals": {}, "ratios": {}, "radius_km": radius_km}

    def build_feature_payload(
        self,
        lat: float,
        lng: float,
        radius_km: Optional[float] = None,
        decay_scale_km: Optional[float] = None,
        include_network: bool = True,
        sort_by: Literal["auto", "haversine", "network"] = "auto",
        include_road_metrics: bool = False,
        road_radius_km: Optional[float] = None,
    ) -> Dict[str, Any]:
        model_feature_names = self._resolve_model_feature_names() or []
        poi_specs, primary_radius = self._extract_poi_feature_specs(model_feature_names)

        if not poi_specs:
            fallback_radius = float(radius_km) if radius_km is not None else 1.0
            radius_label = f"{fallback_radius:g}"
            poi_specs = {
                radius_label: {
                    "distance_km": fallback_radius,
                    "categories": set(SiteAnalysisService.POI_FILES.keys()),
                    "kinds": {"count", "weight"},
                }
            }
            primary_radius = radius_label

        features: Dict[str, float] = {"lat": float(lat), "lng": float(lng)}
        ring_cache: Dict[str, Dict[str, Any]] = {}

        for dist_label, spec in poi_specs.items():
            radius_val = float(spec["distance_km"])
            ring = self._compute_ring_metrics(
                lat,
                lng,
                radius_val,
                decay_scale_km=decay_scale_km,
                include_network=include_network,
                sort_by=sort_by,
            )
            ring_cache[dist_label] = ring
            categories = spec["categories"] or set(SiteAnalysisService.POI_FILES.keys())
            cat_payload = ring.get("categories") or {}
            for cat in categories:
                payload = cat_payload.get(cat, {})
                if "count" in spec["kinds"]:
                    features[f"{cat}_count_{dist_label}_km"] = float(payload.get("count") or 0.0)
                if "weight" in spec["kinds"]:
                    features[f"{cat}_weight_{dist_label}_km"] = float(payload.get("sum_weight") or 0.0)

        if primary_radius is None:
            primary_radius = next(iter(poi_specs.keys()))

        primary_ring = ring_cache.get(primary_radius)
        if primary_ring:
            cat_payload = primary_ring.get("categories") or {}
            base_categories = [
                c for c in SiteAnalysisService.POI_FILES.keys() if c not in ("cafe", "cafes")
            ]
            total_count = 0.0
            total_weight = 0.0
            for cat in base_categories:
                payload = cat_payload.get(cat, {})
                total_count += float(payload.get("count") or 0.0)
                total_weight += float(payload.get("sum_weight") or 0.0)

            if "total_poi_count_km" in model_feature_names:
                features["total_poi_count_km"] = float(total_count)
            if "weighted_POI_strength" in model_feature_names:
                features["weighted_POI_strength"] = float(total_weight)

            eps = 1e-6
            for name in model_feature_names:
                if not name.endswith("_ratio"):
                    continue
                cat = name[: -len("_ratio")]
                if cat not in base_categories:
                    continue
                payload = cat_payload.get(cat, {})
                count_val = float(payload.get("count") or 0.0)
                features[name] = float(count_val / (total_count + eps))

            if "cafe_weight" in model_feature_names:
                cafe_payload = cat_payload.get("cafes") or cat_payload.get("cafe") or {}
                features["cafe_weight"] = float(cafe_payload.get("sum_weight") or 0.0)

        needs_road = bool((set(model_feature_names) & ROAD_ACCESS_SCORE_FEATURES_0_100) or
                          (set(model_feature_names) & ROAD_ACCESS_SCORE_FEATURES_0_1) or
                          include_road_metrics)
        road_payload = None
        if needs_road:
            road_radius = float(road_radius_km) if road_radius_km is not None else float(
                poi_specs[primary_radius]["distance_km"] if primary_radius else 1.0
            )
            road_payload = self._compute_road_access_score(
                float(lat),
                float(lng),
                road_radius,
            )
            if road_payload is not None:
                for name in model_feature_names:
                    if name in ROAD_ACCESS_SCORE_FEATURES_0_100:
                        features[name] = float(road_payload["score_0_100"])
                    if name in ROAD_ACCESS_SCORE_FEATURES_0_1:
                        features[name] = float(road_payload["score_0_1"])

        for col in model_feature_names:
            if col not in features:
                features[col] = 0.0

        return {
            "feature_names": model_feature_names,
            "features": features,
            "primary_radius_km": float(poi_specs[primary_radius]["distance_km"]) if primary_radius else None,
            "rings": ring_cache,
            "road_accessibility": road_payload,
        }

    def build_metrics_for_radius(
        self,
        lat: float,
        lng: float,
        radius_km: float,
        decay_scale_km: Optional[float] = None,
        include_network: bool = True,
        sort_by: Literal["auto", "haversine", "network"] = "auto",
    ) -> Dict[str, Any]:
        radius_val = float(radius_km)
        radius_label = f"{radius_val:g}"
        ring = self._compute_ring_metrics(
            lat,
            lng,
            radius_val,
            decay_scale_km=decay_scale_km,
            include_network=include_network,
            sort_by=sort_by,
        )
        features: Dict[str, float] = {"lat": float(lat), "lng": float(lng)}
        cat_payload = ring.get("categories") or {}
        for cat in SiteAnalysisService.POI_FILES.keys():
            payload = cat_payload.get(cat, {})
            features[f"{cat}_count_{radius_label}_km"] = float(payload.get("count") or 0.0)
            features[f"{cat}_weight_{radius_label}_km"] = float(payload.get("sum_weight") or 0.0)
        return {
            "radius_km": radius_val,
            "radius_label": radius_label,
            "ring": ring,
            "features": features,
        }

    def predict(
        self,
        lat: float,
        lng: float,
        radius_km: Optional[float] = None,
        decay_scale_km: Optional[float] = None,
        include_network: bool = True,
        sort_by: Literal["auto", "haversine", "network"] = "auto",
        include_road_metrics: bool = False,
        road_radius_km: Optional[float] = None,
    ) -> Dict[str, Any]:
        if self.model is None:
            raise RuntimeError("Model not loaded. Please check server logs.")

        payload = self.build_feature_payload(
            lat,
            lng,
            radius_km=radius_km,
            decay_scale_km=decay_scale_km,
            include_network=include_network,
            sort_by=sort_by,
            include_road_metrics=include_road_metrics,
            road_radius_km=road_radius_km,
        )
        feature_names = payload["feature_names"] or []
        features = payload["features"]
        sample_df = pd.DataFrame([features])
        if feature_names:
            sample_df = sample_df[feature_names]

        if isinstance(self.model, xgb.Booster):
            dtest = xgb.DMatrix(sample_df, feature_names=list(sample_df.columns))
            raw_score = float(self.model.predict(dtest)[0])
        else:
            raw_score = float(self.model.predict(sample_df)[0])

        access_score = None
        road_payload = payload.get("road_accessibility") if isinstance(payload, dict) else None
        if isinstance(road_payload, dict):
            access_score = road_payload.get("score_0_1")

        predicted_score = self._shape_score(raw_score, access_score)

        if predicted_score < 1.0:
            risk_level = "High"
        elif predicted_score < 2.0:
            risk_level = "Medium"
        else:
            risk_level = "Low"

        return {
            "predicted_score": predicted_score,
            "raw_score": raw_score,
            "risk_level": risk_level,
            "feature_payload": payload,
        }
