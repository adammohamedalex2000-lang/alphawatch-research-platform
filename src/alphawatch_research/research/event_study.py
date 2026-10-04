from __future__ import annotations

from bisect import bisect_left
from statistics import mean, median, stdev

from alphawatch_research.models import Event, EventReturn, PriceBar


def _validated_prices(bars: list[PriceBar]) -> list[PriceBar]:
    ordered = sorted(bars, key=lambda bar: bar.day)
    if any(bar.close <= 0 for bar in ordered):
        raise ValueError("Price bars must have strictly positive close values")
    if len({bar.day for bar in ordered}) != len(ordered):
        raise ValueError("Duplicate price-bar dates are not allowed")
    return ordered


def _entry_index(bars: list[PriceBar], observed_on) -> int | None:
    days = [bar.day for bar in bars]
    index = bisect_left(days, observed_on)
    if index >= len(days):
        return None
    return index


def _forward_return(bars: list[PriceBar], entry: int, horizon: int) -> float | None:
    exit_index = entry + horizon
    if horizon < 1 or exit_index >= len(bars):
        return None
    start = bars[entry].close
    end = bars[exit_index].close
    return end / start - 1.0


def event_study(
    events: list[Event],
    prices_by_ticker: dict[str, list[PriceBar]],
    benchmark_bars: list[PriceBar],
    *,
    horizon: int = 5,
) -> list[EventReturn]:
    """Compute event-level forward and benchmark-adjusted returns.

    The observation date is mapped to the first available trading bar on or after
    the event. Events without sufficient forward history are excluded rather than
    padded or imputed.
    """

    benchmark = _validated_prices(benchmark_bars)
    output: list[EventReturn] = []

    for event in events:
        ticker_bars = prices_by_ticker.get(event.ticker.upper())
        if not ticker_bars:
            continue
        prices = _validated_prices(ticker_bars)
        entry = _entry_index(prices, event.observed_on)
        benchmark_entry = _entry_index(benchmark, event.observed_on)
        if entry is None or benchmark_entry is None:
            continue

        raw = _forward_return(prices, entry, horizon)
        bench = _forward_return(benchmark, benchmark_entry, horizon)
        if raw is None or bench is None:
            continue

        output.append(
            EventReturn(
                event_id=event.event_id,
                ticker=event.ticker.upper(),
                horizon=horizon,
                raw_return=raw,
                benchmark_return=bench,
                abnormal_return=raw - bench,
            )
        )

    return output


def summarize_abnormal_returns(rows: list[EventReturn]) -> dict[str, float | int | None]:
    """Return simple cohort-level statistics without claiming causal significance."""

    values = [row.abnormal_return for row in rows]
    if not values:
        return {
            "n": 0,
            "mean_abnormal_return": None,
            "median_abnormal_return": None,
            "win_rate": None,
            "t_statistic": None,
        }

    avg = mean(values)
    wins = sum(value > 0 for value in values)
    t_statistic: float | None = None
    if len(values) >= 2:
        sigma = stdev(values)
        if sigma > 0:
            t_statistic = avg / (sigma / (len(values) ** 0.5))

    return {
        "n": len(values),
        "mean_abnormal_return": avg,
        "median_abnormal_return": median(values),
        "win_rate": wins / len(values),
        "t_statistic": t_statistic,
    }
