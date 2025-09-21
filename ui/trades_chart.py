import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from pathlib import Path
import re

st.set_page_config(page_title="Trades Chart", layout="wide")
st.title("Trading System – Candlestick with Trades")

# === File paths ===
price_csv = Path("data/ESM25_5m.csv")   # price data from your simulator run
orders_csv = Path("data/orders_ESM25_5m.csv")  # exported orders

if not price_csv.exists() or not orders_csv.exists():
    st.error("Missing price or orders CSV. Run the simulator with exports first.")
    st.stop()

# === Load and clean price data ===
price_df = pd.read_csv(price_csv)

# Normalize column names to lowercase expected by the rest of the script
price_df.rename(columns={
    "Time": "time",
    "Open": "open",
    "High": "high",
    "Low": "low",
    "Last": "close",
    "Volume": "volume"
}, inplace=True)

# Drop any non-data rows (e.g. Barchart footer/header)
pattern = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$")
price_df = price_df[price_df["time"].apply(lambda x: bool(pattern.match(str(x))))]

# Convert to datetime
price_df["time"] = pd.to_datetime(price_df["time"], format="%Y-%m-%d %H:%M")

# === Load orders ===
orders_df = pd.read_csv(orders_csv)

# Date range filter
min_date, max_date = price_df["time"].min().date(), price_df["time"].max().date()
date_range = st.date_input(
    "Select date range",
    [min_date, max_date],
    min_value=min_date,
    max_value=max_date,
)
if len(date_range) == 2:
    start, end = date_range
    mask = (price_df["time"].dt.date >= start) & (price_df["time"].dt.date <= end)
    price_df = price_df.loc[mask]

# === Build candlestick chart ===
fig = go.Figure(data=[go.Candlestick(
    x=price_df["time"],
    open=price_df["open"],
    high=price_df["high"],
    low=price_df["low"],
    close=price_df["close"],
    name="Price"
)])

# Map order bar index to timestamps inside the filtered price_df
trade_times = price_df["time"].reset_index(drop=True)
orders_df = orders_df.copy()
orders_df["time"] = orders_df["i"].apply(
    lambda idx: trade_times[idx] if 0 <= idx < len(trade_times) else None
)
orders_df.dropna(subset=["time"], inplace=True)

# Add buy/sell markers with hover info
for side, color, symbol in [("buy", "green", "triangle-up"), ("sell", "red", "triangle-down")]:
    subset = orders_df[orders_df["side"] == side]
    hover_text = subset.apply(
        lambda r: f"{side.upper()}<br>Qty: {r.qty}<br>Note: {r.note or ''}", axis=1
    )
    fig.add_trace(go.Scatter(
        x=subset["time"],
        y=[price_df.loc[price_df["time"] == t, "close"].values[0] for t in subset["time"]],
        mode="markers",
        marker=dict(color=color, size=10, symbol=symbol),
        name=side.capitalize(),
        text=hover_text,
        hoverinfo="text"
    ))

st.plotly_chart(fig, use_container_width=True)
