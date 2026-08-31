import os

from dotenv import load_dotenv
from alpaca.data.historical import StockHistoricalDataClient

load_dotenv()

api_key = os.getenv("APCA_API_KEY_ID")
secret_key = os.getenv("APCA_API_SECRET_KEY")

client = StockHistoricalDataClient(
    api_key,
    secret_key
)

print("Alpaca client created successfully")