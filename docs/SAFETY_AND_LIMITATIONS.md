# Safety and Limitations

## No live trading

This repository contains no broker connectivity, order-routing implementation, or real-money execution path. The safety module rejects `live_enabled=True`.

## No performance claim

AlphaWatch should not be presented as a profitable strategy, a fund, or a proven alpha engine. The larger research archive produced both positive controls and null/rejected hypotheses. This portfolio edition demonstrates the **research machinery**, not investment performance.

## Data quality is a first-class risk

A backtest can look precise while being invalid because of:

- survivorship bias
- look-ahead bias
- recycled ticker symbols
- incorrect entity mapping
- stale market data
- corporate-action errors
- point-in-time constituent errors
- missing delisted securities

A clean chart does not compensate for invalid source data.

## Public-source limitations

SEC EDGAR and USAspending are useful public sources, but production-grade research still requires careful handling of identifiers, rate limits, timestamp semantics, schema changes, and historical completeness.

## Statistical limitations

The included null test is intentionally small and educational. Serious empirical work may require richer resampling schemes, clustered standard errors, multiple-testing corrections, regime analysis, and more rigorous treatment of overlapping return windows.

## Portfolio-edition scope

This repository intentionally omits much of the original experimental codebase. Its goal is clarity and inspectability, not feature parity with the larger archive.
