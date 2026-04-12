import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Site Management", layout="wide")

st.title("🏭 Multi‑Site Management")

conn = sqlite3.connect("daily_cost_records.db")
df = pd.read_sql_query("SELECT DISTINCT Site FROM records", conn)

st.subheader("Existing Sites")
st.dataframe(df)

st.subheader("Add New Site")

new_site = st.text_input("Site Name")

if st.button("Add Site"):
    if new_site.strip() == "":
        st.warning("Site name cannot be empty.")
    else:
        st.success(f"Site '{new_site}' added! (Note: This only updates the selector list.)")
