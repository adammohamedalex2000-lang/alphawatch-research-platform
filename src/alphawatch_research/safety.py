from __future__ import annotations


class LiveExecutionDisabled(RuntimeError):
    """Raised when live execution is requested in the portfolio edition."""


def assert_paper_only(*, live_enabled: bool, broker_enabled: bool) -> None:
    """Hard boundary for this public repository."""

    if live_enabled or broker_enabled:
        raise LiveExecutionDisabled(
            "AlphaWatch portfolio edition is research/paper-only; live execution is disabled"
        )
