import pandas as pd


def calculate_zscore(spread, historical_spread=None):
    """
    Calculate z-scores without look-ahead bias.

    Parameters
    ----------
    spread : pandas.Series
        Spread for which z-scores are calculated.

    historical_spread : pandas.Series, optional
        Historical spread used to initialize the calculation.
        Used when calculating trading-period z-scores.

    Returns
    -------
    pandas.Series
        Z-score series.
    """

    if historical_spread is not None:

        combined_spread = pd.concat(
            [historical_spread, spread]
        )

    else:

        combined_spread = spread

    historical_mean = combined_spread.expanding().mean().shift(1)
    historical_std = combined_spread.expanding().std().shift(1)

    zscore = (
        combined_spread - historical_mean
    ) / historical_std

    if historical_spread is not None:
        return zscore.loc[spread.index]

    return zscore