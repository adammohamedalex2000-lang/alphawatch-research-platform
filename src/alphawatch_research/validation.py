from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class ResearchState(StrEnum):
    NOT_ENOUGH_DATA = "NOT_ENOUGH_DATA"
    DESCRIPTIVE_ONLY = "DESCRIPTIVE_ONLY"
    HISTORICAL_CANDIDATE = "HISTORICAL_CANDIDATE"
    NEEDS_FORWARD_CONFIRM = "NEEDS_FORWARD_CONFIRM"
    CONFIRMED = "CONFIRMED"
    REJECTED = "REJECTED"


@dataclass(frozen=True, slots=True)
class ValidationInputs:
    sample_size: int
    minimum_sample_size: int
    mean_abnormal_return: float | None
    predicted_direction: int = 1
    null_p_value: float | None = None
    survives_costs: bool = False
    robustness_pass: bool = False
    forward_confirmed: bool = False


def classify_research_state(inputs: ValidationInputs) -> ResearchState:
    """Conservative research-state classifier.

    Historical strength can create a candidate, but only independent forward
    evidence can produce CONFIRMED.
    """

    if inputs.sample_size < max(1, inputs.minimum_sample_size):
        return ResearchState.NOT_ENOUGH_DATA
    if inputs.mean_abnormal_return is None:
        return ResearchState.DESCRIPTIVE_ONLY

    signed_effect = inputs.mean_abnormal_return * (1 if inputs.predicted_direction >= 0 else -1)
    if signed_effect <= 0:
        return ResearchState.REJECTED

    if inputs.null_p_value is None or inputs.null_p_value > 0.10:
        return ResearchState.DESCRIPTIVE_ONLY

    if not inputs.survives_costs or not inputs.robustness_pass:
        return ResearchState.DESCRIPTIVE_ONLY

    if not inputs.forward_confirmed:
        return ResearchState.NEEDS_FORWARD_CONFIRM

    return ResearchState.CONFIRMED
