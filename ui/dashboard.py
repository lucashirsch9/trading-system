import json
import pandas as pd
import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Trading System Dashboard", layout="wide")

st.title("Trading System – Run Summary")

summary_path = Path("data/run_summary.json")
if not summary_path.exists():
    st.error("No run_summary.json found. Run emit_summary first.")
    st.stop()

with open(summary_path, "r") as f:
    summary = json.load(f)

stats = summary["stats"]
accounting = summary["accounting"]
equity_csv = summary["artifacts"]["equity_csv"]

st.subheader("Key Stats")
cols = st.columns(3)
cols[0].metric("Net PnL", f"${stats['net_pnl']:.2f}")
cols[1].metric("Return %", f"{stats['return_pct']:.2f}%")
cols[2].metric("Max Drawdown %", f"{stats['max_drawdown_pct']:.2f}%")

st.write("**Bars traded:**", stats["bars"])
st.write("**Commission per trade:**", accounting["commission_per_trade"])
st.write("**Multiplier:**", accounting["multiplier"])
st.write("**End close:**", accounting["end_close"])

st.subheader("Equity Curve")
if equity_csv:
    df = pd.read_csv(equity_csv)
    st.line_chart(df[df.columns[-1]])  # last column assumed equity

st.subheader("Artifacts")
st.json(summary["artifacts"])
