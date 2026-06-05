import sys
import os

backend_path = os.path.abspath(r'd:\projects\Finalproject\SiteX\backend')
sys.path.append(backend_path)

from app.services.gnn_prediction_service import GNNPredictionService
try:
    service = GNNPredictionService.get_instance()
    print("Service initialized")
    print(service.predict(27.680992, 85.394746))
except Exception as e:
    import traceback
    traceback.print_exc()
