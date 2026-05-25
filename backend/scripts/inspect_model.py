import joblib
import os

model_path = 'backend/models/xgb_baseline.pkl'
try:
    obj = joblib.load(model_path)
    print(f"Type: {type(obj)}")
    if isinstance(obj, dict):
        print(f"Keys: {obj.keys()}")
    else:
        print(f"Object: {obj}")
except Exception as e:
    print(f"Error: {e}")
