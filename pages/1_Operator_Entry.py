import streamlit as st
import sqlite3
import json
from datetime import datetime

st.set_page_config(page_title="Operator Entry", layout="wide")

DB_FILE = "daily_cost_records.db"

# ---------------------------------------------------
# DATABASE INITIALIZATION
# ---------------------------------------------------
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Records table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS records (
        Timestamp TEXT,
        Date TEXT,
        Shift TEXT,
        UnitsProduced REAL,
        OrdersProcessed REAL,
        LaborHours REAL,
        Data JSON,
        Site TEXT
    )
    """)

    # Sites table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sites (
        SiteName TEXT PRIMARY KEY
    )
    """)

    # Cost categories table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cost_categories (
        CategoryName TEXT PRIMARY KEY
    )
    """)

    # Default categories (only inserted if missing)
    cursor.executemany(
        "INSERT OR IGNORE INTO cost_categories VALUES (?)",
        [
            ("Labor",),
            ("Equipment",),
            ("Supplies",),
            ("Transportation",),
            ("Admin",)
        ]
    )

    conn.commit()
    return conn, cursor


# Initialize DB
conn, cursor = init_db()

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------
cursor.execute("SELECT SiteName FROM sites ORDER BY SiteName")
sites = [row[0] for row in cursor.fetchall()]

if not sites:
    sites = ["Dallas", "Plano", "Houston"]

cursor.execute("SELECT CategoryName FROM cost_categories ORDER BY CategoryName")
cost_items = [row[0] for row in cursor.fetchall()]

# ---------------------------------------------------
# PAGE TITLE
# ---------------------------------------------------
st.title("📥 Daily Operator Entry")

# ---------------------------------------------------
# ENTRY FORM
# ---------------------------------------------------
with st.form("entry_form"):

    st.subheader("Production Information")

    site = st.selectbox("Site", sites)
    date = st.date_input("Date")
    shift = st.selectbox("Shift", ["1", "2", "3"])

    units = st.number_input("Units Produced", min_value=0.0)
    orders = st.number_input("Orders Processed", min_value=0.0)
    labor = st.number_input("Labor Hours", min_value=0.0)

    # ---------------------------------------------------
    # COST CATEGORIES (DYNAMIC)
    # ---------------------------------------------------
    st.subheader("Budget vs Actual Cost Categories")

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

    # ---------------------------------------------------
    # TRAILER METRICS
    # ---------------------------------------------------
    st.subheader("Trailer / Inbound / Outbound Metrics")

    inbound = st.number_input("Inbound Loads", min_value=0.0)
    outbound = st.number_input("Outbound Loads", min_value=0.0)
    detention = st.number_input("Detention Fees", min_value=0.0)
    lumper = st.number_input("Lumper Fees", min_value=0.0)
    pallets = st.number_input("Pallet Costs", min_value=0.0)

    submitted = st.form_submit_button("Save Record")

# ---------------------------------------------------
# SAVE RECORD
# ---------------------------------------------------
if submitted:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Build JSON payload dynamically
    data = {}

    for item in cost_items:
        data[f"Budget_{item}"] = budget[item]
        data[f"Actual_{item}"] = actual[item]
        data[f"Variance_{item}"] = variance[item]

    data.update({
        "Actual_Inbound Loads": inbound,
        "Actual_Outbound Loads": outbound,
        "Actual_Detention Fees": detention,
        "Actual_Lumper Fees": lumper,
        "Actual_Pallet Costs": pallets
    })

    cursor.execute("""
        INSERT INTO records VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        timestamp,
        str(date),
        shift,
        units,
        orders,
        labor,
        json.dumps(data),
        site
    ))

    conn.commit()
    st.success("Record saved successfully!")
