from statsmodels.tsa.stattools import coint,adfuller
from statsmodels.api import OLS, add_constant


def find_cointegrated_pairs(formation_prices,candidate_pairs,significance=0.05):
    coint_pairs=[]
    for pair in candidate_pairs:
        cstat,pvalue,_=coint(formation_prices[pair[0]],formation_prices[pair[1]])
        if pvalue<significance:
            coint_pairs.append((pair[0],pair[1],pvalue))
    return coint_pairs



def fit_hedge_ratio(prices,pair):
    """
    Estimate the OLS intercept and hedge ratio for a stock pair.

    Parameters
    ----------
    prices : pandas.DataFrame
        Price data for the formation period.

    pair : tuple
        Cointegrated pair in the form (stock1, stock2, pvalue).

    Returns
    -------
    tuple
        OLS intercept (alpha) and hedge ratio (beta).
    """
    stock1 = pair[0]
    stock2 = pair[1]

    y = prices[stock2]
    x = prices[stock1]

    X = add_constant(x)#lets ols estimate alpha

    model = OLS(y, X).fit()

    alpha = model.params.iloc[0]
    beta = model.params.iloc[1]

    return alpha, beta

def adf_test(spread, significance=0.05):
    """
    Test whether a spread is stationary using the Augmented Dickey-Fuller test.

    Parameters
    spread : pandas.Series
        Spread series to test for stationarity.

    significance : float, default=0.05
        Maximum p-value for rejecting the null hypothesis of a unit root.

    Returns
    float
        ADF test p-value.
    """

    adf_result = adfuller(spread)
    pvalue = adf_result[1]

    return pvalue
    