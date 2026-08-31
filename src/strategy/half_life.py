import math
import numpy as np
import pandas as pd


def calculate_half_life(spread):
    """
    Calculate the mean-reversion half-life of a spread.

    Parameters
    ----------
    spread : pandas.Series
        Spread series used to estimate the speed of mean reversion.

    Returns
    -------
    float
        Estimated half-life of the spread.
    """

    x = spread.shift(1)
    y = spread.diff()

    combined = pd.concat([x, y], axis=1)
    combined.dropna(inplace=True)

    slope, intercept = np.polyfit(
        combined.iloc[:, 0],
        combined.iloc[:, 1],
        1
    )

    half_life = abs(math.log(2, math.e) / slope)

    return half_life