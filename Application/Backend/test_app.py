import sys
import os
from fastapi.testclient import TestClient
from unittest.mock import patch
import requests  # Import requests to access RequestException
from Application.Backend.app import app

client = TestClient(app)

# Add the project root to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello from the DevOps Pipeline!"}

# Mock data for successful conversion
mock_success_response = {
    "conversion_rates": {
        "EUR": 0.85,
        "GBP": 0.75,
        "JPY": 110.0,
        "USD": 1.0
    }
}

@patch("Application.Backend.app.requests.get")
def test_convert_currency_success(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_success_response

    response = client.get("/convert", params={
        "amount": 100,
        "from_currency": "USD",
        "to_currency": "EUR"
    })
    assert response.status_code == 200
    assert response.json() == {
        "converted_amount": 85.0,
        "from_currency": "USD",
        "to_currency": "EUR"
    }

@patch("Application.Backend.app.requests.get")
def test_convert_currency_invalid_currency(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_success_response

    response = client.get("/convert", params={
        "amount": 100,
        "from_currency": "USD",
        "to_currency": "XYZ"  # Invalid currency
    })
    assert response.status_code == 400
    assert "Invalid currency code: XYZ" in response.json()["detail"]

@patch("Application.Backend.app.requests.get")
def test_convert_currency_api_failure(mock_get):
    mock_get.side_effect = requests.exceptions.RequestException("API Failure")

    response = client.get("/convert", params={
        "amount": 100,
        "from_currency": "USD",
        "to_currency": "EUR"
    })
    assert response.status_code == 500
    assert "Error fetching exchange rates" in response.json()["detail"]

def test_convert_currency_missing_parameters():
    response = client.get("/convert", params={
        "amount": 100,
        "from_currency": "USD"
        # Missing 'to_currency'
    })
    assert response.status_code == 422  # Unprocessable Entity

def test_convert_currency_invalid_amount():
    response = client.get("/convert", params={
        "amount": "invalid",
        "from_currency": "USD",
        "to_currency": "EUR"
    })
    assert response.status_code == 422  # Unprocessable Entity
