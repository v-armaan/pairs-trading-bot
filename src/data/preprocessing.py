import pandas as pd


def prepare_price_data(bars):
    """
    Convert Alpaca historical bars into a price DataFrame.

    Parameters
    ----------
    bars : Alpaca BarSet
        Historical stock bars returned by Alpaca.

    Returns
    -------
    pandas.DataFrame
        DataFrame with timestamps as the index and stock symbols
        as columns containing closing prices.
    """

    df = bars.df.reset_index()

    prices = df.pivot(
        index="timestamp",
        columns="symbol",
        values="close"
    )

    prices = prices.sort_index()

    return prices

def split_data(prices, formation_end):
    """
    Split price data into formation and trading periods.
    """

    formation_end = pd.Timestamp(formation_end)

    formation_prices = prices.loc[
        prices.index.date <= formation_end.date()
    ]

    trading_prices = prices.loc[
        prices.index.date > formation_end.date()
    ]

    return formation_prices, trading_prices