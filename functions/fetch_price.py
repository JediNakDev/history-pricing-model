import yfinance as yf
import pandas as pd
from datetime import datetime


def fetch_price(symbol, interval="1d") -> pd.DataFrame:
    print(f"START FETCHING {symbol} PRICE FOR MAXIMUM TIMEFRAME")
    ticker = yf.Ticker(symbol)
    data = ticker.history(period="max", interval=interval)
    return data


def fetch_price_timeframe(
    symbol: str, timeframe: str, interval: str = "1d"
) -> pd.DataFrame:
    """
    timeframe: Time period ('1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max')
    interval: Data interval ('1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo')
    """
    print(f"START FETCHING {symbol} PRICE FOR {timeframe} TIMEFRAME")
    ticker = yf.Ticker(symbol)
    data = ticker.history(period=timeframe, interval=interval)
    return data


def fetch_option_price(symbol: str) -> tuple[pd.DataFrame, pd.DataFrame, list, list]:
    print(f"START FETCHING OPTION PRICES FOR {symbol}")

    ticker = yf.Ticker(symbol)

    # Get all available expiration dates
    expirations = ticker.options

    if not expirations:
        print(f"No options available for {symbol}")
        return pd.DataFrame(), pd.DataFrame(), [], []

    print(f"Found {len(expirations)} expiration dates")

    # Dictionaries to store option data
    call_option_data = {}
    put_option_data = {}
    time_to_maturity_list = []

    # Fetch option chain for each expiration date
    for expiration in expirations:
        try:
            # Get option chain for this expiration
            opt_chain = ticker.option_chain(expiration)

            calls = opt_chain.calls
            puts = opt_chain.puts

            if calls.empty and puts.empty:
                continue

            # Calculate time to maturity in days
            exp_date = datetime.strptime(expiration, "%Y-%m-%d")
            today = datetime.now()
            days_to_maturity = (exp_date - today).days

            # Skip if already expired
            if days_to_maturity < 0:
                continue

            time_to_maturity_list.append(days_to_maturity)

            # Process CALL options
            call_strikes_prices = {}
            if not calls.empty:
                for _, row in calls.iterrows():
                    strike = row["strike"]
                    # Use mid price between bid and ask, fallback to lastPrice if bid/ask not available
                    if pd.notna(row.get("bid")) and pd.notna(row.get("ask")):
                        option_price = (row["bid"] + row["ask"]) / 2
                    elif pd.notna(row.get("lastPrice")):
                        option_price = row["lastPrice"]
                    else:
                        continue

                    call_strikes_prices[strike] = option_price

            if call_strikes_prices:
                call_option_data[days_to_maturity] = call_strikes_prices

            # Process PUT options
            put_strikes_prices = {}
            if not puts.empty:
                for _, row in puts.iterrows():
                    strike = row["strike"]
                    # Use mid price between bid and ask, fallback to lastPrice if bid/ask not available
                    if pd.notna(row.get("bid")) and pd.notna(row.get("ask")):
                        option_price = (row["bid"] + row["ask"]) / 2
                    elif pd.notna(row.get("lastPrice")):
                        option_price = row["lastPrice"]
                    else:
                        continue

                    put_strikes_prices[strike] = option_price

            if put_strikes_prices:
                put_option_data[days_to_maturity] = put_strikes_prices

            print(
                f"Fetched {len(call_strikes_prices)} call strikes and {len(put_strikes_prices)} put strikes for {expiration} ({days_to_maturity} days)"
            )

        except Exception as e:
            print(f"Error fetching options for {expiration}: {str(e)}")
            continue

    if not call_option_data and not put_option_data:
        print(f"No valid option data found for {symbol}")
        return pd.DataFrame(), pd.DataFrame(), [], []

    # Create DataFrames from the dictionaries
    call_df = pd.DataFrame(call_option_data).T
    put_df = pd.DataFrame(put_option_data).T

    # Get all unique strike prices from both calls and puts
    all_strikes = set()
    if not call_df.empty:
        all_strikes.update(call_df.columns)
    if not put_df.empty:
        all_strikes.update(put_df.columns)

    strike_prices = sorted(list(all_strikes))

    # Sort columns (strike prices) in ascending order and ensure both have same columns
    call_df = call_df.reindex(sorted(call_df.columns), axis=1)
    put_df = put_df.reindex(sorted(put_df.columns), axis=1)

    # Sort rows (time to maturity) in ascending order
    if not call_df.empty:
        call_df = call_df.sort_index()
    if not put_df.empty:
        put_df = put_df.sort_index()

    # Sort time to maturity list
    time_to_maturity_list = sorted(list(set(time_to_maturity_list)))

    print("Successfully created option price matrices:")
    print(f"  Calls: {call_df.shape[0]} expirations x {call_df.shape[1]} strikes")
    print(f"  Puts: {put_df.shape[0]} expirations x {put_df.shape[1]} strikes")
    print(f"  Total unique strikes: {len(strike_prices)}")
    print(
        f"  Time to maturity range: {min(time_to_maturity_list)} to {max(time_to_maturity_list)} days"
    )

    return call_df, put_df, strike_prices, time_to_maturity_list


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    # Example 1: Fetch historical price data
    data = fetch_price("AAPL")
    print(data)

    # Example 2: Fetch option prices
    print("\n" + "=" * 80)
    print("FETCHING OPTION PRICES")
    print("=" * 80 + "\n")
    call_df, put_df, strike_prices, time_to_maturity = fetch_option_price("AAPL")

    print("\n" + "-" * 80)
    print("CALL OPTIONS DataFrame:")
    print("-" * 80)
    print(call_df)
    print(f"\nShape: {call_df.shape}")

    print("\n" + "-" * 80)
    print("PUT OPTIONS DataFrame:")
    print("-" * 80)
    print(put_df)
    print(f"\nShape: {put_df.shape}")

    print("\n" + "-" * 80)
    print("Strike Prices (first 10):")
    print("-" * 80)
    print(strike_prices[:10])

    print("\n" + "-" * 80)
    print("Time to Maturity (days, first 10):")
    print("-" * 80)
    print(time_to_maturity[:10])

    # Example: Access a specific option price
    if not call_df.empty and len(time_to_maturity) > 0 and len(strike_prices) > 0:
        ttm = time_to_maturity[0]
        strike = strike_prices[len(strike_prices) // 2]  # Get middle strike
        if ttm in call_df.index and strike in call_df.columns:
            print(
                f"\nExample: Call option with {ttm} days to maturity and strike ${strike}: ${call_df.loc[ttm, strike]:.2f}"
            )

    # Line chart using matplotlib
    plt.figure(figsize=(12, 8))
    plt.subplot(2, 1, 1)
    plt.plot(data.index, data["Close"], label="Close Price", linewidth=1)
    plt.title("AAPL Stock Price - Line Chart")
    plt.xlabel("Date")
    plt.ylabel("Price ($)")
    plt.legend()
    plt.grid(True, alpha=0.3)

    # Volume chart
    plt.subplot(2, 1, 2)
    plt.bar(data.index, data["Volume"], alpha=0.7, color="orange")
    plt.title("AAPL Trading Volume")
    plt.xlabel("Date")
    plt.ylabel("Volume")
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()

    # Candlestick chart using plotly
    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.1,
        subplot_titles=("AAPL Candlestick Chart", "Volume"),
        row_width=[0.2, 0.7],
    )

    # Add candlestick
    fig.add_trace(
        go.Candlestick(
            x=data.index,
            open=data["Open"],
            high=data["High"],
            low=data["Low"],
            close=data["Close"],
            name="AAPL",
        ),
        row=1,
        col=1,
    )

    # Add volume
    fig.add_trace(
        go.Bar(x=data.index, y=data["Volume"], name="Volume", marker_color="orange"),
        row=2,
        col=1,
    )

    fig.update_layout(
        title="AAPL Stock Analysis",
        yaxis_title="Price ($)",
        xaxis_rangeslider_visible=False,
        height=800,
    )

    fig.show()
