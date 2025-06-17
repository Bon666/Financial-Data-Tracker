# Financial Data Tracker

📈 A Python-based project for tracking and visualizing global financial indicators such as stock prices, commodities, and indices using real-time data from Yahoo Finance.

## ✅ Features

- Pulls historical data using `yfinance`
- Analyzes:
  - S&P 500 (^GSPC)
  - AAPL (Apple Inc.)
  - GLD (Gold ETF)
- Plots:
  - Closing prices
  - Moving averages
  - Normalized trend comparison

## ▶️ How to Run

```bash
pip install -r requirements.txt
python financial_data_tracker.py
```

## 📂 Output

- `graphs/sp500.png`: S&P 500 with 30-day moving average
- `graphs/aapl.png`: Apple stock price with SMA
- `graphs/gld.png`: Gold ETF price
- `graphs/compare_normalized.png`: Normalized comparison of all assets

## 📊 Data Source

- Yahoo Finance via `yfinance` package
