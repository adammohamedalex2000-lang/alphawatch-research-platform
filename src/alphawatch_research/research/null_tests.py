from __future__ import annotations

import random
from statistics import mean


def sign_flip_p_value(
    observed: list[float],
    *,
    simulations: int = 10_000,
    seed: int = 42,
) -> float | None:
    """Two-sided sign-flip randomization p-value for a cohort mean.

    Sign flipping preserves the magnitude distribution while destroying the
    directional effect under a symmetric null. It is useful as a compact
    portfolio demonstration, not a replacement for every empirical null design.
    """

    if not observed:
        return None
    if simulations < 100:
        raise ValueError("simulations must be at least 100")

    rng = random.Random(seed)
    observed_mean = abs(mean(observed))
    extreme = 0
    for _ in range(simulations):
        simulated = mean(value * rng.choice((-1.0, 1.0)) for value in observed)
        if abs(simulated) >= observed_mean:
            extreme += 1
    return (extreme + 1) / (simulations + 1)
