from __future__ import annotations

from datetime import date, timedelta

from alphawatch_research.models import Event, PriceBar
from alphawatch_research.research.event_study import event_study, summarize_abnormal_returns
from alphawatch_research.research.null_tests import sign_flip_p_value
from alphawatch_research.validation import ValidationInputs, classify_research_state


def series(start: date, closes: list[float]) -> list[PriceBar]:
    return [PriceBar(day=start + timedelta(days=i), close=value) for i, value in enumerate(closes)]


def main() -> None:
    start = date(2026, 1, 1)
    events = [
        Event("E1", "AAA", start, "demo", "filing"),
        Event("E2", "BBB", start, "demo", "award"),
        Event("E3", "CCC", start, "demo", "filing"),
    ]
    prices = {
        "AAA": series(start, [100, 101, 102, 103, 104, 106]),
        "BBB": series(start, [100, 100, 101, 102, 103, 104]),
        "CCC": series(start, [100, 99, 100, 101, 102, 103]),
    }
    benchmark = series(start, [100, 100.2, 100.4, 100.5, 100.7, 101.0])

    rows = event_study(events, prices, benchmark, horizon=5)
    summary = summarize_abnormal_returns(rows)
    p_value = sign_flip_p_value([row.abnormal_return for row in rows], simulations=2_000)
    state = classify_research_state(
        ValidationInputs(
            sample_size=summary["n"],
            minimum_sample_size=3,
            mean_abnormal_return=summary["mean_abnormal_return"],
            null_p_value=p_value,
            survives_costs=True,
            robustness_pass=True,
            forward_confirmed=False,
        )
    )

    print("summary:", summary)
    print("sign-flip p-value:", round(p_value or 0.0, 4))
    print("research state:", state)


if __name__ == "__main__":
    main()
