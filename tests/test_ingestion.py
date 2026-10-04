from alphawatch_research.ingestion.sec_edgar import normalize_recent_filings
from alphawatch_research.ingestion.usaspending import build_award_search_payload


def test_edgar_normalizer_uses_only_available_rows() -> None:
    payload = {
        "cik": "123",
        "name": "Example Corp",
        "filings": {
            "recent": {
                "form": ["8-K", "10-Q"],
                "filingDate": ["2026-01-01", "2026-01-02"],
                "accessionNumber": ["a", "b"],
                "primaryDocument": ["a.htm", "b.htm"],
            }
        },
    }
    rows = normalize_recent_filings(payload, limit=1)
    assert rows == [
        {
            "cik": "123",
            "company_name": "Example Corp",
            "form": "8-K",
            "filing_date": "2026-01-01",
            "accession": "a",
            "primary_document": "a.htm",
        }
    ]


def test_usaspending_payload_caps_limit_and_preserves_filters() -> None:
    payload = build_award_search_payload(
        limit=500,
        start_date="2025-01-01",
        recipients=["Example"],
        minimum_award=1_000_000,
    )
    assert payload["limit"] == 100
    assert payload["filters"]["recipient_search_text"] == ["Example"]
    assert payload["filters"]["award_amounts"] == [{"lower_bound": 1_000_000.0}]
