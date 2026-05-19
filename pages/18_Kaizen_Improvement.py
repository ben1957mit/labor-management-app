import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
import json
import os

st.set_page_config(page_title="Kaizen Improvement", layout="wide")

DB_FILE = "kaizen_records.db"

# -----------------------------
# DATABASE SETUP
# -----------------------------
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS kaizen (
    Timestamp TEXT,
    Owner TEXT,
    Problem TEXT,
    CurrentState TEXT,
    RootCause TEXT,
    FiveWhys TEXT,
    Fishbone TEXT,
    Countermeasure TEXT,
    FutureState TEXT,
    BeforeMetrics TEXT,
    AfterMetrics TEXT,
    Sustainment TEXT,
    SupervisorNotes TEXT
)
""")
conn.commit()

st.title("🛠️ Kaizen Improvement (Accelerated Solo Process)")
st.write("Use this page to run a complete Kaizen cycle as a single individual in an accelerated environment.")

# -----------------------------
# SECTION 1 — OWNER + PROBLEM
# -----------------------------
st.header("1️⃣ Problem Definition")

owner = st.text_input("Your Name")
problem = st.text_area("Problem Statement (What is happening vs what should be happening?)", height=120)
current_state = st.text_area("Current State (Describe the process as it exists today)", height=120)

st.markdown("---")

# -----------------------------
# SECTION 2 — ROOT CAUSE
# -----------------------------
st.header("2️⃣ Root Cause Analysis")

root_cause = st.text_area("Primary Root Cause (What is the true cause you can control?)", height=100)

st.subheader("5 Whys")
five_whys = st.text_area("Document your 5 Whys here:", height=150)

st.subheader("Mini Fishbone (People, Process, Tools, Environment)")
fishbone = st.text_area("List contributing factors:", height=150)

st.markdown("---")

# -----------------------------
# SECTION 3 — COUNTERMEASURE
# -----------------------------
st.header("3️⃣ Countermeasure Design")

countermeasure = st.text_area("Countermeasure (What action will remove the root cause?)", height=150)
future_state = st.text_area("Future State (Describe the improved process)", height=150)

st.markdown("---")

# -----------------------------
# SECTION 4 — BEFORE / AFTER METRICS
# -----------------------------
st.header("4️⃣ Before & After Metrics")

col1, col2 = st.columns(2)

with col1:
    before_metrics = st.text_area("Before Metrics (UPH, travel time, errors, cost/unit, etc.)", height=150)

with col2:
    after_metrics = st.text_area("After Metrics (Measured after implementation)", height=150)

st.markdown("---")

# -----------------------------
# SECTION 5 — SUSTAINMENT
# -----------------------------
st.header("5️⃣ Sustainment Plan")

sustainment = st.text_area("How will you lock in the improvement? (SOP updates, visuals, audits, training)", height=150)

st.markdown("---")

# -----------------------------
# SECTION 6 — SUPERVISOR REVIEW
# -----------------------------
st.header("🧑‍💼 Supervisor Review (Optional)")

supervisor_notes = st.text_area("Supervisor Notes / Approval", height=120)

st.markdown("---")

# -----------------------------
# SAVE KAIZEN RECORD
# -----------------------------
def build_record():
    return {
        "Timestamp": datetime.now().isoformat(),
        "Owner": owner,
        "Problem": problem,
        "CurrentState": current_state,
        "RootCause": root_cause,
        "FiveWhys": five_whys,
        "Fishbone": fishbone,
        "Countermeasure": countermeasure,
        "FutureState": future_state,
        "BeforeMetrics": before_metrics,
        "AfterMetrics": after_metrics,
        "Sustainment": sustainment,
        "SupervisorNotes": supervisor_notes
    }

if st.button("Save Kaizen Record"):
    row = build_record()
    cursor.execute("""
        INSERT INTO kaizen VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, tuple(row.values()))
    conn.commit()
    st.success("Kaizen record saved successfully.")

# -----------------------------
# VIEW SAVED KAIZENS
# -----------------------------
st.markdown("---")
st.header("📁 Saved Kaizen Records")

df = pd.read_sql_query("SELECT * FROM kaizen", conn)

if not df.empty:
    st.dataframe(df, use_container_width=True)
else:
    st.info("No Kaizen records saved yet.")
