import streamlit as st
import pandas as pd
import sqlite3
import altair as alt

st.set_page_config(page_title="Kaizen Heatmap", layout="wide")

DB_FILE = "kaizen_records.db"
conn = sqlite3.connect(DB_FILE)

st.title("🔥 Kaizen Heatmap")

df = pd.read_sql_query("SELECT * FROM kaizen", conn)

if df.empty:
    st.warning("No Kaizen records found.")
    st.stop()

df["Timestamp"] = pd.to_datetime(df["Timestamp"])
df["Date"] = df["Timestamp"].dt.date

# -----------------------------
# HEATMAP 1 — KAIZENS BY OWNER & DATE
# -----------------------------
st.subheader("📅 Kaizens by Owner Over Time")

heatmap_data = df.groupby(["Owner", "Date"]).size().reset_index(name="Count")

chart = (
    alt.Chart(heatmap_data)
    .mark_rect()
    .encode(
        x="Date:T",
        y="Owner:N",
        color="Count:Q",
        tooltip=["Owner", "Date", "Count"]
    )
    .properties(height=400)
)

st.altair_chart(chart, use_container_width=True)

# -----------------------------
# HEATMAP 2 — ROOT CAUSE FREQUENCY
# -----------------------------
st.subheader("🧠 Root Cause Frequency Heatmap")

df["RootCauseCategory"] = df["RootCause"].apply(lambda x: x.split()[0] if isinstance(x, str) else "Unknown")

root_data = df.groupby(["Owner", "RootCauseCategory"]).size().reset_index(name="Count")

chart2 = (
    alt.Chart(root_data)
    .mark_rect()
    .encode(
        x="RootCauseCategory:N",
        y="Owner:N",
        color="Count:Q",
        tooltip=["Owner", "RootCauseCategory", "Count"]
    )
    .properties(height=400)
)

st.altair_chart(chart2, use_container_width=True)
