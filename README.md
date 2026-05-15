# 🐂 Bull — 24/7 AI Trading Agent

Autonomous paper-trading agent powered by Claude Code routines on Opus 4.7. Trades US equities via Alpaca API. Goal: beat the S&P 500.

## Architecture

- **Brain:** Claude Code routines (cloud-scheduled cron jobs).
- **Broker:** Alpaca paper trading.
- **Data:** Alpaca news API + Yahoo Finance + Claude WebSearch.
- **Notifications:** Email via Gmail SMTP.
- **Memory:** Markdown files in `memory/` — committed to git after every run.

## Daily schedule (ET)

| Routine | Time | What it does |
|---|---|---|
| Pre-market | 06:00 Mon–Fri | Research overnight catalysts, draft trade plan |
| Market open | 09:30 Mon–Fri | Execute trade plan, log trades |
| Midday | 12:00 Mon–Fri | Cut losers, trim winners, daily-loss check |
| Close | 16:00 Mon–Fri | Daily report email + journal |
| Weekly review | 16:00 Friday | Grade the week, adjust strategy if needed |

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
│   ├── pre-market.md
│   ├── market-open.md
│   ├── midday.md
│   ├── close.md
│   └── weekly-review.md
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
