from fastapi import FastAPI
from pydantic import BaseModel
from src.model.model import predict_pipeline
from src.model.model import __version__ as model_version

app = FastAPI()

class TextIn(BaseModel):
    text: str


class PredictionOut(BaseModel):
    language: str

@app.get("/")
async def get_model_version():
    return {"abstract_checker": "OK", "model_version": model_version}

@app.post("/predict") #, response_model=PredictionOut)
async def predict(payload: TextIn):
    label = predict_pipeline(payload.text)
    return {"label": label}

