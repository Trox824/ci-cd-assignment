from fastapi import FastAPI, HTTPException
import requests
import logging
from fastapi.middleware.cors import CORSMiddleware  # Import CORSMiddleware

app = FastAPI()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure CORS
origins = [
    "http://localhost:3000",             # Frontend URL for local development
    "http://44.211.160.71:3000",         # Frontend URL via Public IPv4
    # Add other origins if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,                # Allow specified origins
    allow_credentials=True,
    allow_methods=["*"],                  # Allow all HTTP methods
    allow_headers=["*"],                  # Allow all headers
)

# Base URL for the Exchange rate API
BASE_API_URL = "https://v6.exchangerate-api.com/v6/c794e36475a70d94f5e6bbf2/latest/"

@app.get("/")
def read_root():
    return {"message": "Hello from the DevOps Pipeline!"}

@app.get("/convert")
def convert_currency(amount: float, from_currency: str, to_currency: str):
    api_url = f"{BASE_API_URL}{from_currency}"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        rates = data.get("conversion_rates", {})
        if to_currency not in rates:
            raise HTTPException(status_code=400, detail=f"Invalid currency code: {to_currency}")
        converted_amount = amount * rates[to_currency]
        return {
            "converted_amount": converted_amount,
            "from_currency": from_currency,
            "to_currency": to_currency
        }
    except requests.exceptions.RequestException:
        raise HTTPException(status_code=500, detail="Error fetching exchange rates")
