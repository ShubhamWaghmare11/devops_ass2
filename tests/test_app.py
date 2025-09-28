from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_predict_endpoint():
    # Example input matching your PredictionInput model
    input_data = {
        "sqft": 1000,
        "bedrooms": 3,
        "bathrooms": 2,
        "age": 5,
        "distance": 10.5
    }
    
    response = client.post("/predict", json=input_data)
    
    # Check if the response status is 200 OK
    assert response.status_code == 200
    
    # Check if the response contains 'predicted_price'
    assert "predicted_price" in response.json()
