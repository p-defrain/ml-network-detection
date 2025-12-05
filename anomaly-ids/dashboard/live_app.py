import streamlit as st
import pandas as pd
import altair as alt
import time
import os

LIVE_PATH = "data/live/live_predictions.csv"

st.set_page_config(
    page_title="Live Network Anomaly Detection",
    layout="wide"
)

st.title("🛰 Live Network Anomaly Dashboard")
st.write("Updates automatically as new network flows are captured and scored.")

# Auto-refresh every 2 seconds
st_autorefresh = st.experimental_rerun

REFRESH_RATE = 2000  # ms

st_autorefresh(interval=REFRESH_RATE, limit=None)

if not os.path.exists(LIVE_PATH):
    st.warning("Waiting for live data... Start capture with: anomaly-detect live")
    st.stop()

df = pd.read_csv(LIVE_PATH)

# Convert scores to severity colors
def severity_color(score):
    if score < -0.2:
        return "Critical"
    elif score < -0.1:
        return "High"
    elif score < -0.05:
        return "Medium"
    else:
        return "Low"

df["severity"] = df["anomaly_score"].apply(severity_color)

# Summary metrics
col1, col2, col3 = st.columns(3)

col1.metric("Total Live Flows", len(df))
col2.metric("Total Anomalies", (df["label"] == "anomaly").sum())
col3.metric("Critical Alerts", (df["severity"] == "Critical").sum())

st.markdown("---")

# Anomaly score chart
st.subheader("📉 Live Anomaly Score Timeline")

line_chart = alt.Chart(df).mark_line().encode(
    x="timestamp:T",
    y="anomaly_score",
    color="label"
).properties(height=300)

st.altair_chart(line_chart, use_container_width=True)

st.markdown("---")

# Live table
st.subheader("🚨 Live Flow Alerts")

# Show newest first
df = df.sort_values("timestamp", ascending=False)

st.dataframe(
    df[[
        "src_ip", "dst_ip", "proto", "sport", "dport",
        "anomaly_score", "severity", "label", "timestamp"
    ]],
    height=400
)
