from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True, slots=True)
class Event:
    """Normalized public event observed by the research pipeline."""

    event_id: str
    ticker: str
    observed_on: date
    source: str
    event_type: str


@dataclass(frozen=True, slots=True)
class PriceBar:
    """Minimal daily price bar used by the portfolio research engine."""

    day: date
    close: float


@dataclass(frozen=True, slots=True)
class EventReturn:
    """Event-level forward return and benchmark-adjusted abnormal return."""

    event_id: str
    ticker: str
    horizon: int
    raw_return: float
    benchmark_return: float
    abnormal_return: float
