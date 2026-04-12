import streamlit as st
import pandas as pd
import sqlite3
import json
from datetime import datetime

st.set_page_config(page_title="PDF Report Generator", layout="wide")

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
# PAGE UI
# -----------------------------
st.title("📄 PDF Report Generator")

report_type = st.selectbox("Select Report Type", ["Weekly Summary", "Monthly Summary"])

# -----------------------------
# WEEKLY REPORT
# -----------------------------
if report_type == "Weekly Summary":
    df["Week"] = df["Date"].dt.isocalendar().week
    selected_week = st.selectbox("Select Week", df["Week"].unique())

    report_df = df[df["Week"] == selected_week]
    title = f"Weekly Summary Report – Week {selected_week}"

# -----------------------------
# MONTHLY REPORT
# -----------------------------
else:
    df["Month"] = df["Date"].dt.month
    df["Month Name"] = df["Date"].dt.strftime("%B")
    selected_month = st.selectbox("Select Month", df["Month Name"].unique())

    report_df = df[df["Month Name"] == selected_month]
    title = f"Monthly Summary Report – {selected_month}"

# -----------------------------
# BUILD HTML REPORT
# -----------------------------
total_units = report_df["Units Produced"].sum()
total_orders = report_df["Orders Processed"].sum()
total_labor = report_df["Labor Hours"].sum()

cost_cols = [c for c in df.columns if c.startswith("Budget_") or c.startswith("Actual_") or c.startswith("Variance_")]
cost_summary = report_df[cost_cols].sum(numeric_only=True)

trailer_cols = [
    "Actual_Inbound Loads",
    "Actual_Outbound Loads",
    "Actual_Detention Fees",
    "Actual_Lumper Fees",
    "Actual_Pallet Costs"
]
trailer_summary = report_df[trailer_cols].sum(numeric_only=True)

html = f"""
<h1>{title}</h1>
<h3>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</h3>

<h2>Production Summary</h2>
<ul>
    <li><b>Total Units:</b> {total_units:,.0f}</li>
    <li><b>Total Orders:</b> {total_orders:,.0f}</li>
    <li><b>Total Labor Hours:</b> {total_labor:,.2f}</li>
</ul>

<h2>Cost Summary</h2>
{cost_summary.to_frame().to_html()}

<h2>Trailer Summary</h2>
{trailer_summary.to_frame().to_html()}
"""

# -----------------------------
# EXPORT HTML (Always Works)
# -----------------------------
st.subheader("📤 Export Report")

html_bytes = html.encode("utf-8")

st.download_button(
    label="Download HTML Report",
    data=html_bytes,
    file_name="report.html",
    mime="text/html",
)

st.info("PDF export can be added if your environment supports pdfkit + wkhtmltopdf.")

