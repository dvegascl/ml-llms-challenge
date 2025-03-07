from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

class FlightData(BaseModel):
    OPERA: str
    TIPOVUELO: str
    MES: int

class PredictionRequest(BaseModel):
    flights: List[FlightData]

@app.get("/health", status_code=200)
async def get_health() -> dict:
    return {
        "status": "OK"
    }

@app.post("/predict", status_code=200)
async def post_predict(request: PredictionRequest) -> dict:
    # Para pruebas, simplemente devolvemos una predicción fija
    return {"predict": [0] * len(request.flights)}
