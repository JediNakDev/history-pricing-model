import pandas as pd


def calc_percent_change(price_df: pd.DataFrame) -> pd.Series:
    print("START CALCULATING PERCENT CHANGE")
    return price_df["Close"].pct_change() * 100


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from fetch_price import fetch_price

    data = fetch_price("AAPL")
    percent_changes = calc_percent_change(data)
    print(percent_changes)

    # Plot distribution of percent changes
    plt.figure(figsize=(10, 6))
    plt.hist(percent_changes.dropna(), bins=50, alpha=0.7, edgecolor="black")
    plt.title("Distribution of Daily Percent Changes (AAPL)")
    plt.xlabel("Percent Change")
    plt.ylabel("Frequency")
    plt.grid(True, alpha=0.3)
    plt.show()
