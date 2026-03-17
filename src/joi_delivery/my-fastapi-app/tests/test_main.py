from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}  # Adjust based on your actual response

def test_read_items():
    response = client.get("/items/")
    assert response.status_code == 200
    # Add more assertions based on expected response for items endpoint

# Add more test cases as needed for other endpoints and functionalities