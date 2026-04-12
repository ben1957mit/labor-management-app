import streamlit as st
import sqlite3

st.title("Database Migration – Add Site Column")

conn = sqlite3.connect("daily_cost_records.db")
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE records ADD COLUMN Site TEXT")
    conn.commit()
    st.success("Site column added successfully!")
except Exception as e:
    st.info("Migration already applied or not needed.")
    st.write(e)

