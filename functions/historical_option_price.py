from fetch_price import fetch_price
from calc_percent_change import calc_percent_change
from price_option import price_option


def historical_option_price(
    symbol: str,
    strike_price: float,
    time_to_maturity_days: int,
    option_type: str = "call",
):
    if option_type not in ["call", "put"]:
        raise ValueError("option_type must be 'call' or 'put'")

    print("START CALCULATING HISTORICAL OPTION PRICE")
    print(f"SYMBOL: {symbol}")
    print(f"STRIKE PRICE: {strike_price}")
    print(f"TIME TO MATURITY: {time_to_maturity_days} (DAYS)")
    price_df = fetch_price(symbol, interval=f"{time_to_maturity_days}d")
    current_price = price_df["Close"].iloc[-1]
    percent_change_series = calc_percent_change(price_df)
    percent_strike_price = (strike_price - current_price) / current_price
    expected_payoff = price_option(
        percent_change_series, percent_strike_price, option_type
    )

    return expected_payoff * current_price


if __name__ == "__main__":
    print(historical_option_price("AAPL", 240, 1, "put"))
