import yfinance as yf
import pandas as pd


def fetch_price(symbol, period="1y", interval="1d") -> pd.DataFrame:
    ticker = yf.Ticker(symbol)
    data = ticker.history(period=period, interval=interval)
    return data


def fetch_price_range(symbol, start_date, end_date, interval="1d") -> pd.DataFrame:
    ticker = yf.Ticker(symbol)
    data = ticker.history(start=start_date, end=end_date, interval=interval)
    return data


def fetch_all_historical_data(symbol, interval="1d") -> pd.DataFrame:
    ticker = yf.Ticker(symbol)
    data = ticker.history(period="max", interval=interval)
    return data


if __name__ == "__main__":
    data = fetch_all_historical_data("AAPL")
    print(data)
