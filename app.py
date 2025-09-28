import pickle
import logging
from fastapi import FastAPI
from pydantic import BaseModel

# Setup logging
logging.basicConfig(filename="predictions.log", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

app = FastAPI()

# Load model and feature columns
with open("linear_regression_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("features.pkl", "rb") as f:
    feature_columns = pickle.load(f)

class PredictionInput(BaseModel):
    sqft: int
    bedrooms: int
    bathrooms: int
    age: int
    distance: float

@app.post("/predict")
def predict(input_data: PredictionInput):
    try:
        input_dict = input_data.dict()
        features = [input_dict[col] for col in feature_columns]
        prediction = model.predict([features])[0]

        # Log success
        logging.info(f"SUCCESS - Input: {input_dict}, Prediction: {prediction}")
        return {"predicted_price": prediction}

    except KeyError as e:
        error_message = f"Missing feature in input data: {e}"
        logging.error(f"ERROR - {error_message} - Input: {input_data.dict()}")
        return {"error": error_message}

    except Exception as e:
        logging.error(f"ERROR - {str(e)} - Input: {input_data.dict()}")
        return {"error": str(e)}
