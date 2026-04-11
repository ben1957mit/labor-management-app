import streamlit as st
import pandas as pd
import altair as alt
import sqlite3
import os

st.set_page_config(page_title="Supervisor Dashboard", layout="wide")

DB_FILE = "daily_cost_records.db"

# -----------------------------
# DATABASE SETUP
# -----------------------------
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS records (
    Timestamp TEXT,
    Date TEXT,
    Shift TEXT,
    UnitsProduced REAL,
    OrdersProcessed REAL,
    LaborHours REAL,
    Data JSON
)
""")
conn.commit()

# -----------------------------
# SUPERVISOR PIN
# -----------------------------
st.sidebar.title("Supervisor Access")
pin = st.sidebar.text_input("Enter Supervisor PIN", type="password")
CORRECT_PIN = "1234"  # change this

if pin != CORRECT_PIN:
    st.warning("Supervisor PIN required.")
    st.stop()

st.title("🧑‍💼 Supervisor Dashboard")
st.write("Analyze trends, variances, KPIs, trailers, and labor standards.")

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_sql_query("SELECT * FROM records", conn)

if df.empty:
    st.warning("No data available yet. Operators must enter at least one day.")
    st.stop()

df["Date"] = pd.to_datetime(df["Date"])

# -----------------------------
# UNPACK JSON FIELDS
# -----------------------------
import json

expanded_rows = []
for _, row in df.iterrows():
    base = {
        "Timestamp": row["Timestamp"],
        "Date": row["Date"],
        "Shift": row["Shift"],
        "Units Produced": row["UnitsProduced"],
        "Orders Processed": row["OrdersProcessed"],
        "Labor Hours": row["LaborHours"],
    }
    extra = json.loads(row["Data"])
    base.update(extra)
    expanded_rows.append(base)

df = pd.DataFrame(expanded_rows)

# -----------------------------
# LATEST DAY
# -----------------------------
latest = df.sort_values("Date").iloc[-1]

# -----------------------------
# LABOR STANDARDS
# -----------------------------
st.sidebar.markdown("### Labor Standards")
target_uph = st.sidebar.number_input("Target Units per Labor Hour", min_value=0.0, value=20.0, step=1.0)
target_oplh = st.sidebar.number_input("Target Orders per Labor Hour", min_value=0.0, value=8.0, step=0.5)

labor_hours = latest["Labor Hours"]
units = latest["Units Produced"]
orders = latest["Orders Processed"]

actual_uph = units / labor_hours if labor_hours > 0 else None
actual_oplh = orders / labor_hours if labor_hours > 0 else None

def kpi_color_emoji(actual, low, high):
    if actual is None:
        return "⚪"
    if actual < low:
        return "🟥"
    elif actual > high:
        return "🟩"
    else:
        return "🟨"

# -----------------------------
# SUMMARY METRICS
# -----------------------------
st.subheader("📊 Summary & Labor Standards")

col1, col2, col3 = st.columns(3)
col1.metric("Units Produced (Latest)", f"{units:,}")
col2.metric("Orders Processed (Latest)", f"{orders:,}")
col3.metric("Labor Hours (Latest)", f"{labor_hours:.2f}")

k1, k2 = st.columns(2)
if actual_uph is not None:
    k1.markdown(
        f"{kpi_color_emoji(actual_uph, target_uph * 0.8, target_uph)} "
        f"**Units per Labor Hour:** {actual_uph:.2f} (Target: {target_uph:.2f})"
    )
else:
    k1.markdown("⚪ **Units per Labor Hour:** N/A")

if actual_oplh is not None:
    k2.markdown(
        f"{kpi_color_emoji(actual_oplh, target_oplh * 0.8, target_oplh)} "
        f"**Orders per Labor Hour:** {actual_oplh:.2f} (Target: {target_oplh:.2f})"
    )
else:
    k2.markdown("⚪ **Orders per Labor Hour:** N/A")

st.markdown("---")

# -----------------------------
# VARIANCE TABLE
# -----------------------------
st.subheader("Variance by Cost Item (Latest Day)")

variance_cols = [c for c in df.columns if c.startswith("Variance_")]
latest_variances = latest[variance_cols].reset_index()
latest_variances.columns = ["Cost Item", "Variance"]
latest_variances["Cost Item"] = latest_variances["Cost Item"].str.replace("Variance_", "")

def color_variance(val):
    if val < -5:
        return "background-color: green; color: white"
    elif -5 <= val <= 5:
        return "background-color: yellow; color: black"
    else:
        return "background-color: red; color: white"

st.dataframe(latest_variances.style.applymap(color_variance, subset=["Variance"]), use_container_width=True)

st.markdown("---")

# -----------------------------
# TRAILER / INBOUND / OUTBOUND DASHBOARD
# -----------------------------
st.subheader("🚚 Inbound / Outbound / Trailer Dashboard")

inbound = latest.get("Actual_Inbound Loads", 0)
outbound = latest.get("Actual_Outbound Loads", 0)
detention = latest.get("Actual_Detention Fees", 0)
lumper = latest.get("Actual_Lumper Fees", 0)
pallets = latest.get("Actual_Pallet Costs", 0)

t1, t2, t3 = st.columns(3)
t1.metric("Inbound Loads", f"{inbound:.0f}")
t2.metric("Outbound Loads", f"{outbound:.0f}")
t3.metric("Detention Fees", f"${detention:,.2f}")

t4, t5 = st.columns(2)
t4.metric("Lumper Fees", f"${lumper:,.2f}")
t5.metric("Pallet Costs", f"${pallets:,.2f}")

st.markdown("---")

# -----------------------------
# TOP 3 OVER / UNDER BUDGET
# -----------------------------
st.subheader("🔺 Top 3 Over / Under Budget Items")

top3 = latest_variances.nlargest(3, "Variance")
bottom3 = latest_variances.nsmallest(3, "Variance")

colA, colB = st.columns(2)
colA.write("### Over Budget")
colA.dataframe(top3, use_container_width=True)

colB.write("### Under Budget")
colB.dataframe(bottom3, use_container_width=True)

st.markdown("---")

# -----------------------------
# TREND CHARTS
# -----------------------------
st.subheader("📈 Multi‑Day Trend Charts")

metric = st.selectbox(
    "Select Trend Metric",
    ["Units Produced", "Orders Processed"] + variance_cols
)

trend_chart = alt.Chart(df).mark_line(point=True).encode(
    x="Date:T",
    y=f"{metric}:Q",
    color=alt.value("#1f77b4")
).properties(height=350)

st.altair_chart(trend_chart, use_container_width=True)

st.markdown("---")

# -----------------------------
# EXPORT TO EXCEL
# -----------------------------
st.subheader("📤 Export Data")

excel_file = "daily_cost_records_export.xlsx"
df.to_excel(excel_file, index=False)

with open(excel_file, "rb") as f:
    st.download_button(
        label="Download All Records as Excel",
        data=f,
        file_name="daily_cost_records_export.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
