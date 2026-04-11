import streamlit as st
import sqlite3
import json
from datetime import datetime

st.set_page_config(page_title="Operator Entry", layout="wide")

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

st.title("📥 Daily Operator Entry")

# -----------------------------
# FORM INPUTS
# -----------------------------
with st.form("entry_form"):

    st.subheader("Production Metrics")
    date = st.date_input("Date")
    shift = st.selectbox("Shift", ["1", "2", "3"])
    units = st.number_input("Units Produced", min_value=0.0)
    orders = st.number_input("Orders Processed", min_value=0.0)
    labor = st.number_input("Labor Hours", min_value=0.0)

    st.subheader("Budget vs Actual Cost Categories")
    cost_items = ["Labor", "Equipment", "Supplies", "Transportation", "Admin"]
    budget = {}
    actual = {}
    variance = {}

    for item in cost_items:
        col1, col2 = st.columns(2)
        with col1:
            budget[item] = st.number_input(f"Budgeted {item} Cost", min_value=0.0, key=f"b_{item}")
        with col2:
            actual[item] = st.number_input(f"Actual {item} Cost", min_value=0.0, key=f"a_{item}")

        variance[item] = actual[item] - budget[item]

    st.subheader("Trailer / Inbound / Outbound Metrics")
    inbound = st.number_input("Inbound Loads", min_value=0.0)
    outbound = st.number_input("Outbound Loads", min_value=0.0)
    detention = st.number_input("Detention Fees", min_value=0.0)
    lumper = st.number_input("Lumper Fees", min_value=0.0)
    pallets = st.number_input("Pallet Costs", min_value=0.0)

    submitted = st.form_submit_button("Save Record")

# -----------------------------
# SAVE RECORD
# -----------------------------
if submitted:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    data = {
        "Budget_Labor": budget["Labor"],
        "Actual_Labor": actual["Labor"],
        "Variance_Labor": variance["Labor"],

        "Budget_Equipment": budget["Equipment"],
        "Actual_Equipment": actual["Equipment"],
        "Variance_Equipment": variance["Equipment"],

        "Budget_Supplies": budget["Supplies"],
        "Actual_Supplies": actual["Supplies"],
        "Variance_Supplies": variance["Supplies"],

        "Budget_Transportation": budget["Transportation"],
        "Actual_Transportation": actual["Transportation"],
        "Variance_Transportation": variance["Transportation"],

        "Budget_Admin": budget["Admin"],
        "Actual_Admin": actual["Admin"],
        "Variance_Admin": variance["Admin"],

        "Actual_Inbound Loads": inbound,
        "Actual_Outbound Loads": outbound,
        "Actual_Detention Fees": detention,
        "Actual_Lumper Fees": lumper,
        "Actual_Pallet Costs": pallets
    }

    cursor.execute("""
        INSERT INTO records VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        timestamp,
        str(date),
        shift,
        units,
        orders,
        labor,
        json.dumps(data)
    ))

    conn.commit()
    st.success("Record saved successfully!")

