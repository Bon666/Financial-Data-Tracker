
---

## `main.py`（完整高级版，直接可跑）
```python
import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import yfinance as yf
import plotly.express as px


# -----------------------------
# Helpers
# -----------------------------
def ensure_dirs():
    out_dir = Path("outputs")
    data_dir = Path("data")
    out_dir.mkdir(exist_ok=True)
    data_dir.mkdir(exist_ok=True)
    return out_dir, data_dir


def fetch_prices(tickers, years, data_dir):
    tickers = [t.upper() for t in tickers]
    cache = data_dir / f"tracker_prices_{'-'.join(tickers)}_{years}y.csv"

    if cache.exists():
        return pd.read_csv(cache, parse_dates=["Date"]).set_index("Date")

    df = yf.download(tickers, period=f"{years}y", auto_adjust=True, progress=False)["Close"]
    df.index.name = "Date"
    df.to_csv(cache)
    return df


def compute_metrics(prices: pd.DataFrame) -> pd.DataFrame:
    """
    Returns a summary table with performance & risk metrics (annualized).
    """
    rets = prices.pct_change().dropna()

    ann_return = rets.mean() * 252
    ann_vol = rets.std() * np.sqrt(252)
    sharpe = ann_return / ann_vol.replace(0, np.nan)

    # Max drawdown
    cum = (1 + rets).cumprod()
    peak = cum.cummax()
    drawdown = (cum / peak) - 1
    max_dd = drawdown.min()

    out = pd.DataFrame({
        "ann_return": ann_return,
        "ann_vol": ann_vol,
        "sharpe": sharpe,
        "max_drawdown": max_dd
    }).dropna()

    return out


def normalized(prices: pd.DataFrame) -> pd.DataFrame:
    return prices / prices.iloc[0]


def build_html_report(out_dir: Path, figures: list, title: str = "Financial Data Tracker Report"):
    parts = [f"<h1>{title}</h1>", "<p>Auto-generated market tracking report (interactive).</p>"]
    for fig in figures:
        parts.append(fig.to_html(full_html=False, include_plotlyjs="cdn"))
    html = "\n".join(parts)
    report_path = out_dir / "report.html"
    report_path.write_text(html, encoding="utf-8")
    print(f"Saved: {report_path}")


# -----------------------------
# Main
# -----------------------------
def main():
    parser = argparse.ArgumentParser(description="Financial Data Tracker (Advanced)")
    parser.add_argument("--years", type=int, default=3)
    parser.add_argument(
        "--tickers",
        nargs="+",
        default=["SPY", "QQQ", "TLT", "GLD", "USO", "EFA", "EEM"],
        help="Tickers to track (ETFs/indices/crypto)"
    )
    args = parser.parse_args()

    out_dir, data_dir = ensure_dirs()

    prices = fetch_prices(args.tickers, args.years, data_dir).dropna()
    if prices.empty:
        raise RuntimeError("No data returned. Check tickers or internet connection.")

    # Compute metrics
    metrics = compute_metrics(prices)
    metrics_path = out_dir / "summary_metrics.csv"
    metrics.to_csv(metrics_path)
    print(f"Saved: {metrics_path}")

    # Align prices to only valid tickers (in case some got dropped)
    prices = prices[metrics.index]

    # Figures
    norm = normalized(prices)
    fig_perf = px.line(
        norm,
        title="Normalized Performance (Start = 1.0)",
        labels={"value": "Normalized Price", "Date": "Date"}
    )
    fig_perf.write_html(out_dir / "normalized_performance.html")

    corr = prices.pct_change().dropna().corr()
    fig_corr = px.imshow(
        corr,
        color_continuous_scale="RdBu",
        zmin=-1, zmax=1,
        title="Return Correlation Heatmap"
    )
    fig_corr.write_html(out_dir / "correlation_heatmap.html")

    # Drawdown
    rets = prices.pct_change().dropna()
    cum = (1 + rets).cumprod()
    dd = (cum / cum.cummax()) - 1
    fig_dd = px.line(
        dd,
        title="Drawdown (by Asset)",
        labels={"value": "Drawdown", "Date": "Date"}
    )
    fig_dd.write_html(out_dir / "drawdown_chart.html")

    # Summary table (for report)
    metrics_display = metrics.copy().reset_index().rename(columns={"index": "asset"})
    fig_table = px.scatter(
        metrics_display,
        x="ann_vol",
        y="ann_return",
        size="sharpe",
        hover_name="asset",
        title="Risk–Return Map (Size = Sharpe)"
    )

    # One combined report.html
    build_html_report(
        out_dir=out_dir,
        figures=[fig_perf, fig_corr, fig_dd, fig_table],
        title="Financial Data Tracker Report"
    )

    print("Done. Open outputs/report.html to view the dashboard.")


if __name__ == "__main__":
    main()
