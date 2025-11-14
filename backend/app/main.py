# app/main.py
from fastapi import FastAPI
from app.api.endpoints import cafe_processing

app = FastAPI(
    title="Cafe Location Intelligence API",
    description="API for processing and predicting cafe suitability."
)

# Include the router from the cafe_processing endpoint file
app.include_router(cafe_processing.router, prefix="/api/v1", tags=["Cafe Processing"])

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the Cafe Suitability API!"}