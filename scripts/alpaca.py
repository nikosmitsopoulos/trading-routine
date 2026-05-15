"""
Alpaca API helper — paper trading.

Usage from bash:
    python scripts/alpaca.py account
    python scripts/alpaca.py positions
    python scripts/alpaca.py orders [open|closed|all]
    python scripts/alpaca.py news TICKER [TICKER ...]
    python scripts/alpaca.py quote TICKER
    python scripts/alpaca.py buy TICKER SHARES [limit_price]
    python scripts/alpaca.py sell TICKER SHARES [limit_price]
    python scripts/alpaca.py sell-all TICKER
    python scripts/alpaca.py cancel ORDER_ID
    python scripts/alpaca.py is-trading-day   # exit 0 if today is a US trading day, 1 otherwise
    python scripts/alpaca.py clock            # current market clock (open/closed, next open/close)

All credentials read from environment variables:
    ALPACA_API_KEY, ALPACA_SECRET_KEY, ALPACA_BASE_URL
"""

import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone


def _env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        print(f"ERROR: missing env var {name}", file=sys.stderr)
        sys.exit(2)
    return value


API_KEY = _env("ALPACA_API_KEY")
SECRET = _env("ALPACA_SECRET_KEY")
BASE = os.environ.get("ALPACA_BASE_URL", "https://paper-api.alpaca.markets").rstrip("/")
DATA_BASE = "https://data.alpaca.markets"

HEADERS = {
    "APCA-API-KEY-ID": API_KEY,
    "APCA-API-SECRET-KEY": SECRET,
    "Content-Type": "application/json",
}


def _request(method: str, url: str, body: dict | None = None) -> dict:
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, method=method, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read().decode()
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        msg = e.read().decode()
        print(f"HTTP {e.code} on {method} {url}: {msg}", file=sys.stderr)
        sys.exit(1)


def get_account() -> dict:
    return _request("GET", f"{BASE}/v2/account")


def get_positions() -> list:
    return _request("GET", f"{BASE}/v2/positions")


def get_orders(status: str = "open") -> list:
    qs = urllib.parse.urlencode({"status": status, "limit": 100})
    return _request("GET", f"{BASE}/v2/orders?{qs}")


def get_quote(ticker: str) -> dict:
    url = f"{DATA_BASE}/v2/stocks/{ticker.upper()}/quotes/latest"
    return _request("GET", url)


def get_news(tickers: list[str], limit: int = 20) -> dict:
    since = (datetime.now(timezone.utc) - timedelta(days=3)).isoformat()
    qs = urllib.parse.urlencode({
        "symbols": ",".join(t.upper() for t in tickers),
        "limit": limit,
        "start": since,
    })
    return _request("GET", f"{DATA_BASE}/v1beta1/news?{qs}")


def place_order(ticker: str, side: str, qty: float, limit_price: float | None = None) -> dict:
    body = {
        "symbol": ticker.upper(),
        "qty": str(qty),
        "side": side,
        "type": "limit" if limit_price else "market",
        "time_in_force": "day",
    }
    if limit_price:
        body["limit_price"] = str(limit_price)
    return _request("POST", f"{BASE}/v2/orders", body)


def close_position(ticker: str) -> dict:
    return _request("DELETE", f"{BASE}/v2/positions/{ticker.upper()}")


def cancel_order(order_id: str) -> dict:
    return _request("DELETE", f"{BASE}/v2/orders/{order_id}")


def get_clock() -> dict:
    return _request("GET", f"{BASE}/v2/clock")


def is_trading_day() -> bool:
    """True if today (US/Eastern) is a NYSE trading day. False on weekends and holidays."""
    today = datetime.now(timezone.utc).date().isoformat()
    cal = _request("GET", f"{BASE}/v2/calendar?start={today}&end={today}")
    return isinstance(cal, list) and len(cal) > 0


def _print(obj):
    print(json.dumps(obj, indent=2, default=str))


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(0)

    cmd = args[0]

    if cmd == "account":
        _print(get_account())
    elif cmd == "positions":
        _print(get_positions())
    elif cmd == "orders":
        status = args[1] if len(args) > 1 else "open"
        _print(get_orders(status))
    elif cmd == "quote":
        _print(get_quote(args[1]))
    elif cmd == "news":
        _print(get_news(args[1:]))
    elif cmd in ("buy", "sell"):
        ticker = args[1]
        qty = float(args[2])
        limit = float(args[3]) if len(args) > 3 else None
        _print(place_order(ticker, cmd, qty, limit))
    elif cmd == "sell-all":
        _print(close_position(args[1]))
    elif cmd == "cancel":
        _print(cancel_order(args[1]))
    elif cmd == "clock":
        _print(get_clock())
    elif cmd == "is-trading-day":
        if is_trading_day():
            print("yes")
            sys.exit(0)
        else:
            print("no")
            sys.exit(1)
    else:
        print(f"Unknown command: {cmd}", file=sys.stderr)
        print(__doc__)
        sys.exit(2)


if __name__ == "__main__":
    main()
