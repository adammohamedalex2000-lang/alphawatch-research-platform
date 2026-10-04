from __future__ import annotations

from fastapi import FastAPI

from alphawatch_research.research.power import required_sample_size
from alphawatch_research.safety import assert_paper_only

app = FastAPI(
    title="AlphaWatch Research API",
    version="0.1.0",
    description="Local, paper-only research demonstration API.",
)


@app.get("/health")
def health() -> dict[str, str | bool]:
    assert_paper_only(live_enabled=False, broker_enabled=False)
    return {"status": "ok", "paper_only": True, "live_trading": False}


@app.get("/research/power")
def power(effect: float = 0.01, sigma: float = 0.025) -> dict[str, float | int]:
    return {
        "effect": effect,
        "sigma": sigma,
        "required_sample_size": required_sample_size(effect, sigma),
    }
