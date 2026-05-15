# Lessons Learned

Curated insights from past trades and routines. The agent's evolving wisdom.

**Rule:** Only add entries that are **actionable** and **non-obvious**. Don't write "always do research" — that's already in the strategy. Write things like "after FOMC meetings, wait 24h before entering new positions — false moves are common."

Format:
```
## YYYY-MM-DD — Short title

**Observation:** What happened.
**Lesson:** What to do differently next time.
**Applies to:** Pre-market / open / midday / close / always.
```

Review during weekly review. Prune redundant entries.

---

## 2026-05-15 — Routine aborted: missing env vars on day 1

**Observation:** The close routine ran but ALPACA_API_KEY (and likely ALPACA_SECRET_KEY, ALPACA_BASE_URL, GMAIL_USER, GMAIL_APP_PASSWORD) were not set in the cloud execution environment. Both `scripts/alpaca.py` and `scripts/email_report.py` exited with error code 2 immediately. Yahoo Finance (yfinance) also returned HTTP 403 (host not in allowlist). The Gmail SMTP email could not be sent; a draft was created via Gmail MCP instead.

**Lesson:** Before any routine can operate, the five required env vars must be present in the cloud routine's environment configuration: ALPACA_API_KEY, ALPACA_SECRET_KEY, ALPACA_BASE_URL, GMAIL_USER, GMAIL_APP_PASSWORD. Nikos must set these in the cloud scheduler (e.g., GitHub Actions secrets, GCP Cloud Run env, etc.) before the bot can trade or report. Check for missing vars at the very start of every routine and fail fast with a clear alert.

**Applies to:** Always — pre-market, open, midday, close, weekly review.

---

_(Empty. Will grow over time.)_
