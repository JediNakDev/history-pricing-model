from numpy import e
import yfinance as yf


def fetch_risk_free_rate() -> float:
    ticker = yf.Ticker("^IRX")  # 3-month Treasury bill
    data = ticker.history(period="1d")
    return data["Close"].iloc[-1] / 100  # Convert percentage to decimal


def apply_risk_free_rate(
    price: float, days: int, risk_free_rate: float = None
) -> float:
    time_in_years = days / 365
    if risk_free_rate is None:
        risk_free_rate = fetch_risk_free_rate()
    return price * e ** (-risk_free_rate * time_in_years)
