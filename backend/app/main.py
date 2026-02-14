# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import cafe_processing
from app.api.endpoints import analysis
from app.api.endpoints import explain
from app.api.endpoints import pois
from app.api.endpoints import predict
from app.api.endpoints import road_types

app = FastAPI(
    title="Cafe Location Intelligence API",
    description="API for processing and predicting cafe suitability."
)

# CORS: allow frontend dev servers to call this API during development
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Include the router from endpoint files
app.include_router(cafe_processing.router, prefix="/api/v1", tags=["Cafe Processing"])
app.include_router(predict.router, prefix="/api/v1", tags=["Prediction"])
app.include_router(pois.router, prefix="/api/v1", tags=["POIS"])
app.include_router(road_types.router, prefix="/api/v1", tags=["Road Types"])
app.include_router(explain.router, prefix="/api/v1", tags=["Explanation"])
app.include_router(analysis.router, prefix="/api/v1", tags=["Analysis"])
# app.include_router(pois.router, prefix="/api/v1", tags=["POIS"])

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the Cafe Suitability API!"}