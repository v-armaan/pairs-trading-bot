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