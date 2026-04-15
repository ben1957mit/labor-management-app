import streamlit as st
import pandas as pd
import json
from database_init import init_db

st.set_page_config(page_title="Database Viewer", layout="wide")

conn, cursor = init_db()

st.title("📊 Database Viewer")

# Available tables
tables = ["records", "sites", "cost_categories"]

selected_table = st.selectbox("Select a table to view", tables)

cursor.execute(f"SELECT * FROM {selected_table}")
rows = cursor.fetchall()

col_names = [desc[0] for desc in cursor.description]
df = pd.DataFrame(rows, columns=col_names)

# Expand JSON column for records
if selected_table == "records" and "Data" in df.columns:
    df["Data"] = df["Data"].apply(lambda x: json.loads(x) if x else {})

st.dataframe(df, use_container_width=True)
