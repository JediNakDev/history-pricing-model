import pandas as pd


def price_option(
    percent_change_series: pd.Series, percent_strike_price: float, option_type: str
) -> float:
    print("START PRICING OPTION")
    payoffs: pd.Series = (
        (percent_change_series - percent_strike_price).where(
            percent_change_series >= percent_strike_price, 0
        )
        if option_type == "call"
        else (percent_strike_price - percent_change_series).where(
            percent_change_series <= percent_strike_price, 0
        )
    )
    return payoffs.mean()
