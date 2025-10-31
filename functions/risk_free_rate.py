import yfinance as yf


def fetch_risk_free_rate() -> float:
    """Fetch 3-month Treasury bill yield from Yahoo Finance"""
    ticker = yf.Ticker("^IRX")  # 3-month Treasury bill
    data = ticker.history(period="1d")
    return data["Close"].iloc[-1] / 100  # Convert percentage to decimal


def apply_risk_free_rate(
    price: float, days: int, risk_free_rate: float = None
) -> float:
    if risk_free_rate is None:
        risk_free_rate = fetch_risk_free_rate()
    yield_to_maturity = price * risk_free_rate * (days / 365)
    return price - yield_to_maturity
