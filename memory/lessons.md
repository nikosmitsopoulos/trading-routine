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

## 2026-05-15 — Routine αποτυχία: λείπουν env vars και network access

**Observation:** Το close routine εκτελέστηκε αλλά δεν μπόρεσε να ολοκληρωθεί. Λείπουν τα env vars `ALPACA_API_KEY`, `ALPACA_SECRET_KEY`, `GMAIL_USER`, `GMAIL_APP_PASSWORD`. Επίσης, το Yahoo Finance (yfinance) έδωσε HTTP 403 — το outbound network policy του cloud environment δεν επιτρέπει πρόσβαση στα external APIs (Alpaca, Yahoo Finance).

**Lesson:** Πριν από οποιαδήποτε trading ενέργεια, ο Nikos πρέπει να ρυθμίσει τα environment variables στο cloud routine: `ALPACA_API_KEY`, `ALPACA_SECRET_KEY`, `ALPACA_BASE_URL`, `GMAIL_USER`, `GMAIL_APP_PASSWORD`. Επίσης, το network policy του environment πρέπει να επιτρέπει πρόσβαση στο `paper-api.alpaca.markets` και `query1.finance.yahoo.com`.

**Applies to:** Όλα τα routines (pre-market, open, midday, close, weekly review).
