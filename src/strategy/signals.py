def calculate_thresholds(zscore, lower_percentile=0.05, upper_percentile=0.95):
    """
    Calculate lower and upper z-score thresholds from formation data.

    Parameters
    ----------
    zscore : pandas.Series
        Formation-period z-score series.
    lower_percentile : float, default=0.05
        Lower percentile used for the entry threshold.
    upper_percentile : float, default=0.95
        Upper percentile used for the entry threshold.

    Returns
    -------
    tuple
        Lower and upper z-score thresholds.
    """

    zscore = zscore.dropna()

    lower_threshold = zscore.quantile(lower_percentile)
    upper_threshold = zscore.quantile(upper_percentile)

    return lower_threshold, upper_threshold
import pandas as pd


def get_thresholds(formation_zscores):
    """
    Extract trading thresholds from the formation-period z-score data.

    Parameters
    ----------
    formation_zscores : list
        Formation z-score statistics.

    Returns
    -------
    tuple
        Lower threshold, upper threshold, and formation median.
    """

    lower_threshold = formation_zscores[0][8]
    upper_threshold = formation_zscores[0][9]
    formation_median = formation_zscores[0][7].quantile(0.5)

    return lower_threshold, upper_threshold, formation_median


def initialize_position_dataframe(trading_zscore):
    """
    Create the DataFrame used for signal generation.

    Parameters
    ----------
    trading_zscore : pandas.Series
        Z-score calculated over the trading period.

    Returns
    -------
    pandas.DataFrame
        DataFrame containing z-score, position, and event columns.
    """

    position_df = pd.DataFrame(trading_zscore.copy())
    position_df = position_df.rename(columns={0: "zscore"})

    position_df["position"] = 0
    position_df["event"] = "NO_EVENT"

    return position_df


def generate_signals(trading_zscore, formation_zscores, max_holding_period):
    """
    Generate trading positions and entry/exit events.

    Parameters
    ----------
    trading_zscore : pandas.Series
        Z-score calculated over the trading period.

    formation_zscores : list
        Formation-period z-score statistics used to determine
        entry and exit thresholds.

    max_holding_period : int or float
        Maximum number of trading observations a position
        can be held.

    Returns
    -------
    pandas.DataFrame
        DataFrame containing the trading-period z-score,
        position state, and event for each observation.
    """

    # Get formation-period thresholds
    lower_threshold, upper_threshold, formation_median = (
        get_thresholds(formation_zscores)
    )

    # Create output DataFrame
    position_df = initialize_position_dataframe(trading_zscore)

    # Position states:
    #  0  = flat
    #  1  = long
    # -1  = short
    #  2  = cooldown after long stop-loss
    # -2  = cooldown after short stop-loss

    position = 0
    entry_day = None

    for i in range(len(position_df)):

        current_zscore = position_df.iloc[i, 0]

        # --------------------------------
        # FLAT: look for a new entry
        # --------------------------------
        if position == 0:

            if current_zscore < lower_threshold:

                position = 1
                entry_day = i

                position_df.loc[
                    position_df.index[i], "event"
                ] = "LONG_ENTRY"

            elif current_zscore > upper_threshold:

                position = -1
                entry_day = i

                position_df.loc[
                    position_df.index[i], "event"
                ] = "SHORT_ENTRY"

        # --------------------------------
        # LONG POSITION
        # --------------------------------
        elif position == 1:

            # Mean reversion
            if current_zscore >= formation_median:

                position = 0
                entry_day = None

                position_df.loc[
                    position_df.index[i], "event"
                ] = "LONG_MEAN_EXIT"

            # Stop loss
            elif current_zscore <= lower_threshold - 1:

                position = 2
                entry_day = None

                position_df.loc[
                    position_df.index[i], "event"
                ] = "LONG_STOPLOSS"

            # Maximum holding period
            elif i - entry_day >= max_holding_period:

                position = 0
                entry_day = None

                position_df.loc[
                    position_df.index[i], "event"
                ] = "LONG_MAX_HOLDING"

        # --------------------------------
        # SHORT POSITION
        # --------------------------------
        elif position == -1:

            # Mean reversion
            if current_zscore <= formation_median:

                position = 0
                entry_day = None

                position_df.loc[
                    position_df.index[i], "event"
                ] = "SHORT_MEAN_EXIT"

            # Stop loss
            elif current_zscore >= upper_threshold + 1:

                position = -2
                entry_day = None

                position_df.loc[
                    position_df.index[i], "event"
                ] = "SHORT_STOPLOSS"

            # Maximum holding period
            elif i - entry_day >= max_holding_period:

                position = 0
                entry_day = None

                position_df.loc[
                    position_df.index[i], "event"
                ] = "SHORT_MAX_HOLDING"

        # --------------------------------
        # COOLDOWN AFTER LONG STOP
        # --------------------------------
        elif position == 2:

            if current_zscore > lower_threshold:

                position = 0

                position_df.loc[
                    position_df.index[i], "event"
                ] = "LONG_REENTRY_UNLOCK"

        # --------------------------------
        # COOLDOWN AFTER SHORT STOP
        # --------------------------------
        elif position == -2:

            if current_zscore < upper_threshold:

                position = 0

                position_df.loc[
                    position_df.index[i], "event"
                ] = "SHORT_REENTRY_UNLOCK"

        # Store current position
        position_df.loc[
            position_df.index[i], "position"
        ] = position

    return position_df