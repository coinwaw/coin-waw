# Coin Waw News Bot

A lightweight starter RSS collector for Coin Waw.

## Purpose

The bot collects publicly available RSS article metadata and stores it as structured JSON.

It is designed as a starting point for a larger financial-news pipeline.

## Current Features

- RSS feed collection
- URL-based duplicate detection
- Basic keyword categorization
- JSON output
- Source attribution
- Configurable feeds

## Architecture

```text
RSS Sources
    ↓
Feed Collector
    ↓
Duplicate Detection
    ↓
Keyword Categorization
    ↓
JSON Storage
    ↓
Future: Telegram / Discord / X / Web
```

## Setup

Requires Python 3.10+.

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

Install dependencies:

```bash
pip install -r requirements.txt
```

Run:

```bash
python bot.py
```

The output is written to:

```text
../data/news.json
```

## Sources

Edit `FEEDS` inside `bot.py` to add or remove RSS sources.

Only use sources whose terms permit the intended use.

The bot stores article metadata and links to the original source. It does not copy full articles.

## Future Improvements

- database storage
- better classification
- configurable keywords
- article scoring
- language detection
- Telegram alerts
- Discord alerts
- X publishing
- official-source verification
- tests
- scheduled execution

