import pickle
import sys

model_path = 'backend/models/xgb_baseline.pkl'
try:
    with open(model_path, 'rb') as f:
        obj = pickle.load(f)
    print(f"Type: {type(obj)}")
    if isinstance(obj, dict):
        print(f"Keys: {obj.keys()}")
except Exception as e:
    print(f"Error: {e}")
