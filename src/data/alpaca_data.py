import os

from dotenv import load_dotenv

from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame


load_dotenv()

api_key = os.getenv("APCA_API_KEY_ID")
secret_key = os.getenv("APCA_API_SECRET_KEY")

alpaca_client = StockHistoricalDataClient(
    api_key=api_key,
    secret_key=secret_key
)


def get_stock_bars(symbols, start, end):
    """
    Fetch daily stock price data from Alpaca.

    Parameters
    ----------
    symbols : str or list
        Stock ticker or list of stock tickers.

    start : str
        Start date in YYYY-MM-DD format.

    end : str
        End date in YYYY-MM-DD format.

    Returns
    -------
    BarSet
        Historical daily stock bars returned by Alpaca.
    """

    request = StockBarsRequest(
        symbol_or_symbols=symbols,
        timeframe=TimeFrame.Day,
        start=start,
        end=end
    )

    bars = alpaca_client.get_stock_bars(request)

    return bars