from __future__ import annotations

import random
from statistics import median


def bootstrap_terminal_values(
    returns: list[float],
    *,
    initial_value: float = 100.0,
    horizon: int = 20,
    simulations: int = 5_000,
    seed: int = 42,
) -> dict[str, float | int]:
    """Bootstrap terminal portfolio values from an empirical return distribution."""

    if not returns:
        raise ValueError("returns cannot be empty")
    if initial_value <= 0 or horizon < 1 or simulations < 100:
        raise ValueError("invalid simulation parameters")
    if any(value <= -1.0 for value in returns):
        raise ValueError("returns must be greater than -100%")

    rng = random.Random(seed)
    terminal: list[float] = []
    for _ in range(simulations):
        value = initial_value
        for _ in range(horizon):
            value *= 1.0 + rng.choice(returns)
        terminal.append(value)

    terminal.sort()
    n = len(terminal)
    p05 = terminal[max(0, int(n * 0.05) - 1)]
    p95 = terminal[min(n - 1, int(n * 0.95))]
    return {
        "simulations": simulations,
        "horizon": horizon,
        "median_terminal_value": median(terminal),
        "p05_terminal_value": p05,
        "p95_terminal_value": p95,
        "probability_of_loss": sum(value < initial_value for value in terminal) / n,
    }
