import os
import joblib
import pandas as pd
import numpy as np
import xgboost as xgb
from scipy.spatial import distance
from pathlib import Path
from typing import Dict, Any, Optional

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
            self.backend_root / "Data" / "CSV" / "final",
            self.backend_root / "Data" / "CSV_Reference" / "final",
            self.backend_root / "Data" / "CSV",
            self.backend_root / "Data" / "CSV_Reference",
        ]

        for candidate in candidates:
            candidate = candidate.resolve()
            if (candidate / "master_cafes_minimal.csv").is_file():
                return candidate

        print(
            "Warning: Could not locate master_cafes_minimal.csv in default locations. "
            "Continuing with backend/Data/CSV/final."
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

    def predict(self, lat: float, lng: float, k_neighbors: int = 5) -> Dict[str, Any]:
        if self.model is None:
            raise RuntimeError("Model not loaded. Please check server logs.")
        if self.reference_df is None:
            raise RuntimeError("Reference data not loaded. Cannot perform feature estimation.")

        # 1. Find k-nearest neighbors
        existing_coords = self.reference_df[['lat', 'lng']].values
        new_coord = np.array([[lat, lng]])
        
        # Calculate Euclidean distances
        distances = distance.cdist(new_coord, existing_coords, 'euclidean')[0]
        
        # Get k-nearest neighbors
        nearest_indices = np.argsort(distances)[:k_neighbors]
        nearest_cafes = self.reference_df.iloc[nearest_indices]
        
        # 2. Estimate POI features by averaging nearest neighbors
        poi_count_cols = [c for c in self.reference_df.columns if c.endswith('_count_1km')]
        poi_weight_cols = [c for c in self.reference_df.columns if c.endswith('_weight_1km')]
        
        new_features = {}
        
        # Copy raw POI features (averaged from neighbors)
        for col in poi_count_cols + poi_weight_cols:
            new_features[col] = nearest_cafes[col].mean()

        # Include cafe_weight if present in the reference data
        if 'cafe_weight' in self.reference_df.columns:
            new_features['cafe_weight'] = nearest_cafes['cafe_weight'].mean()
        
        # Add lat/lng
        new_features['lat'] = lat
        new_features['lng'] = lng
        
        # Create a temporary dataframe for feature engineering
        temp_df = pd.DataFrame([new_features])
        
        # 3. Feature Engineering (Must match notebook logic)
        eng_new = pd.DataFrame(index=temp_df.index)
        EPSILON = 1e-6
        
        # Helper to safely get column or 0
        def get_col(df, col_name):
            return df[col_name].fillna(0) if col_name in df.columns else 0

        # Total POI Count
        eng_new['total_poi_count_1km'] = (
            get_col(temp_df, 'banks_count_1km') +
            get_col(temp_df, 'education_count_1km') +
            get_col(temp_df, 'health_count_1km') +
            get_col(temp_df, 'temples_count_1km') +
            get_col(temp_df, 'other_count_1km')
        )
        
        # Category Ratios
        total_poi = eng_new['total_poi_count_1km'] + EPSILON
        eng_new['bank_ratio'] = get_col(temp_df, 'banks_count_1km') / total_poi
        eng_new['education_ratio'] = get_col(temp_df, 'education_count_1km') / total_poi
        eng_new['temple_ratio'] = get_col(temp_df, 'temples_count_1km') / total_poi
        eng_new['health_ratio'] = get_col(temp_df, 'health_count_1km') / total_poi
        
        # Weighted POI Strength
        eng_new['weighted_POI_strength'] = (
            get_col(temp_df, 'banks_weight_1km') +
            get_col(temp_df, 'education_weight_1km') +
            get_col(temp_df, 'health_weight_1km') +
            get_col(temp_df, 'temples_weight_1km') +
            get_col(temp_df, 'other_weight_1km')
        )
        
        # Combine with raw features
        sample_full = pd.concat([temp_df.reset_index(drop=True), eng_new.reset_index(drop=True)], axis=1)

        model_feature_names = self._resolve_model_feature_names()
        if model_feature_names:
            for col in model_feature_names:
                if col not in sample_full.columns:
                    sample_full[col] = 0.0
            sample_df = sample_full[model_feature_names]
        else:
            # Fallback if feature names not loaded (risky)
            print("Warning: No feature names available. Using all engineered features.")
            sample_df = sample_full

        # Make prediction
        if isinstance(self.model, xgb.Booster):
            dtest = xgb.DMatrix(sample_df, feature_names=list(sample_df.columns))
            predicted_score = float(self.model.predict(dtest)[0])
        else:
            predicted_score = float(self.model.predict(sample_df)[0])
        
        # Risk assessment
        if predicted_score < 1.0:
            risk_level = 'High'
        elif predicted_score < 2.0:
            risk_level = 'Medium'
        else:
            risk_level = 'Low'
            
        return {
            "predicted_score": predicted_score,
            "risk_level": risk_level,
            "estimated_features": new_features
        }
