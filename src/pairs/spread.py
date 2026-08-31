def calculate_spread(prices, pair, alpha, beta):
    """
    Calculate the spread for a stock pair using its OLS hedge ratio.

    Parameters
    prices : pandas.DataFrame
        Price data for the pair.

    pair : tuple
        Stock pair in the form (stock1, stock2, pvalue).

    alpha : float
        OLS intercept estimated for the pair.

    beta : float
        OLS hedge ratio estimated for the pair.

    Returns
    pandas.Series
        Spread between the two stocks.
    """
    stock1 = pair[0]
    stock2 = pair[1]

    x = prices[stock1]
    y = prices[stock2]

    spread = y - (alpha + beta * x)

    return spread