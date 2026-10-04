from __future__ import annotations

import math


def required_sample_size(
    effect: float,
    sigma: float,
    *,
    z_alpha: float = 1.96,
    z_power: float = 0.84,
) -> int:
    """Approximate observations required for a mean effect under a normal model."""

    if effect <= 0 or sigma <= 0:
        raise ValueError("effect and sigma must be positive")
    return max(1, math.ceil(((z_alpha + z_power) * sigma / effect) ** 2))
