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

_(Empty. Will grow over time.)_

## 2026-05-15 — Κρίσιμο: Λείπουν env vars, routine αδύνατη

**Observation:** Το EOD close routine (2026-05-15) απέτυχε να εκτελεστεί γιατί ΟΛΕΣ οι environment variables λείπουν: ALPACA_API_KEY, ALPACA_SECRET_KEY, ALPACA_BASE_URL, GMAIL_USER, GMAIL_APP_PASSWORD. Κανένα Alpaca script δεν τρέχει, κανένα email δεν εστάλη μέσω SMTP. Το Gmail MCP χρησιμοποιήθηκε ως fallback για να δημιουργηθεί draft ειδοποίησης.
**Lesson:** Πριν από οποιοδήποτε routine, πρέπει να υπάρχει validation των env vars. Χωρίς ALPACA_API_KEY τουλάχιστον, δεν έχει νόημα να ξεκινά κανένα trading routine. Ο Nikos πρέπει να διαμορφώσει τα env vars στο cloud routine environment.
**Applies to:** Πάντα — pre-market, open, midday, close, weekly review.
