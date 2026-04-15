import streamlit as st
import pandas as pd
import json
from database_init import init_db

st.set_page_config(page_title="Dynamic Dashboard", layout="wide")

conn, cursor = init_db()

st.title("📈 Dynamic Dashboard")

# Load records
cursor.execute("SELECT * FROM records")
rows = cursor.fetchall()

col_names = [desc[0] for desc in cursor.description]
df = pd.DataFrame(rows, columns=col_names)

if df.empty:
    st.info("No records found yet")
    st.stop()

# Expand JSON
df["Data"] = df["Data"].apply(lambda x: json.loads(x))

# Convert JSON keys into columns
json_df = df["Data"].apply(pd.Series)

# Merge with main df
full_df = pd.concat([df.drop(columns=["Data"]), json_df], axis=1)

# Load categories
cursor.execute("SELECT CategoryName FROM cost_categories ORDER BY CategoryName")
categories = [row[0] for row in cursor.fetchall()]

# Build dynamic charts
for cat in categories:
    budget_col = f"Budget_{cat}"
    actual_col = f"Actual_{cat}"

    if budget_col in full_df.columns and actual_col in full_df.columns:
        st.subheader(f"{cat} Cost Overview")

        chart_df = full_df[[budget_col, actual_col]].copy()
        chart_df.columns = ["Budget", "Actual"]

        st.line_chart(chart_df)
