import pickle
import random
import logging
from fastapi import FastAPI
from pydantic import BaseModel

# ------------------------------
# Setup FastAPI
# ------------------------------
app = FastAPI(title="House Price Predictor")

# ------------------------------
# Load Model & Feature Columns
# ------------------------------
with open("linear_regression_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("features.pkl", "rb") as f:
    feature_columns = pickle.load(f)

# ------------------------------
# Logging Setup
# ------------------------------
logging.basicConfig(
    filename="predictions.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s:%(message)s"
)

# ------------------------------
# Pydantic Model for Input
# ------------------------------
class PredictionInput(BaseModel):
    sqft: int
    bedrooms: int
    bathrooms: int
    age: int
    distance: float

# ------------------------------
# Prediction Endpoint
# ------------------------------
@app.post("/predict")
def predict(input_data: PredictionInput):
    input_dict = input_data.dict()
    
    try:
        # Random intentional exception (50% chance)
        if random.random() < 0.5:
            raise ValueError("Intentional random error for testing logs")
        
        # Prepare features
        features = [input_dict[col] for col in feature_columns]
        prediction = model.predict([features])[0]

        # Log successful prediction
        logging.info(f"Input: {input_dict}, Prediction: {prediction}")
    
    except Exception as e:
        # Log the exception but still produce prediction
        logging.error(f"Exception occurred: {e}, Input: {input_dict}")
        # Still produce prediction even if error occurs
        features = [input_dict.get(col, 0) for col in feature_columns]  # fallback for missing features
        prediction = model.predict([features])[0]

    return {"predicted_price": prediction}
