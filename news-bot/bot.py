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

# Replace/add feeds only when their terms permit your intended use.
FEEDS = [
    # Example public RSS feeds can be added here.
    # ("Source Name", "https://example.com/rss"),
]

CATEGORY_KEYWORDS = {
    "crypto": [
        "bitcoin", "btc", "ethereum", "eth", "solana", "sol", "crypto",
        "cryptocurrency", "blockchain", "defi", "token", "stablecoin",
    ],
    "stocks": [
        "stock", "stocks", "shares", "nasdaq", "s&p 500", "dow jones",
        "earnings", "ipo", "equity", "wall street",
    ],
    "macro": [
        "federal reserve", "fed", "interest rate", "inflation", "cpi",
        "jobs", "employment", "gdp", "recession", "central bank",
        "treasury", "bond yield",
    ],
    "finance": [
        "finance", "bank", "banking", "financial", "credit", "markets",
        "investment", "fund",
    ],
}


def clean_text(value: str) -> str:
    """Remove HTML tags and normalize whitespace."""
    value = re.sub(r"<[^>]+>", " ", value or "")
    return re.sub(r"\s+", " ", value).strip()


def categorize(title: str, summary: str) -> str:
    text = f"{title} {summary}".lower()

    scores: dict[str, int] = {}
    for category, keywords in CATEGORY_KEYWORDS.items():
        scores[category] = sum(1 for keyword in keywords if keyword in text)

    best_category = max(scores, key=scores.get)
    return best_category if scores[best_category] > 0 else "markets"


def parse_feed(source_name: str, feed_url: str) -> list[dict[str, Any]]:
    parsed = feedparser.parse(feed_url)
    articles: list[dict[str, Any]] = []

    for entry in parsed.entries[:50]:
        title = clean_text(entry.get("title", "Untitled"))
        url = entry.get("link", "").strip()
        summary = clean_text(entry.get("summary", ""))

        if not url:
            continue

        published = (
            entry.get("published")
            or entry.get("updated")
            or datetime.now(timezone.utc).isoformat()
        )

        articles.append(
            {
                "title": title,
                "source": source_name,
                "url": url,
                "published_at": published,
                "category": categorize(title, summary),
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

    # Keep the latest 2,000 records.
    existing = existing[-2000:]

    OUTPUT_FILE.write_text(
        json.dumps(existing, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def main() -> None:
    if not FEEDS:
        print("No RSS feeds configured.")
        print("Add permitted RSS feeds to FEEDS in news-bot/bot.py.")
        return

    collected: list[dict[str, Any]] = []

    for source_name, feed_url in FEEDS:
        try:
            items = parse_feed(source_name, feed_url)
            collected.extend(items)
            print(f"{source_name}: collected {len(items)} items")
        except Exception as exc:
            print(f"{source_name}: error: {exc}")

    save_articles(collected)
    print(f"Saved data to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()

