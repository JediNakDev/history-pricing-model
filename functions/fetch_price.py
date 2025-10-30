import yfinance as yf
import pandas as pd


def fetch_price(symbol, interval="1d") -> pd.DataFrame:
    print("START FETCHING PRICE")
    ticker = yf.Ticker(symbol)
    data = ticker.history(period="max", interval=interval)
    return data


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    
    data = fetch_price("AAPL")
    print(data)
    
    # Line chart using matplotlib
    plt.figure(figsize=(12, 8))
    plt.subplot(2, 1, 1)
    plt.plot(data.index, data['Close'], label='Close Price', linewidth=1)
    plt.title('AAPL Stock Price - Line Chart')
    plt.xlabel('Date')
    plt.ylabel('Price ($)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Volume chart
    plt.subplot(2, 1, 2)
    plt.bar(data.index, data['Volume'], alpha=0.7, color='orange')
    plt.title('AAPL Trading Volume')
    plt.xlabel('Date')
    plt.ylabel('Volume')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    # Candlestick chart using plotly
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.1,
        subplot_titles=('AAPL Candlestick Chart', 'Volume'),
        row_width=[0.2, 0.7]
    )
    
    # Add candlestick
    fig.add_trace(
        go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name='AAPL'
        ),
        row=1, col=1
    )
    
    # Add volume
    fig.add_trace(
        go.Bar(x=data.index, y=data['Volume'], name='Volume', marker_color='orange'),
        row=2, col=1
    )
    
    fig.update_layout(
        title='AAPL Stock Analysis',
        yaxis_title='Price ($)',
        xaxis_rangeslider_visible=False,
        height=800
    )
    
    fig.show()
