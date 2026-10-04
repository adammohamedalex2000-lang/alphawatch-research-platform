from datetime import date, timedelta

import pytest

from alphawatch_research.models import Event, PriceBar
from alphawatch_research.research.event_study import event_study, summarize_abnormal_returns


def bars(start: date, closes: list[float]) -> list[PriceBar]:
    return [PriceBar(start + timedelta(days=i), close) for i, close in enumerate(closes)]


def test_event_study_uses_first_bar_on_or_after_observation_date() -> None:
    start = date(2026, 1, 1)
    event = Event("e1", "AAA", start + timedelta(days=1), "sec", "8-k")
    prices = {"AAA": bars(start, [100, 101, 103, 104])}
    benchmark = bars(start, [100, 101, 102, 103])

    result = event_study([event], prices, benchmark, horizon=2)

    assert len(result) == 1
    assert result[0].raw_return == pytest.approx(104 / 101 - 1)
    assert result[0].benchmark_return == pytest.approx(103 / 101 - 1)
    assert result[0].abnormal_return == pytest.approx((104 / 101) - (103 / 101))


def test_event_study_skips_insufficient_forward_history() -> None:
    start = date(2026, 1, 1)
    event = Event("e1", "AAA", start, "sec", "8-k")
    prices = {"AAA": bars(start, [100, 101])}
    benchmark = bars(start, [100, 101])
    assert event_study([event], prices, benchmark, horizon=5) == []


def test_summary_is_descriptive_only_math() -> None:
    start = date(2026, 1, 1)
    events = [Event("e1", "AAA", start, "demo", "event")]
    prices = {"AAA": bars(start, [100, 102])}
    benchmark = bars(start, [100, 101])
    rows = event_study(events, prices, benchmark, horizon=1)
    summary = summarize_abnormal_returns(rows)
    assert summary["n"] == 1
    assert summary["mean_abnormal_return"] == pytest.approx(0.01)
    assert summary["t_statistic"] is None
