from fetch_price import fetch_price
from calc_percent_change import calc_percent_change
from price_option import price_option


def historical_call_option_premium(
    symbol: str, strike_price: float, time_to_maturity_days: int
):
    print("START CALCULATING HISTORICAL OPTION PRICE")
    print(f"SYMBOL: {symbol}")
    print(f"STRIKE PRICE: {strike_price}")
    print(f"TIME TO MATURITY: {time_to_maturity_days} (DAYS)")
    price_df = fetch_price(symbol, interval=f"{time_to_maturity_days}d")
    current_price = price_df["Close"].iloc[-1]
    percent_change_series = calc_percent_change(price_df)
    percent_strike_price = (strike_price - current_price) / current_price
    option_price = (
        price_option(percent_change_series, percent_strike_price) * current_price
    )

    return option_price


if __name__ == "__main__":
    print(historical_call_option_premium("AAPL", 270, 1))
