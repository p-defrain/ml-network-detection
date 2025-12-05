import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import os

PRED_PATH = "data/processed/predictions.csv"

st.set_page_config(
    page_title="Network Anomaly Detection Dashboard",
    layout="wide"
)

st.title("🔍 Network Anomaly Detection Dashboard")
st.write("Interactive dashboard for reviewing ML-detected anomalies based on log + PCAP flow analysis.")

# -------- Load data -------- #
if not os.path.exists(PRED_PATH):
    st.error("Predictions file not found. Run the pipeline first.")
    st.stop()

df = pd.read_csv(PRED_PATH)

# Convert anomaly score to colors
def risk_color(score):
    if score < -0.2:
        return "red"
    elif score < -0.05:
        return "orange"
    else:
        return "green"

df["color"] = df["anomaly_score"].apply(risk_color)

# -------- Summary Metrics -------- #
col1, col2, col3 = st.columns(3)

col1.metric("Total Flows", len(df))
col2.metric("Normal", (df["label"] == "normal").sum())
col3.metric("Anomaly", (df["label"] == "anomaly").sum())

st.markdown("---")

# -------- Charts -------- #

st.subheader("📉 Anomaly Score Distribution")

chart = (
    alt.Chart(df)
    .mark_bar()
    .encode(
        x=alt.X("anomaly_score", bin=alt.Bin(maxbins=40)),
        y="count()",
        color="label"
    )
    .properties(height=300)
)

st.altair_chart(chart, use_container_width=True)

st.markdown("---")

# -------- Interactive Filtering -------- #

st.subheader("🔎 Flow Explorer (Filterable)")

score_range = st.slider(
    "Filter by anomaly score:",
    float(df["anomaly_score"].min()),
    float(df["anomaly_score"].max()),
    (float(df["anomaly_score"].min()), float(df["anomaly_score"].max()))
)

label_filter = st.multiselect(
    "Filter by label:",
    options=df["label"].unique(),
    default=df["label"].unique()
)

filtered_df = df[
    (df["anomaly_score"] >= score_range[0]) &
    (df["anomaly_score"] <= score_range[1]) &
    (df["label"].isin(label_filter))
]

st.dataframe(
    filtered_df[
        [
            "src_ip",
            "dst_ip",
            "packet_count",
            "byte_count",
            "anomaly_score",
            "label",
        ]
    ],
    height=400,
)

st.markdown("---")

# -------- Top Anomalies -------- #

st.subheader("🚨 Top 20 Most Suspicious Flows")

top_anom = df.sort_values("anomaly_score").head(20)

st.dataframe(
    top_anom[
        ["src_ip", "dst_ip", "packet_count", "byte_count", "anomaly_score", "label"]
    ],
    height=300
)
