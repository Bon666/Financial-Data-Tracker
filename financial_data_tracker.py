import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Create output folder
os.makedirs("graphs", exist_ok=True)

# Define tickers
tickers = {
    "S&P 500": "^GSPC",
    "AAPL": "AAPL",
    "Gold ETF": "GLD"
}

# Download data
data = {}
for name, symbol in tickers.items():
    df = yf.download(symbol, start="2022-01-01", end="2024-12-31")
    df["30d_SMA"] = df["Close"].rolling(window=30).mean()
    data[name] = df

    # Plot with moving average
    plt.figure(figsize=(10, 5))
    plt.plot(df.index, df["Close"], label="Close Price")
    plt.plot(df.index, df["30d_SMA"], label="30-Day SMA", linestyle="--")
    plt.title(f"{name} Price Trend")
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"graphs/{symbol.lower().replace('^','')}.png")
    plt.close()

# Normalize prices for comparison
norm_df = pd.DataFrame()
for name, df in data.items():
    norm_df[name] = df["Close"] / df["Close"].iloc[0]

# Plot normalized comparison
plt.figure(figsize=(12, 6))
for column in norm_df.columns:
    plt.plot(norm_df.index, norm_df[column], label=column)
plt.title("Normalized Price Comparison")
plt.xlabel("Date")
plt.ylabel("Normalized Price (Base = 1.0)")
plt.legend()
plt.tight_layout()
plt.savefig("graphs/compare_normalized.png")
plt.close()
