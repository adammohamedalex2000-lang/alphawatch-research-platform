from __future__ import annotations

from typing import Any

import httpx

COMPANY_SUBMISSIONS = "https://data.sec.gov/submissions/CIK{cik:010d}.json"


def normalize_recent_filings(payload: dict[str, Any], *, limit: int = 20) -> list[dict[str, Any]]:
    """Normalize the small filing subset used by AlphaWatch research examples."""

    recent = payload.get("filings", {}).get("recent", {})
    forms = recent.get("form", []) or []
    dates = recent.get("filingDate", []) or []
    accessions = recent.get("accessionNumber", []) or []
    primary_docs = recent.get("primaryDocument", []) or []

    n = min(limit, len(forms), len(dates))
    rows: list[dict[str, Any]] = []
    for index in range(n):
        rows.append(
            {
                "cik": payload.get("cik"),
                "company_name": payload.get("name"),
                "form": forms[index],
                "filing_date": dates[index],
                "accession": accessions[index] if index < len(accessions) else None,
                "primary_document": primary_docs[index] if index < len(primary_docs) else None,
            }
        )
    return rows


class EdgarClient:
    """Narrow SEC EDGAR client for recent filing metadata."""

    def __init__(self, user_agent: str, *, timeout: float = 30.0) -> None:
        if not user_agent.strip():
            raise ValueError("SEC requests require a descriptive user agent")
        self.user_agent = user_agent
        self.timeout = timeout

    def recent_filings(self, cik: int, *, limit: int = 20) -> list[dict[str, Any]]:
        headers = {"User-Agent": self.user_agent, "Accept-Encoding": "gzip, deflate"}
        with httpx.Client(timeout=self.timeout, follow_redirects=True, headers=headers) as client:
            response = client.get(COMPANY_SUBMISSIONS.format(cik=cik))
            response.raise_for_status()
            payload = response.json()
        return normalize_recent_filings(payload, limit=limit)
