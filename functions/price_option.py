import pandas as pd


def price_option(
    percent_change_series: pd.Series, percent_strike_price: float
) -> float:
    print("START PRICING OPTION")
    payoffs: pd.Series = (percent_change_series - percent_strike_price).where(
        percent_change_series >= percent_strike_price, 0
    )
    print(payoffs)
    return payoffs.mean()
