# Security

This repository is a portfolio/research edition and intentionally has **no live-trading capability**.

## Secrets

- Never commit `.env`, API keys, passwords, tokens, broker credentials, account IDs, or private datasets.
- `.env.example` contains placeholders only.
- Public-source adapters should use source-compliant identification and rate limits.

## Network exposure

The FastAPI example is intended to bind to `127.0.0.1`. Do not expose it directly to the public internet without a proper authentication, TLS, rate-limiting, and deployment review.

## Trading boundary

`alphawatch_research.safety.assert_paper_only()` rejects any attempt to initialize this portfolio edition with live execution enabled. There is no broker adapter or order-routing module in this repository.

## Vulnerability reporting

For a security issue in this demonstration repository, open a GitHub issue without including credentials, private data, or exploit secrets.
