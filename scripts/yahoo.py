"""
Yahoo Finance helper — fundamentals + historical prices.

Usage:
    python scripts/yahoo.py fundamentals TICKER
    python scripts/yahoo.py prices TICKER [days]
    python scripts/yahoo.py compare TICKER [TICKER ...]   # vs SPY
    python scripts/yahoo.py spy [days]

No API key needed. Uses yfinance library.
"""

import json
import sys

try:
    import yfinance as yf
except ImportError:
    print("ERROR: yfinance not installed. Run: pip install yfinance", file=sys.stderr)
    sys.exit(2)


def fundamentals(ticker: str) -> dict:
    t = yf.Ticker(ticker.upper())
    info = t.info
    keys = [
        "shortName", "sector", "industry", "marketCap", "trailingPE", "forwardPE",
        "pegRatio", "priceToBook", "trailingEps", "forwardEps", "revenueGrowth",
        "earningsGrowth", "profitMargins", "operatingMargins", "returnOnEquity",
        "debtToEquity", "freeCashflow", "totalCash", "totalDebt", "currentPrice",
        "targetMeanPrice", "recommendationKey", "numberOfAnalystOpinions",
        "fiftyTwoWeekHigh", "fiftyTwoWeekLow", "fiftyDayAverage",
        "twoHundredDayAverage", "averageVolume", "beta",
    ]
    return {k: info.get(k) for k in keys}


def prices(ticker: str, days: int = 30) -> dict:
    t = yf.Ticker(ticker.upper())
    hist = t.history(period=f"{days}d")
    if hist.empty:
        return {"error": f"No data for {ticker}"}
    return {
        "ticker": ticker.upper(),
        "days": days,
        "first_close": float(hist["Close"].iloc[0]),
        "last_close": float(hist["Close"].iloc[-1]),
        "high": float(hist["High"].max()),
        "low": float(hist["Low"].min()),
        "return_pct": round(
            (float(hist["Close"].iloc[-1]) / float(hist["Close"].iloc[0]) - 1) * 100, 2
        ),
        "avg_volume": int(hist["Volume"].mean()),
    }


def compare(tickers: list[str], days: int = 30) -> dict:
    tickers = [t.upper() for t in tickers] + ["SPY"]
    out = {}
    for t in tickers:
        out[t] = prices(t, days)
    return out


def spy_perf(days: int = 30) -> dict:
    return prices("SPY", days)


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(0)

    cmd = args[0]

    if cmd == "fundamentals":
        print(json.dumps(fundamentals(args[1]), indent=2, default=str))
    elif cmd == "prices":
        days = int(args[2]) if len(args) > 2 else 30
        print(json.dumps(prices(args[1], days), indent=2, default=str))
    elif cmd == "compare":
        days = 30
        tickers = args[1:]
        print(json.dumps(compare(tickers, days), indent=2, default=str))
    elif cmd == "spy":
        days = int(args[1]) if len(args) > 1 else 30
        print(json.dumps(spy_perf(days), indent=2, default=str))
    else:
        print(f"Unknown command: {cmd}", file=sys.stderr)
        print(__doc__)
        sys.exit(2)


if __name__ == "__main__":
    main()
