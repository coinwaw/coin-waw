# Coin Waw Data

This directory stores structured data generated or used by Coin Waw tools.

## Possible Data

- news metadata
- market events
- source information
- timestamps
- categories
- asset references

## Example Schema

```json
{
  "title": "Example market news",
  "source": "Example Source",
  "url": "https://example.com/article",
  "published_at": "2026-01-01T12:00:00Z",
  "category": "crypto",
  "summary": "Short source-attributed summary."
}
```

## Data Rules

- Preserve original source URLs.
- Do not fabricate data.
- Keep timestamps when available.
- Respect source/API licensing terms.
- Do not commit credentials.

Generated files such as `news.json` may be ignored by Git if they become large.

