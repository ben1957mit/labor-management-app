import streamlit as st
import pandas as pd
import sqlite3
from datetime import date

st.set_page_config(page_title="Kaizen Task Tracker", layout="wide")

DB_FILE = "kaizen_records.db"
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS kaizen_tasks (
    TaskID INTEGER PRIMARY KEY AUTOINCREMENT,
    KaizenID INTEGER,
    Task TEXT,
    Owner TEXT,
    DueDate TEXT,
    Status TEXT
)
""")
conn.commit()

st.title("📋 Kaizen Task Tracker")

df_kaizen = pd.read_sql_query("SELECT rowid, * FROM kaizen", conn)

kaizen_id = st.selectbox("Link Task to Kaizen", df_kaizen["rowid"])

task = st.text_input("Task Description")
owner = st.text_input("Task Owner")
due_date = st.date_input("Due Date", value=date.today())
status = st.selectbox("Status", ["Not Started", "In Progress", "Completed"])

if st.button("Add Task"):
    cursor.execute("""
        INSERT INTO kaizen_tasks (KaizenID, Task, Owner, DueDate, Status)
        VALUES (?, ?, ?, ?, ?)
    """, (kaizen_id, task, owner, due_date.isoformat(), status))
    conn.commit()
    st.success("Task added successfully.")

st.markdown("---")
st.subheader("📁 All Tasks")

df_tasks = pd.read_sql_query("SELECT * FROM kaizen_tasks", conn)
st.dataframe(df_tasks, use_container_width=True)
