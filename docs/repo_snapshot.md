# Repo Snapshot — trading-system

## Folder Tree
docs/
  decisions.md          — chronological log of all design and implementation decisions
  gpt_instructions.md   — full system prompt and contribution rules for the Custom GPT
  north_star.md         — project purpose, principles, and current status
  repo_snapshot.md      — this complete file-by-file reference

src/
  trade_core/
    __init__.py
    sim.py              — event-driven simulator contract and stub implementation
    features.py         — feature functions (e.g. ema20) defined once, point-in-time safe
  trade_strategies/
    __init__.py
    baseline.py         — BaselineAlwaysIn strategy skeleton
  trade_ui/
    __init__.py         — placeholder for future dashboards or API

tests/
  test_env_imports.py          — verifies core libs import
  test_sim_contract.py         — checks simulator contract and base behavior
  test_features_ema.py         — verifies ema20 matches pandas.ewm and is point-in-time
  test_features_no_lookahead.py — guards against future lookahead in ema20
  test_baseline_import.py      — verifies BaselineAlwaysIn imports correctly

pytest.ini             — adds src/ to PYTHONPATH for pytest
.pre-commit-config.yaml — local pre-commit hooks running ruff, mypy, pytest
.gitignore             — ignores virtual envs, caches, and parquet data files

## 2025-09-20 — Repo Snapshot (post-sim upgrades)

### Key files (added/changed)
- `scripts/_bootstrap.py` — ensures `src/` on `sys.path`.
- `scripts/run_sim_baseline.py` — CLI runner:
  - Args: CSV cols, `--baseline-mode`, accounting, `--multiplier`, auto-sizing (`--risk-pct`, `--min-qty`, `--max-qty`, `--round-lot`), stops/targets (`--stop-pct`, `--target-pct`), exports, verbosity (`--show`).
  - Prints counts, previews, summary; writes CSVs if requested.
- `src/trade_core/sim.py` — simulator:
  - Lifecycle tolerant, equity events, forced close, multiplier, commission.
  - Auto-size on entries, auto-flatten on qty-less exits.
- `src/trade_strategies/baseline.py` — baseline with modes + optional stop/target.

### Typical commands
```bat
# Lint + typecheck + tests
pre-commit run -a
pytest -q

# Run baseline with ES multiplier and equity export
python -m scripts.run_sim_baseline --csv "data\\ESM25_5m.csv" --limit-rows 5000 --export-equity "data\\equity_ESM25_5m.csv"

# Size 2% of equity, cap size 3, stops/targets
python -m scripts.run_sim_baseline --csv "data\\ESM25_5m.csv" --risk-pct 2 --max-qty 3 --stop-pct 1.0 --target-pct 1.5

### Session – 2025-09-21

Key updates made during this session:
1. **scripts/emit_summary.py** – creates `data/run_summary.json` from simulator CSV exports (equity, orders, fills, events).
2. **ui/dashboard.py** – first Streamlit page: shows run summary metrics and equity curve.
3. **ui/trades_chart.py** – candlestick chart with buy/sell markers and hoverable trade details. Includes column normalization and Barchart-footer cleanup.

Suggested commit message:
