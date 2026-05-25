import sys
import types

# Provide a minimal stub for joblib if it's not installed in this test environment
if 'joblib' not in sys.modules:
    stub = types.SimpleNamespace(load=lambda p: None)
    sys.modules['joblib'] = stub
# Stub xgboost minimally if not installed so tests can run without it
if 'xgboost' not in sys.modules:
    class _BoosterStub:
        def predict(self, dmatrix):
            return [0.0]

    def _DMatrix(df):
        return df

    xgb_stub = types.SimpleNamespace(Booster=_BoosterStub, DMatrix=_DMatrix)
    sys.modules['xgboost'] = xgb_stub

# Stub scipy.spatial.distance.cdist if scipy not available
if 'scipy' not in sys.modules:
    import types as _types
    import numpy as _np
    import types as _types_module
    # create module objects for scipy and scipy.spatial
    scipy_mod = _types_module.ModuleType('scipy')
    spatial_mod = _types_module.ModuleType('scipy.spatial')

    class _Distance:
        @staticmethod
        def cdist(a, b, metric='euclidean'):
            a = _np.asarray(a, dtype=float)
            b = _np.asarray(b, dtype=float)
            return _np.sqrt(((a[:, None, :] - b[None, :, :]) ** 2).sum(axis=2))

    spatial_mod.distance = _Distance
    scipy_mod.spatial = spatial_mod
    sys.modules['scipy'] = scipy_mod
    sys.modules['scipy.spatial'] = spatial_mod

from app.services.prediction_service import PredictionService

if __name__ == '__main__':
    svc = PredictionService.get_instance()
    # Ensure model and reference_df exist for testing (use stubs)
    if svc.model is None:
        svc.model = xgb_stub.Booster()
    import pandas as _pd
    if svc.reference_df is None:
        svc.reference_df = _pd.DataFrame([{'lat':27.67, 'lng':85.43}])
    # minimal feature names if absent
    if not svc.feature_names:
        svc.feature_names = ['lat','lng','banks_count_1km','education_count_1km','health_count_1km','temples_count_1km','other_count_1km','banks_weight_1km','education_weight_1km','health_weight_1km','temples_weight_1km','other_weight_1km','total_poi_count_1km','bank_ratio','education_ratio','temple_ratio','health_ratio','weighted_POI_strength']

    print('Loaded model:', svc.model is not None)
    print('Data dir:', svc.data_dir)
    try:
        res = svc.predict(27.6742856, 85.4327744)
        print('Predict result:', res)
    except Exception as e:
        print('Predict error:', repr(e))
