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
    "http://localhost:3000",  # Frontend URL
    # Add other origins if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # Allow specified origins
    allow_credentials=True,
    allow_methods=["*"],              # Allow all HTTP methods
    allow_headers=["*"],              # Allow all headers
)

# Base URL for the Exchange rate API
BASE_API_URL = "https://v6.exchangerate-api.com/v6/c794e36475a70d94f5e6bbf2/latest/"

@app.get("/convert")
def convert_currency(amount: float, from_currency: str, to_currency: str):
    try:
        # Fetch exchange rates using the 'from_currency' as the base
        api_url = f"{BASE_API_URL}{from_currency.upper()}"
        logger.info(f"Requesting exchange rates from: {api_url}")
        
        response = requests.get(api_url)
        response.raise_for_status()  # Raise HTTPError for bad responses
        data = response.json()
        
        logger.info(f"API Response: {data}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching exchange rates: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching exchange rates: {str(e)}")

    # Check if "conversion_rates" is in the response
    if "conversion_rates" not in data:
        logger.error(f"Invalid response format: {data}")
        raise HTTPException(status_code=500, detail="Invalid response format")

    # Get exchange rate for the target currency
    to_rate = data["conversion_rates"].get(to_currency.upper())

    if to_rate is None:
        logger.error(f"Invalid currency code: {to_currency}")
        raise HTTPException(status_code=400, detail=f"Invalid currency code: {to_currency}")

    # Perform conversion
    try:
        converted_amount = amount * to_rate
        logger.info(f"Conversion successful: {amount} {from_currency} = {converted_amount} {to_currency}")
        return {
            "converted_amount": converted_amount,
            "from_currency": from_currency,
            "to_currency": to_currency
        }
    except Exception as e:
        logger.error(f"Error during conversion: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error during conversion: {str(e)}")
