from fetch_price import fetch_price, fetch_price_timeframe
from calc_percent_change import calc_percent_change
from price_option import price_option
from risk_free_rate import apply_risk_free_rate


def historical_option_price(
    symbol: str,
    strike_price: float,
    time_to_maturity_days: int,
    option_type: str = "call",
    timeframe: str = None,
):
    if option_type not in ["call", "put"]:
        raise ValueError("option_type must be 'call' or 'put'")

    print("START CALCULATING HISTORICAL OPTION PRICE")
    print(f"SYMBOL: {symbol}")
    print(f"STRIKE PRICE: {strike_price}")
    print(f"TIME TO MATURITY: {time_to_maturity_days} (DAYS)")
    print(f"OPTION TYPE: {option_type}")
    if timeframe:
        print(f"TIME FRAME: {timeframe}")
        price_df = fetch_price_timeframe(symbol, timeframe)
    else:
        price_df = fetch_price(symbol)

    current_price = price_df["Close"].iloc[-1]
    percent_change_series = calc_percent_change(price_df)
    percent_strike_price = (strike_price - current_price) / current_price
    expected_payoff = price_option(
        percent_change_series, percent_strike_price, option_type
    )
    option_fair_price = apply_risk_free_rate(
        expected_payoff * current_price, time_to_maturity_days
    )

    return option_fair_price


if __name__ == "__main__":
    print(historical_option_price("AAPL", 270, 1, "call"))
