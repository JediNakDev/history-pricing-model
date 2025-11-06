import pandas as pd


def price_option(
    price_at_maturity: pd.Series, strike_price: float, option_type: str
) -> float:
    print("START PRICING OPTION")
    payoffs: pd.Series = (
        (price_at_maturity - strike_price).where(price_at_maturity >= strike_price, 0)
        if option_type == "call"
        else (strike_price - price_at_maturity).where(
            price_at_maturity <= strike_price, 0
        )
    )
    return payoffs.mean()
