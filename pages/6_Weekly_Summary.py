import streamlit as st
import pandas as pd
import sqlite3
import json
import altair as alt

st.set_page_config(page_title="Weekly Summary", layout="wide")

DB_FILE = "daily_cost_records.db"

# -----------------------------
# LOAD DATA
# -----------------------------
conn = sqlite3.connect(DB_FILE)
df = pd.read_sql_query("SELECT * FROM records", conn)

if df.empty:
    st.info("No data available yet. Enter data on the Operator Entry page.")
    st.stop()

df["Date"] = pd.to_datetime(df["Date"])

# -----------------------------
# UNPACK JSON FIELDS
# -----------------------------
expanded_rows = []
for _, row in df.iterrows():
    base = {
        "Date": row["Date"],
        "Units Produced": row["UnitsProduced"],
        "Orders Processed": row["OrdersProcessed"],
        "Labor Hours": row["LaborHours"],
    }
    try:
        extra = json.loads(row["Data"])
        base.update(extra)
    except:
        pass
    expanded_rows.append(base)

df = pd.DataFrame(expanded_rows)

# -----------------------------
# WEEKLY GROUPING
# -----------------------------
df["Week"] = df["Date"].dt.isocalendar().week
weekly = df.groupby("Week").sum(numeric_only=True).reset_index()

st.title("📅 Weekly Summary Report")

# -----------------------------
# WEEK SELECTOR
# -----------------------------
selected_week = st.selectbox("Select Week Number", weekly["Week"].unique())

week_df = df[df["Week"] == selected_week]

st.subheader(f"📊 Summary for Week {selected_week}")

col1, col2, col3 = st.columns(3)
col1.metric("Total Units", f"{week_df['Units Produced'].sum():,.0f}")
col2.metric("Total Orders", f"{week_df['Orders Processed'].sum():,.0f}")
col3.metric("Total Labor Hours", f"{week_df['Labor Hours'].sum():,.2f}")

# -----------------------------
# COST SUMMARY
# -----------------------------
st.subheader("💰 Weekly Cost Summary")

cost_cols = [c for c in df.columns if c.startswith("Budget_") or c.startswith("Actual_") or c.startswith("Variance_")]

weekly_costs = week_df[cost_cols].sum(numeric_only=True).reset_index()
weekly_costs.columns = ["Cost Category", "Total"]

st.dataframe(weekly_costs, use_container_width=True)

# -----------------------------
# TRAILER SUMMARY
# -----------------------------
st.subheader("🚚 Trailer Activity Summary")

trailer_cols = [
    "Actual_Inbound Loads",
    "Actual_Outbound Loads",
    "Actual_Detention Fees",
    "Actual_Lumper Fees",
    "Actual_Pallet Costs"
]

trailer_summary = week_df[trailer_cols].sum(numeric_only=True).reset_index()
trailer_summary.columns = ["Trailer Metric", "Total"]

st.dataframe(trailer_summary, use_container_width=True)

# -----------------------------
# TREND CHARTS
# -----------------------------
st.subheader("📈 Weekly Trend Charts")

metric = st.selectbox("Select Metric", ["Units Produced", "Orders Processed", "Labor Hours"])

chart = alt.Chart(weekly).mark_line(point=True).encode(
    x="Week:O",
    y=f"{metric}:Q",
    color=alt.value("#1f77b4")
).properties(height=350)

st.altair_chart(chart, use_container_width=True)

