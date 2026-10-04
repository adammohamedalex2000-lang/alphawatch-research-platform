from __future__ import annotations

from typing import Any

import httpx

SEARCH_URL = "https://api.usaspending.gov/api/v2/search/spending_by_award/"


def build_award_search_payload(
    *,
    limit: int = 25,
    page: int = 1,
    start_date: str | None = None,
    end_date: str | None = None,
    recipients: list[str] | None = None,
    minimum_award: float | None = None,
) -> dict[str, Any]:
    """Build a deterministic USAspending award-search request."""

    filters: dict[str, Any] = {"award_type_codes": ["A", "B", "C", "D"]}
    if start_date or end_date:
        filters["time_period"] = [
            {
                "start_date": start_date or "1900-01-01",
                "end_date": end_date or "2100-01-01",
            }
        ]
    if recipients:
        filters["recipient_search_text"] = recipients
    if minimum_award is not None:
        filters["award_amounts"] = [{"lower_bound": float(minimum_award)}]

    return {
        "filters": filters,
        "fields": [
            "Award ID",
            "Recipient Name",
            "Award Amount",
            "Award Date",
            "Action Date",
            "Start Date",
            "Last Modified Date",
            "generated_unique_award_id",
            "Awarding Agency",
            "Awarding Sub Agency",
            "NAICS",
        ],
        "limit": min(max(limit, 1), 100),
        "page": max(page, 1),
        "sort": "Start Date",
        "order": "desc",
    }


class USAspendingClient:
    """Small public API client for federal award search."""

    def __init__(self, *, timeout: float = 30.0) -> None:
        self.timeout = timeout

    def search_awards(self, **kwargs: Any) -> list[dict[str, Any]]:
        payload = build_award_search_payload(**kwargs)
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        with httpx.Client(timeout=self.timeout, headers=headers) as client:
            response = client.post(SEARCH_URL, json=payload)
            response.raise_for_status()
            data = response.json()
        results = data.get("results", [])
        if not isinstance(results, list):
            raise TypeError("Unexpected USAspending response shape")
        return results
