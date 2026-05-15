# 🐂 Bull — 24/7 AI Trading Agent

Autonomous paper-trading agent powered by Claude Code routines on Opus 4.7. Trades US equities via Alpaca API. Goal: beat the S&P 500.

## Architecture

- **Brain:** Claude Code routines (cloud-scheduled cron jobs).
- **Broker:** Alpaca paper trading.
- **Data:** Alpaca news API + Yahoo Finance + Claude WebSearch.
- **Notifications:** Email via Gmail SMTP.
- **Memory:** Markdown files in `memory/` — committed to git after every run.

## Schedule (3 routines/day max)

All routines start with a holiday/trading-day check via Alpaca calendar API. On non-trading days they exit immediately (zero tokens).

| Routine | Time ET | Time Greece | What it does |
|---|---|---|---|
| **Daily** | 10:00 Mon–Fri | 17:00 | Defensive pass on positions → research → execute new buys → update portfolio |
| **Close** | 16:15 Mon–Fri | 23:15 | EOD summary email + journal lessons |
| **Weekly Review** | 16:30 Friday | 23:30 | Grade the week, adjust strategy if pattern emerges |

**Run count:** ~11 runs/week (vs 26 in the original 5-routine design).

## Repo layout

```
trading-routine/
├── CLAUDE.md                # Agent's main instructions & rules
├── README.md                # This file
├── requirements.txt         # Python deps
├── .gitignore
├── memory/                  # Persistent state (read & written every routine)
│   ├── strategy.md
│   ├── portfolio.md
│   ├── trade_log.md
│   ├── research_log.md
│   ├── watchlist.md
│   └── lessons.md
├── routines/                # Prompts for each scheduled run
│   ├── daily.md             # Mon–Fri 10:00 ET (combined research + trades + defense)
│   ├── close.md             # Mon–Fri 16:15 ET (EOD report)
│   └── weekly-review.md     # Friday 16:30 ET (weekly reflection)
└── scripts/                 # Helper utilities
    ├── alpaca.py            # Alpaca REST API wrapper
    ├── yahoo.py             # Yahoo Finance fundamentals
    └── email_report.py      # Gmail SMTP email sender
```

## Required environment variables

All credentials live in the **cloud routine environment**, never in this repo.

```
ALPACA_API_KEY
ALPACA_SECRET_KEY
ALPACA_BASE_URL       # https://paper-api.alpaca.markets for paper
GMAIL_USER
GMAIL_APP_PASSWORD
```

## Setup checklist

1. ✅ Alpaca paper account created
2. ✅ Gmail App Password generated
3. ⬜ GitHub repo created and pushed
4. ⬜ Claude Desktop "Trading" cloud environment with env vars set
5. ⬜ 5 routines created and pointed at this repo
6. ⬜ "Allow unrestricted branch pushes" enabled on each routine
7. ⬜ First test runs successful

## Safety

- **Paper trading only** — no real money.
- Hard rules in CLAUDE.md prevent options, leverage, crypto, penny stocks.
- Daily loss cap (3%), per-position cap (5%), sector cap (25%).
- Memory committed to git after every run for full audit trail.
