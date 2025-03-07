import os
import fastapi
import joblib
import pandas as pd
import uvicorn
from challenge.model import DelayModel

# Inicializar FastAPI
app = fastapi.FastAPI()

# Cargar el modelo entrenado
model_path = "/app/challenge/model.pkl"  # Ruta en Render
try:
    model = joblib.load(model_path)
    print("✅ Modelo cargado correctamente.")
except Exception as e:
    print(f"❌ Error al cargar el modelo: {e}")
    model = None  # Evita errores si el modelo no está disponible

@app.get("/health", status_code=200)
async def get_health() -> dict:
    return {"status": "OK"}

@app.post("/predict", status_code=200)
async def post_predict(data: dict) -> dict:
    """
    Recibe un JSON con los datos del vuelo y devuelve la predicción de retraso (1 = retraso, 0 = no retraso).
    """
    if model is None:
        return {"error": "Modelo no disponible"}

    # Convertir JSON a DataFrame
    df = pd.DataFrame([data])

    # Preprocesar datos
    delay_model = DelayModel()
    features = delay_model.preprocess(df)

    # Hacer predicción
    prediction = model.predict(features).tolist()
    
    return {"prediction": prediction}

# Ejecutar en Render con puerto dinámico
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render usa un puerto dinámico
    uvicorn.run(app, host="0.0.0.0", port=port)
