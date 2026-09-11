# Security

Security is important for Coin Waw.

## Never Commit Secrets

Never commit:

- Solana private keys
- seed phrases
- API keys
- passwords
- authentication tokens
- private credentials

## Environment Variables

Use environment variables for secrets.

Example:

```text
NEWS_API_KEY=your_key_here
TELEGRAM_BOT_TOKEN=your_token_here
```

Never place real credentials directly in source code.

## Recommended .gitignore

The root `.gitignore` already excludes common secret files.

## Reporting a Security Issue

Do not publicly disclose sensitive details before an issue can be investigated.

Security contact:

`[ADD SECURITY CONTACT]`

