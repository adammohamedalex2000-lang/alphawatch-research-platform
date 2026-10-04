import pytest

from alphawatch_research.research.monte_carlo import bootstrap_terminal_values
from alphawatch_research.research.null_tests import sign_flip_p_value
from alphawatch_research.research.power import required_sample_size


def test_power_matches_formula() -> None:
    assert required_sample_size(0.01, 0.025) == 49


def test_null_test_is_deterministic_for_seed() -> None:
    data = [0.01, 0.02, 0.015, 0.03, 0.005]
    first = sign_flip_p_value(data, simulations=1_000, seed=7)
    second = sign_flip_p_value(data, simulations=1_000, seed=7)
    assert first == second
    assert first is not None
    assert 0 <= first <= 1


def test_monte_carlo_is_deterministic_and_reports_loss_probability() -> None:
    result = bootstrap_terminal_values(
        [0.01, -0.005, 0.002], horizon=10, simulations=1_000, seed=11
    )
    again = bootstrap_terminal_values(
        [0.01, -0.005, 0.002], horizon=10, simulations=1_000, seed=11
    )
    assert result == again
    assert 0 <= result["probability_of_loss"] <= 1
    assert result["p05_terminal_value"] <= result["median_terminal_value"]
    assert result["median_terminal_value"] <= result["p95_terminal_value"]


def test_invalid_monte_carlo_input_is_rejected() -> None:
    with pytest.raises(ValueError):
        bootstrap_terminal_values([])
