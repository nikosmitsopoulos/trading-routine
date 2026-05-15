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

## 2026-05-15 — Close routine aborted: no API credentials in environment

**Observation:** Market-close routine fired but every external dependency failed:
- `ALPACA_API_KEY` / `ALPACA_SECRET_KEY` not set → cannot read account, positions, or orders.
- `GMAIL_USER` / `GMAIL_APP_PASSWORD` not set → cannot send the daily report email.
- `yfinance` (SPY benchmark) blocked by network allowlist: `HTTP 403: Host not in allowlist`.

No trading data could be gathered, no numbers computed, no email delivered. Portfolio snapshot left unchanged (still at the $100k starting state — no live state to overwrite it with).

**Lesson:** Before any routine can do useful work, the cloud session must be configured with: (1) the four Alpaca + Gmail secrets injected as env vars, and (2) `query2.finance.yahoo.com` (and any other yfinance hosts) added to the outbound network allowlist. Until both are in place, the close routine is a no-op and Nikos won't get the daily checkpoint email. Suggest a one-time health-check step at the top of every routine that verifies env vars + a trivial Alpaca ping, and bails loudly if either fails.
**Applies to:** Always (every routine).
