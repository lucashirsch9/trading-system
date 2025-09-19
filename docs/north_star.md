# Trading Automation — North Star

Purpose:
- Build a durable trading infrastructure for
  1. a minimal baseline trend policy, and
  2. a machine-learning–assisted Brooks-style trader.

Guiding Principles:
- All price-action features are **point-in-time** (no future look-ahead).
- One-definition-per-concept: each Brooks construct defined once in `src/trade_core/features.py`.
- Event-driven simulator: `simulate(strategy, bars, config) -> trades, equity_curve, logs`.
- Walk-forward evaluation and test-driven development (TDD).
- Hard risk rails baked in from the start.

Current Status:
- Repo scaffolded with `src/`, `tests/`, and `docs/` directories.
- Green test suite for core simulator contract.
- Local pre-commit hooks running ruff, mypy, and pytest.
- Implemented `ema20` feature with equivalence tests and no-lookahead guard.
- Stubbed `BaselineAlwaysIn` strategy ready for first simulated runs.
