import streamlit as st
import sqlite3
import pandas as pd
import json

st.title("Database Debug Viewer")

conn = sqlite3.connect("daily_cost_records.db")
df = pd.read_sql_query("SELECT * FROM records", conn)

st.write("Raw Table:")
st.dataframe(df)

st.write("Expanded JSON:")
expanded = []
for _, row in df.iterrows():
    base = dict(row)
    try:
        extra = json.loads(row["Data"])
        base.update(extra)
    except:
        pass
    expanded.append(base)

st.dataframe(pd.DataFrame(expanded))
