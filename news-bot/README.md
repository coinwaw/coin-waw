# Coin Waw News Bot

A lightweight Python RSS collector for the Coin Waw financial-news project.

## What it does

The current version:

- reads configured RSS feeds
- collects article metadata
- removes duplicate URLs
- classifies stories as crypto, stocks, macro, finance, or markets
- assigns a simple 1–5 impact score
- detects a small set of market assets
- saves structured records to `data/news.json`
- prints the highest-scoring stories

This is a starter data pipeline, not an automated financial-advice system.

## Setup

Python 3.10+ is recommended.

```bash
cd news-bot
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install:

```bash
pip install -r requirements.txt
```

Run:

```bash
python bot.py
```

## Output

The bot writes:

```text
../data/news.json
```

Example record:

```json
{
  "title": "Example market story",
  "source": "Example Source",
  "url": "https://example.com/story",
  "published_at": "2026-01-01T12:00:00Z",
  "category": "crypto",
  "impact_score": 3,
  "assets": ["BTC"],
  "summary": "Short source-provided summary.",
  "collected_at": "2026-01-01T12:05:00Z"
}
```

## RSS Sources

The starter configuration includes:

- CoinDesk
- Cointelegraph
- Yahoo Finance

RSS availability and publisher terms can change. Review each publisher's current terms before using the feeds for commercial redistribution.

The bot stores metadata and source links; it should not be used to republish full copyrighted articles.

## Impact Score

The current score is deliberately simple:

- `1` = normal story
- `3` = contains a market-impact keyword
- `4` = multiple impact signals
- `5` = several strong signals

This is **not** a prediction of price movement.

## Next upgrades

Recommended next steps:

1. Store data in SQLite/PostgreSQL.
2. Add stronger duplicate detection.
3. Add source reliability metadata.
4. Add a review queue before publishing.
5. Generate short summaries with an appropriate LLM/API.
6. Add Telegram/Discord output.
7. Add scheduled execution.
8. Add tests.
9. Add a web dashboard.
