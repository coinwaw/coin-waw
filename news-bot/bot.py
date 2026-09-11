from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import feedparser


ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
OUTPUT_FILE = DATA_DIR / "news.json"

# Public RSS feeds. Check each publisher's terms before using its content
# commercially or republishing summaries at scale.
FEEDS = [
    ("CoinDesk", "https://www.coindesk.com/arc/outboundfeeds/rss/"),
    ("Cointelegraph", "https://cointelegraph.com/rss"),
    ("Yahoo Finance", "https://finance.yahoo.com/news/rssindex"),
]

CATEGORY_KEYWORDS = {
    "crypto": [
        "bitcoin", "btc", "ethereum", "eth", "solana", "sol", "crypto",
        "cryptocurrency", "blockchain", "defi", "stablecoin", "token",
        "binance", "coinbase", "sec crypto",
    ],
    "stocks": [
        "stock", "stocks", "shares", "nasdaq", "s&p 500", "dow jones",
        "earnings", "ipo", "equity", "wall street", "nvidia", "apple",
        "microsoft", "amazon", "tesla", "meta", "alphabet",
    ],
    "macro": [
        "federal reserve", "fed", "interest rate", "inflation", "cpi",
        "jobs", "employment", "gdp", "recession", "central bank",
        "treasury", "bond yield", "powell", "ecb", "boj",
    ],
    "finance": [
        "finance", "bank", "banking", "financial", "credit", "markets",
        "investment", "fund", "etf", "economy",
    ],
}

HIGH_IMPACT_KEYWORDS = [
    "breaking", "urgent", "approval", "approved", "rejected", "ban",
    "banned", "hack", "hacked", "exploit", "lawsuit", "regulation",
    "sec", "fed", "rate cut", "rate hike", "inflation", "war",
    "sanctions", "bankruptcy", "acquisition", "merger", "etf",
]


def clean_text(value: str) -> str:
    value = re.sub(r"<[^>]+>", " ", value or "")
    return re.sub(r"\s+", " ", value).strip()


def categorize(title: str, summary: str) -> str:
    text = f"{title} {summary}".lower()
    scores = {
        category: sum(1 for keyword in keywords if keyword in text)
        for category, keywords in CATEGORY_KEYWORDS.items()
    }
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "markets"


def impact_score(title: str, summary: str) -> int:
    text = f"{title} {summary}".lower()
    hits = sum(1 for keyword in HIGH_IMPACT_KEYWORDS if keyword in text)

    if hits >= 3:
        return 5
    if hits == 2:
        return 4
    if hits == 1:
        return 3
    return 1


def extract_assets(text: str) -> list[str]:
    text = text.lower()
    assets = []

    asset_map = {
        "BTC": ["bitcoin", "btc"],
        "ETH": ["ethereum", "eth"],
        "SOL": ["solana", "sol"],
        "SPX": ["s&p 500", "spx"],
        "NDX": ["nasdaq", "nasdaq 100"],
    }

    for symbol, keywords in asset_map.items():
        if any(keyword in text for keyword in keywords):
            assets.append(symbol)

    return assets


def parse_feed(source_name: str, feed_url: str) -> list[dict[str, Any]]:
    parsed = feedparser.parse(feed_url)
    articles = []

    for entry in parsed.entries[:50]:
        title = clean_text(entry.get("title", "Untitled"))
        url = entry.get("link", "").strip()
        summary = clean_text(entry.get("summary", ""))

        if not url or not title:
            continue

        published = (
            entry.get("published")
            or entry.get("updated")
            or datetime.now(timezone.utc).isoformat()
        )

        combined = f"{title} {summary}"

        articles.append(
            {
                "title": title,
                "source": source_name,
                "url": url,
                "published_at": published,
                "category": categorize(title, summary),
                "impact_score": impact_score(title, summary),
                "assets": extract_assets(combined),
                "summary": summary[:500],
                "collected_at": datetime.now(timezone.utc).isoformat(),
            }
        )

    return articles


def load_existing() -> list[dict[str, Any]]:
    if not OUTPUT_FILE.exists():
        return []

    try:
        return json.loads(OUTPUT_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []


def save_articles(articles: list[dict[str, Any]]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    existing = load_existing()
    known_urls = {item.get("url") for item in existing}

    for article in articles:
        if article["url"] not in known_urls:
            existing.append(article)
            known_urls.add(article["url"])

    # Newest records first, keep a manageable local archive.
    existing.sort(key=lambda item: item.get("collected_at", ""), reverse=True)
    existing = existing[:2000]

    OUTPUT_FILE.write_text(
        json.dumps(existing, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def print_top_news(articles: list[dict[str, Any]]) -> None:
    top = sorted(
        articles,
        key=lambda item: item.get("impact_score", 0),
        reverse=True,
    )[:10]

    if not top:
        return

    print("\nCoin Waw — Top News")
    print("=" * 60)

    for item in top:
        print(f"[{item['impact_score']}/5] {item['category'].upper()}")
        print(item["title"])
        print(f"Source: {item['source']}")
        print(f"URL: {item['url']}")
        print()


def main() -> None:
    if not FEEDS:
        print("No RSS feeds configured.")
        return

    collected = []

    for source_name, feed_url in FEEDS:
        try:
            items = parse_feed(source_name, feed_url)
            collected.extend(items)
            print(f"{source_name}: collected {len(items)} items")
        except Exception as exc:
            print(f"{source_name}: error: {exc}")

    save_articles(collected)
    print_top_news(collected)

    print(f"Saved archive to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
