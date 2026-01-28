# Financial Data Tracker (Advanced)

A production-style financial data tracker that:
- pulls multi-asset market data from Yahoo Finance
- computes key performance & risk metrics
- generates reusable outputs (CSV + charts + interactive HTML report)

## What it tracks
Default tickers include:
- US equities: SPY, QQQ
- Bonds: TLT
- Gold/Oil: GLD, USO
- Global equities: EFA, EEM
- Crypto: BTC-USD (optional)

## Run
```bash
pip install -r requirements.txt
python main.py --years 3
