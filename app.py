from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

# Load saved model
model = joblib.load("model.pkl")

# Request schema
class IrisInput(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Iris ML Model API is running 🚀"}

@app.post("/predict")
def predict(data: IrisInput):
    X = np.array([[data.sepal_length, data.sepal_width, data.petal_length, data.petal_width]])
    prediction = model.predict(X)[0]
    return {"prediction": int(prediction)}
