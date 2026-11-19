import os
from contextlib import asynccontextmanager
import joblib
import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "modelo", "modelo.joblib")

# MODELO
@asynccontextmanager
async def loadmodel(app: FastAPI):
    app.state.model = joblib.load(MODEL_PATH)
    yield

# API
app = FastAPI(
    title="CardioCheck API",
    description="API de predicción de riesgo cardiovascular con Machine Learning",
    version="1.0.0",
    lifespan=loadmodel
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# INPUT
class PacienteEntrada(BaseModel):
    age: int = Field(..., ge=18, le=120, description="Edad del paciente")
    sex: int = Field(..., ge=0, le=1, description="0 = Femenino, 1 = Masculino")
    chest: int = Field(..., ge=1, le=4, description="Tipo de dolor torácico (1 a 4)")
    resting_blood_pressure: float = Field(..., ge=50, le=250, description="Presión arterial en reposo")
    serum_cholestoral: float = Field(..., ge=80, le=700, description="Colesterol sérico (mg/dl)")
    maximum_heart_rate_achieved: float = Field(..., ge=50, le=250, description="Frecuencia cardíaca máx")
    exercise_induced_angina: int = Field(..., ge=0, le=1, description="Angina por ejercicio (0 o 1)")


# HEALTH
@app.get("/health")
def health_check():
    return {"estado": "ok"}


# POST
@app.post("/predecir")
def predecir(paciente: PacienteEntrada):

    df_paciente = pd.DataFrame([paciente.model_dump()])
    
  
    prediccion = int(app.state.model.predict(df_paciente)[0])
    probabilidad = float(app.state.model.predict_proba(df_paciente)[0][1])
    
    return {
        "prediccion": prediccion,
        "probabilidad": round(probabilidad, 4),
        "diagnostico": "Riesgo cardíaco detectado" if prediccion == 1 else "Bajo riesgo"
    }

