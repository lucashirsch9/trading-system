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
