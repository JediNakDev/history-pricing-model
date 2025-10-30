import pandas as pd


def calc_percent_change(price_df: pd.DataFrame) -> pd.Series:
    return price_df["Close"].pct_change() * 100


if __name__ == "__main__":
    from fetch_price import fetch_price

    data = fetch_price("AAPL")
    print(calc_percent_change(data))
