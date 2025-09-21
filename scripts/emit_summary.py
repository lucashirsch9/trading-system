# scripts/emit_summary.py
import argparse
import json
import math
import os
from datetime import datetime
import pandas as pd

def max_drawdown(series):
    # classic MDD on equity curve
    roll_max = series.cummax()
    dd = (series - roll_max)
    return float(dd.min()), float((dd / roll_max).min())  # abs, pct

def safe_path(p):
    return os.path.abspath(p) if p else None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--equity", required=True, help="CSV exported by run_sim_baseline --export-equity")
    ap.add_argument("--orders", help="CSV from --export-orders")
    ap.add_argument("--fills", help="CSV from --export-fills")
    ap.add_argument("--events", help="CSV from --export-events")
    ap.add_argument("--multiplier", type=float, default=None)
    ap.add_argument("--commission-per-trade", type=float, default=None)
    ap.add_argument("--end-close", type=int, choices=[0,1], default=1, help="1 if end-of-run flatten occurred (default 1)")
    ap.add_argument("--out", required=True, help="Output JSON path, e.g. data/run_summary.json")
    args = ap.parse_args()

    eq = pd.read_csv(args.equity)
    # be flexible on column names
    # expect columns like: time, equity or cash/position_value/equity; fall back to last col
    equity_col = None
    for cand in ["equity", "Equity", "EQUITY"]:
    	if cand in eq.columns:
        	equity_col = cand
        	break
    if equity_col is None:
        equity_col = eq.columns[-1]  # last column is often equity in our exports
    equity = eq[equity_col].astype(float)

    start_equity = float(equity.iloc[0])
    end_equity   = float(equity.iloc[-1])
    net_pnl      = end_equity - start_equity
    ret_pct      = (net_pnl / start_equity) * 100.0 if start_equity != 0 else math.nan

    mdd_abs, mdd_pct = max_drawdown(equity)
    bars = int(len(equity))

    # Optional paths (None if not supplied)
    summary = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "stats": {
            "start_equity": round(start_equity, 2),
            "end_equity": round(end_equity, 2),
            "net_pnl": round(net_pnl, 2),
            "return_pct": round(ret_pct, 4),
            "max_drawdown_abs": round(mdd_abs, 2),
            "max_drawdown_pct": round(mdd_pct * 100.0, 4),
            "bars": bars
        },
        "accounting": {
            "multiplier": args.multiplier,
            "commission_per_trade": args.commission_per_trade,
            "end_close": bool(args.end_close),
        },
        "artifacts": {
            "equity_csv": safe_path(args.equity),
            "orders_csv": safe_path(args.orders),
            "fills_csv": safe_path(args.fills),
            "events_csv": safe_path(args.events),
        },
        "ui_contract_version": 1
    }

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print(f"[emit_summary] wrote {os.path.abspath(args.out)}")
    print(json.dumps(summary["stats"], indent=2))

if __name__ == "__main__":
    main()
