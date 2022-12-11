from fastapi import FastAPI
from pydantic import BaseModel
from src.model.model import predict_pipeline
from src.model.model import __version__ as model_version

app = FastAPI()


@app.get("/")
async def get_model_version():
    return {"abstract_checker": "OK", "model_version": model_version}

@app.get("/predict/text={query_string}") #, response_model=PredictionOut)
async def predict(query_string: str):
    label = predict_pipeline(query_string)
    return {"label": label}

