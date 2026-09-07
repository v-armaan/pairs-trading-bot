import pandas as pd
def build_equity_curve(pnl_df, initial_capital):
    """
    Build the portfolio equity curve from trade-level P&L.

    Each completed trade's P&L is added to the portfolio equity
    in chronological order.
    """

    pnl_df = pnl_df.sort_values("exit_date").reset_index(drop=True)

    equity = initial_capital
    portfolio_data = []

    for _, row in pnl_df.iterrows():

        equity += row["total_pnl"]

        portfolio_data.append(
            {
                "date": row["exit_date"],
                "trade_id": row["trade_id"],
                "trade_pnl": row["total_pnl"],
                "cumulative_pnl": equity - initial_capital,
                "equity": equity
            }
        )

    portfolio_df = pd.DataFrame(portfolio_data)

    return portfolio_df

import pandas as pd



def build_daily_equity_curve(
    pnl_df,
    trading_data,
    initial_capital,
    ticker_A,
    ticker_B,
):
    daily_data = trading_data[[ticker_A, ticker_B]].copy()
    daily_data["daily_pnl"] = 0.0

    for _, trade in pnl_df.iterrows():
        entry_date = trade["entry_date"]
        exit_date = trade["exit_date"]

        shares_A = trade["shares_A"]
        shares_B = trade["shares_B"]

        # Price movement starts after entry and ends on the exit date.
        trade_days = daily_data.loc[entry_date:exit_date].copy()
        price_change_A = trade_days[ticker_A].diff()
        price_change_B = trade_days[ticker_B].diff()

        if trade["direction"] == "LONG":
            # Long AMD, short MSFT
            trade_pnl = (
                shares_A * price_change_A
                - shares_B * price_change_B
            )

        else:
            # Short AMD, long MSFT
            trade_pnl = (
                -shares_A * price_change_A
                + shares_B * price_change_B
            )

        daily_data.loc[trade_days.index, "daily_pnl"] += (
            trade_pnl.fillna(0)
        )

    daily_data["equity"] = (
        initial_capital + daily_data["daily_pnl"].cumsum()
    )

    daily_data["daily_return"] = (
        daily_data["daily_pnl"]
        / daily_data["equity"].shift(1)
    )

    # Ensure the output has a consistent date column even when the input
    # price index is unnamed or is named something other than "date".
    daily_data.index.name = "date"
    equity_curve_df = daily_data.reset_index()

    equity_curve_df = equity_curve_df.rename(
        columns={"index": "date"}
    )

    equity_curve_df = equity_curve_df[
        ["date", "daily_pnl", "equity", "daily_return"]
    ]

    return equity_curve_df
