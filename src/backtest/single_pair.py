import pandas as pd


def construct_trades(position_df):
    """
    Pair each entry signal with the next corresponding exit signal
    and construct a trade-level DataFrame.

    Holding period is measured in trading days.
    """

    trades = []

    entry_day = None
    entry_zscore = None
    direction = None

    for date, row in position_df.iterrows():

        event = row["event"]

        # ENTRY
        if event == "LONG_ENTRY":

            entry_day = date
            entry_zscore = row["zscore"]
            direction = "LONG"

        elif event == "SHORT_ENTRY":

            entry_day = date
            entry_zscore = row["zscore"]
            direction = "SHORT"

        # EXIT
        elif event in [
            "LONG_MEAN_EXIT",
            "LONG_STOPLOSS",
            "LONG_MAX_HOLDING",
            "SHORT_MEAN_EXIT",
            "SHORT_STOPLOSS",
            "SHORT_MAX_HOLDING"
        ]:

            # Make sure the exit matches the open position
            if direction == "LONG" and event.startswith("LONG_"):
                pass

            elif direction == "SHORT" and event.startswith("SHORT_"):
                pass

            else:
                continue

            # Calculate holding period in trading days
            holding_period = position_df.loc[entry_day:date].shape[0] - 1

            trade = {
                "trade_id": len(trades) + 1,
                "direction": direction,
                "entry_date": entry_day,
                "exit_date": date,
                "entry_zscore": entry_zscore,
                "exit_zscore": row["zscore"],
                "exit_reason": event,
                "holding_period": holding_period
            }

            trades.append(trade)

            # Reset after completing the trade
            entry_day = None
            entry_zscore = None
            direction = None

    trade_df = pd.DataFrame(trades)

    return trade_df

from math import floor


def calculate_trade_pnl(trade_df, trading_data, initial_capital, ticker_A, ticker_B):
    """
    Calculate trade-level P&L for a single pair.

    Each leg is sized with approximately half of the initial capital.
    LONG spread  = long A, short B
    SHORT spread = short A, long B

    Returns a DataFrame containing the original trade information
    along with prices, share quantities, leg P&Ls, total P&L,
    and trade return.
    """

    pandl_all = []

    for _, row in trade_df.iterrows():

        entry_date = row["entry_date"]
        exit_date = row["exit_date"]
        direction = row["direction"]

        entry_price_A = trading_data.loc[entry_date, ticker_A]
        entry_price_B = trading_data.loc[entry_date, ticker_B]

        exit_price_A = trading_data.loc[exit_date, ticker_A]
        exit_price_B = trading_data.loc[exit_date, ticker_B]

        shares_A = floor(initial_capital / (2 * entry_price_A))
        shares_B = floor(initial_capital / (2 * entry_price_B))

        if direction == "LONG":

            pnl_A = shares_A * (exit_price_A - entry_price_A)
            pnl_B = shares_B * (entry_price_B - exit_price_B)

        elif direction == "SHORT":

            pnl_A = shares_A * (entry_price_A - exit_price_A)
            pnl_B = shares_B * (exit_price_B - entry_price_B)

        total_pnl = pnl_A + pnl_B

        trade_return = total_pnl / initial_capital

        pandl_all.append(
            {
                "entry_price_A": entry_price_A,
                "exit_price_A": exit_price_A,
                "entry_price_B": entry_price_B,
                "exit_price_B": exit_price_B,
                "shares_A": shares_A,
                "shares_B": shares_B,
                "pnl_A": pnl_A,
                "pnl_B": pnl_B,
                "total_pnl": total_pnl,
                "trade_return%": trade_return * 100
            }
        )

    pnl_df = pd.DataFrame(pandl_all)

    pnl_df = pd.concat(
        [
            trade_df.reset_index(drop=True),
            pnl_df
        ],
        axis=1
    )

    return pnl_df



