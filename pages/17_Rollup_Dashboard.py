import streamlit as st
import pandas as pd
import json
from database_init import init_db

st.set_page_config(page_title="Rollup Dashboard", layout="wide")

conn, cursor = init_db()

st.title("📊 Weekly / Monthly Rollup Dashboard")

cursor.execute("SELECT * FROM records")
rows = cursor.fetchall()

col_names = [desc[0] for desc in cursor.description]
df = pd.DataFrame(rows, columns=col_names)

if df.empty:
    st.info("No data available")
    st.stop()

df["Data"] = df["Data"].apply(lambda x: json.loads(x))
json_df = df["Data"].apply(pd.Series)
full_df = pd.concat([df.drop(columns=["Data"]), json_df], axis=1)

full_df["Date"] = pd.to_datetime(full_df["Date"])
full_df["Week"] = full_df["Date"].dt.isocalendar().week
full_df["Month"] = full_df["Date"].dt.month

rollup_type = st.radio("Rollup Type", ["Weekly", "Monthly"])

group_col = "Week" if rollup_type == "Weekly" else "Month"

cost_cols = [c for c in full_df.columns if c.startswith("Actual_")]

rollup_df = full_df.groupby(group_col)[cost_cols].sum()

st.dataframe(rollup_df, use_container_width=True)
