import streamlit as st
import pandas as pd
import sqlite3
import altair as alt

st.set_page_config(page_title="Kaizen Dashboard", layout="wide")

DB_FILE = "kaizen_records.db"

# -----------------------------
# LOAD DATA
# -----------------------------
conn = sqlite3.connect(DB_FILE)
df = pd.read_sql_query("SELECT * FROM kaizen", conn)

st.title("📊 Kaizen Dashboard")
st.write("Visualize trends, performance gains, and improvement activity across the organization.")

if df.empty:
    st.warning("No Kaizen records found. Add some improvements first.")
    st.stop()

# Convert timestamp
df["Timestamp"] = pd.to_datetime(df["Timestamp"])

# -----------------------------
# FILTERS
# -----------------------------
st.sidebar.header("Filters")

owners = st.sidebar.multiselect("Filter by Owner", df["Owner"].unique())
if owners:
    df = df[df["Owner"].isin(owners)]

date_range = st.sidebar.date_input(
    "Date Range",
    value=[df["Timestamp"].min(), df["Timestamp"].max()]
)

if len(date_range) == 2:
    start, end = date_range
    df = df[(df["Timestamp"] >= pd.to_datetime(start)) & (df["Timestamp"] <= pd.to_datetime(end))]

st.markdown("---")

# -----------------------------
# METRICS SUMMARY
# -----------------------------
col1, col2, col3 = st.columns(3)

col1.metric("Total Kaizens", len(df))
col2.metric("Unique Owners", df["Owner"].nunique())
col3.metric("Avg. Kaizens per Owner", round(len(df) / max(df["Owner"].nunique(), 1), 2))

st.markdown("---")

# -----------------------------
# CHART 1 — KAIZENS OVER TIME
# -----------------------------
st.subheader("📈 Kaizens Over Time")

kaizen_over_time = (
    df.groupby(df["Timestamp"].dt.date)
    .size()
    .reset_index(name="Count")
)

chart1 = (
    alt.Chart(kaizen_over_time)
    .mark_line(point=True)
    .encode(
        x="Timestamp:T",
        y="Count:Q",
        tooltip=["Timestamp:T", "Count:Q"]
    )
    .properties(height=300)
)

st.altair_chart(chart1, use_container_width=True)

# -----------------------------
# CHART 2 — KAIZENS BY OWNER
# -----------------------------
st.subheader("👤 Kaizens by Owner")

kaizen_by_owner = df.groupby("Owner").size().reset_index(name="Count")

chart2 = (
    alt.Chart(kaizen_by_owner)
    .mark_bar()
    .encode(
        x="Owner:N",
        y="Count:Q",
        tooltip=["Owner:N", "Count:Q"],
        color="Owner:N"
    )
    .properties(height=300)
)

st.altair_chart(chart2, use_container_width=True)

# -----------------------------
# CHART 3 — BEFORE VS AFTER METRICS
# -----------------------------
st.subheader("📉 Before vs After Metrics (Text-Based Comparison)")

def extract_number(text):
    try:
        return float(text)
    except:
        return None

df["BeforeValue"] = df["BeforeMetrics"].apply(extract_number)
df["AfterValue"] = df["AfterMetrics"].apply(extract_number)
df_valid = df.dropna(subset=["BeforeValue", "AfterValue"])

if not df_valid.empty:
    df_valid["Delta"] = df_valid["AfterValue"] - df_valid["BeforeValue"]

    chart3 = (
        alt.Chart(df_valid)
        .mark_bar()
        .encode(
            x="Owner:N",
            y="Delta:Q",
            color=alt.condition("datum.Delta < 0", alt.value("green"), alt.value("red")),
            tooltip=["Owner", "BeforeValue", "AfterValue", "Delta"]
        )
        .properties(height=300)
    )

    st.altair_chart(chart3, use_container_width=True)
else:
    st.info("No numeric before/after metrics available to chart.")

# -----------------------------
# TABLE VIEW
# -----------------------------
st.markdown("---")
st.subheader("📁 Full Kaizen Table")

st.dataframe(df, use_container_width=True)
