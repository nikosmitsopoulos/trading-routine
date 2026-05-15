# Trading Strategy — Bull

**Last reviewed:** 2026-05-15
**Owner:** Nikos Mits
**Status:** v1.0 — paper trading

---

## Philosophy

Fundamentals-driven swing trading. We bet on **good businesses at reasonable prices** that have a **near-term catalyst** (earnings, product launch, sector tailwind, analyst upgrades).

We do **not** chase momentum, meme stocks, or technical patterns. We do not day-trade.

## Universe

- **US equities only** (NYSE, NASDAQ).
- Market cap ≥ **$2B** (no micro-caps).
- Average daily volume ≥ **500k shares** (liquidity).
- Price ≥ **$5** (no penny stocks).
- Sector focus: **Tech, Healthcare, Consumer, Financials, Industrials.** Avoid energy/materials unless strong catalyst.

## Buy signals (need at least 2 of these to enter)

1. **Earnings beat** in last quarter with raised guidance.
2. **Analyst upgrades** from 2+ major firms within last 30 days.
3. **Positive catalyst news** (product launch, acquisition, regulatory win, sector tailwind).
4. **Reasonable valuation** — P/E below sector median OR PEG < 1.5.
5. **Strong fundamentals** — revenue growth >10% YoY, positive free cash flow, debt/equity < 1.

## Sell signals (any one triggers exit)

1. **Stop-loss hit: -7%** from entry → immediate sell, no questions.
2. **Trailing stop: -10%** from peak, once position is +15% → sell.
3. **Thesis broken** — original buy reason no longer holds (e.g., guidance cut, key exec leaves).
4. **Better opportunity** — if at max positions and a clearly stronger setup appears, rotate.
5. **Position +30%** — sell HALF, let the rest ride with trailing stop.

## Position sizing

- **5% max per position** on entry.
- New positions sized based on conviction:
  - High conviction (4+ buy signals): 5%
  - Medium conviction (3 signals): 3.5%
  - Low conviction (2 signals): 2%
- Never average down a loser. If a position is red, the next move is sell, not buy more.

## Risk management

- **Daily loss cap: 3% of portfolio.** If breached, stop trading until next day.
- **Weekly loss cap: 7%.** If breached, no new positions until weekly review.
- **Max 15 positions** open at once.
- **Min 10% cash reserve** always.
- **Max 25% in any single sector.**

## Benchmark

Compare daily and weekly to **SPY** (S&P 500 ETF). Goal: beat SPY by 5%+ over rolling 6 months.

## Trade journal requirements

Every trade logged in `trade_log.md` must include:
- Date, ticker, action (buy/sell), shares, price, total value.
- **Rationale** (which buy/sell signals triggered).
- **Conviction level** (low/medium/high).
- **Exit plan** (stop-loss price, target price, max hold time).

## Weekly review checklist (Fridays 4pm)

1. Compare portfolio return vs SPY for the week.
2. Review every closed trade — was the thesis right?
3. Review every open position — does the thesis still hold?
4. Update `lessons.md` with anything new.
5. Adjust this strategy file if a pattern emerges (but only ONE change per week max — don't overfit).

## Things this strategy does NOT do

- Day trading / scalping
- Options, futures, FX, crypto
- Short selling
- Leverage / margin
- Earnings plays (buying day before earnings) — too risky
- Penny stocks, OTC, meme stocks

## Notes from Nikos

_(Use this section for personal preferences, restrictions, or insights you want the bot to remember.)_

- Prefer companies with products I actually understand or use.
- Avoid tobacco, gambling, and weapons stocks.
- This is an experiment, not retirement money. Be conservative but not paralyzed.
