from fetch_price import fetch_price, fetch_price_timeframe
from calc_percent_change import calc_percent_change
from price_option import price_option
from risk_free_rate import apply_risk_free_rate
import pandas as pd


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
    percent_change_series = calc_percent_change(price_df, time_to_maturity_days)
    price_at_maturity = current_price * percent_change_series
    expected_payoff = price_option(price_at_maturity, strike_price, option_type)
    option_fair_price = apply_risk_free_rate(expected_payoff, time_to_maturity_days)

    return option_fair_price


def batch_historical_option_price(
    symbol: str,
    strike_prices: list[float],
    time_to_maturity_days: list[int],
    timeframe: str = None,
):
    print("START CALCULATING BATCH HISTORICAL OPTION PRICES")
    print(f"SYMBOL: {symbol}")
    print(f"STRIKE PRICES: {strike_prices}")
    print(f"TIME TO MATURITY: {time_to_maturity_days} (DAYS)")
    if timeframe:
        print(f"TIME FRAME: {timeframe}")
        price_df = fetch_price_timeframe(symbol, timeframe)
    else:
        price_df = fetch_price(symbol)

    current_price = price_df["Close"].iloc[-1]

    call_prices = pd.DataFrame(index=time_to_maturity_days, columns=strike_prices)
    put_prices = pd.DataFrame(index=time_to_maturity_days, columns=strike_prices)

    # Calculate option prices for each combination
    for days in time_to_maturity_days:
        print(f"\nProcessing time to maturity: {days} days")
        percent_change_series = calc_percent_change(price_df, days)
        price_at_maturity = current_price * percent_change_series

        for strike in strike_prices:
            expected_payoff_call = price_option(price_at_maturity, strike, "call")
            option_fair_price_call = apply_risk_free_rate(expected_payoff_call, days)
            call_prices.loc[days, strike] = option_fair_price_call

            expected_payoff_put = price_option(price_at_maturity, strike, "put")
            option_fair_price_put = apply_risk_free_rate(expected_payoff_put, days)
            put_prices.loc[days, strike] = option_fair_price_put

    # Set index and column names
    call_prices.index.name = "Time to Maturity (Days)"
    call_prices.columns.name = "Strike Price"
    put_prices.index.name = "Time to Maturity (Days)"
    put_prices.columns.name = "Strike Price"

    return call_prices, put_prices


if __name__ == "__main__":
    # Test single option price
    print(historical_option_price("AAPL", 270, 1, "call"))

    # Test batch option pricing
    print("\n" + "=" * 80)
    print("BATCH OPTION PRICING TEST")
    print("=" * 80)

    strike_prices = [250, 260, 270, 280, 290]
    time_to_maturity_days = [1, 7, 14, 30, 60]

    call_df, put_df = batch_historical_option_price(
        symbol="AAPL",
        strike_prices=strike_prices,
        time_to_maturity_days=time_to_maturity_days,
    )

    print("\n" + "=" * 80)
    print("CALL OPTION PRICES")
    print("=" * 80)
    print(call_df)

    print("\n" + "=" * 80)
    print("PUT OPTION PRICES")
    print("=" * 80)
    print(put_df)
