# SiteX — Site Suitability / Cafe Location Intelligence

SiteX is a data-driven site suitability analysis project. The current implementation focuses on **franchised cafés / coffee shops**, providing:

- A **FastAPI** backend that can (a) flatten raw cafe place JSON into a clean tabular shape and (b) **predict a suitability score** for a latitude/longitude using a trained XGBoost model + local feature estimation.
- A **React + TypeScript + Vite** frontend that lets you pick a location and view a result page with a map, nearby POIs (from packaged CSVs), and the predicted score.

## Repository layout

- [backend/](backend/) — FastAPI app, model + data, notebooks
  - [backend/app/main.py](backend/app/main.py) — API entrypoint
  - [backend/app/api/endpoints/](backend/app/api/endpoints/) — routes
  - [backend/app/services/prediction_service.py](backend/app/services/prediction_service.py) — model loading + prediction
  - [backend/models/](backend/models/) — trained model artifacts (expects [backend/models/xgb_baseline.pkl](backend/models/xgb_baseline.pkl))
  - [backend/Data/](backend/Data/) — data scripts + CSV datasets
- [site_x_ui/](site_x_ui/) — React UI (Vite)
  - [site_x_ui/src/pages/Result.tsx](site_x_ui/src/pages/Result.tsx) — calls the backend prediction endpoint
  - [site_x_ui/data/](site_x_ui/data/) — CSV/GeoJSON packaged with the UI

## Tech stack

- Backend: FastAPI, Uvicorn, Pandas, scikit-learn, XGBoost, SciPy, joblib
- Frontend: React, TypeScript, Vite, Tailwind, Leaflet (react-leaflet)

## Quickstart (local development)

### 1) Start the backend API (FastAPI)

Prereqs: Python 3.10+ recommended.

PowerShell:

```powershell
cd backend

python -m venv .venv
.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
pip install -r requirements.txt

uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Environment variable for Gemini (optional, for AI explanations):

- macOS/Linux (bash/zsh):

```bash
export GEMINI_API_KEY="YOUR_API_KEY"
```

- Windows PowerShell:

```powershell
$env:GEMINI_API_KEY = "YOUR_API_KEY"
```

Note: keep your API key out of git (do not commit it). You can also set it in your shell profile so it persists across sessions.

Then open:

- Swagger UI: http://127.0.0.1:8000/docs
- Health/root: http://127.0.0.1:8000/

Notes:

- CORS is configured to allow Vite dev servers on `http://localhost:5173`.
- The prediction endpoint requires the model + reference CSV present (see “Model & data”).

### 2) Start the frontend (Vite)

Prereqs: Node.js 18+ recommended.

PowerShell (new terminal):

```powershell
cd site_x_ui
npm install
npm run dev
```

Open the URL Vite prints (typically http://127.0.0.1:5173).

## API

Base URL (dev): `http://127.0.0.1:8000`

### `POST /api/v1/process-cafes/`

Flattens raw cafe place JSON objects into a consistent tabular schema.

Request body:

```json
{
  "data": [
    {
      "title": "Cafe Boh",
      "location": { "lat": 27.67, "lng": 85.39 },
      "additionalInfo": {
        "Amenities": [{ "Free Wi-Fi": true }]
      }
    }
  ]
}
```

Response: a list of flattened dicts.

### `POST /api/v1/predict-score/`

Predicts a suitability score from latitude/longitude.

Request body:

```json
{ "lat": 27.670587, "lng": 85.420868 }
```

Response:

```json
{
  "predicted_score": 1.234,
  "risk_level": "Medium",
  "estimated_features": {
    "banks_count_1km": 3.2,
    "banks_weight_1km": 0.8
  }
}
```

### `POST /api/v1/explain/`

Generates a natural-language explanation of per-point scores and top POI contributors using Google Gemini.

Requires: `GEMINI_API_KEY` environment variable (see Quickstart section).

### POIs endpoint (currently disabled)

There is a POI lookup endpoint implemented in [backend/app/api/endpoints/pois.py](backend/app/api/endpoints/pois.py), but it is **not currently mounted** in the app (see [backend/app/main.py](backend/app/main.py)).

If you enable it (uncomment the router include), it exposes:

- `GET /api/v1/pois/?lat=...&lon=...&radius_km=1.0`

## Model & data

The prediction service loads resources relative to the backend folder:

- Model: [backend/models/xgb_baseline.pkl](backend/models/) (required)
- Feature list (optional but recommended): [backend/models/model_features.pkl](backend/models/model_features.pkl)
- Reference CSV used for local k-NN feature estimation:
  - [backend/Data/CSV/final/master_cafes_minimal.csv](backend/Data/CSV/final/master_cafes_minimal.csv)

If the feature list file is missing, the service falls back to using all engineered features (you may see a warning in server logs).

## Training / notebooks

- Model training notebook: [backend/notebooks/train_xgb.ipynb](backend/notebooks/train_xgb.ipynb)

## Troubleshooting

- **`503 Model not loaded`**: ensure [backend/models/](backend/models/) contains [backend/models/xgb_baseline.pkl](backend/models/xgb_baseline.pkl).
- **`503 Reference data not loaded`**: ensure [backend/Data/CSV/final/master_cafes_minimal.csv](backend/Data/CSV/final/master_cafes_minimal.csv) exists.
- **Frontend can’t reach backend**: confirm the backend is running on `127.0.0.1:8000` (the UI currently fetches `http://127.0.0.1:8000/api/v1/predict-score/`).
- **XGBoost install issues on Windows**: try upgrading `pip` first; if it persists, install a compatible Python version (3.10/3.11 typically has wheels available).

## Status

- Backend Dockerfile and backend config module exist but are currently empty placeholders.
- Backend tests folder exists but does not currently contain runnable tests.
