# Research Methodology

AlphaWatch is built around falsification rather than backtest optimization.

## 1. Predefine the hypothesis

Before reading the result, record:

- event definition
- observation timestamp
- expected direction
- measurement horizon
- benchmark
- minimum sample size
- transaction-cost assumption
- pass/fail criteria

Changing those fields after observing the result creates a new experiment rather than silently rewriting the original one.

## 2. Separate event, signal, and edge

- **Event**: an observed filing, award, or other catalyst.
- **Signal**: an event that passes deterministic eligibility rules.
- **Edge**: a repeatable abnormal-return pattern that survives validation.

An event is not automatically a signal, and a signal is not automatically evidence of edge.

## 3. Use an observation point that could have been known at the time

Returns should be measured from a timestamp that reflects when the information became observable to the research process. This reduces look-ahead bias.

## 4. Measure benchmark-adjusted forward returns

For an event return `R_i` and benchmark return `R_b`:

```text
abnormal_return = R_i - R_b
```

AlphaWatch aggregates event-level abnormal returns into cohort statistics rather than treating one successful example as proof.

## 5. Run null tests

The portfolio edition includes a deterministic sign-flip/permutation test. In the broader project, null thinking also included matched-random and date-shuffled cohorts.

The question is not only whether the observed mean is positive; it is whether the result is unusually strong relative to a plausible null process.

## 6. Include transaction-cost sensitivity

A gross result that disappears under a reasonable cost assumption is labeled cost-sensitive rather than promoted.

## 7. Use power analysis

Before collecting endless observations, estimate the sample size required for a target effect size and assumed volatility:

```text
N ≈ ((z_alpha + z_power) * sigma / effect)^2
```

This makes "not enough data" a quantitative state rather than a vague excuse.

## 8. Preserve holdouts and forward confirmation

Historical exploration and forward observation serve different purposes. A historical candidate should not be treated as confirmed until it survives genuinely unseen data.

## 9. Keep failed experiments

Nulls and rejected hypotheses are part of the research record. Deleting them creates survivorship bias at the experiment level.

## Decision ladder

```text
NOT_ENOUGH_DATA
DESCRIPTIVE_ONLY
HISTORICAL_CANDIDATE
NEEDS_FORWARD_CONFIRM
CONFIRMED
REJECTED
```

The default bias is conservative: when evidence is ambiguous, the state moves downward rather than upward.
