import yfinance as yf
import pandas as pd


def fetch_price(symbol, interval="1d") -> pd.DataFrame:
    ticker = yf.Ticker(symbol)
    data = ticker.history(period="max", interval=interval)
    return data


if __name__ == "__main__":
    data = fetch_price("AAPL")
    print(data)
