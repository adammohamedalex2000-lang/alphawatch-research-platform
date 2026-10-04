from alphawatch_research.validation import ResearchState, ValidationInputs, classify_research_state


def test_small_sample_is_not_enough_data() -> None:
    state = classify_research_state(
        ValidationInputs(
            sample_size=9,
            minimum_sample_size=10,
            mean_abnormal_return=0.02,
            null_p_value=0.01,
            survives_costs=True,
            robustness_pass=True,
            forward_confirmed=True,
        )
    )
    assert state is ResearchState.NOT_ENOUGH_DATA


def test_wrong_direction_is_rejected() -> None:
    state = classify_research_state(
        ValidationInputs(
            sample_size=20,
            minimum_sample_size=10,
            mean_abnormal_return=-0.01,
            null_p_value=0.01,
            survives_costs=True,
            robustness_pass=True,
            forward_confirmed=True,
        )
    )
    assert state is ResearchState.REJECTED


def test_historical_strength_still_needs_forward_confirmation() -> None:
    state = classify_research_state(
        ValidationInputs(
            sample_size=100,
            minimum_sample_size=30,
            mean_abnormal_return=0.012,
            null_p_value=0.03,
            survives_costs=True,
            robustness_pass=True,
            forward_confirmed=False,
        )
    )
    assert state is ResearchState.NEEDS_FORWARD_CONFIRM


def test_confirmation_requires_all_gates() -> None:
    state = classify_research_state(
        ValidationInputs(
            sample_size=100,
            minimum_sample_size=30,
            mean_abnormal_return=0.012,
            null_p_value=0.03,
            survives_costs=True,
            robustness_pass=True,
            forward_confirmed=True,
        )
    )
    assert state is ResearchState.CONFIRMED
