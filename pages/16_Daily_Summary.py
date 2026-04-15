import streamlit as st
import pandas as pd
import json
from database_init import init_db

st.set_page_config(page_title="Daily Summary", layout="wide")

conn, cursor = init_db()

st.title("📅 Daily Summary")

cursor.execute("SELECT DISTINCT Date FROM records ORDER BY Date DESC")
dates = [row[0] for row in cursor.fetchall()]

if not dates:
    st.info("No records available")
    st.stop()

selected_date = st.selectbox("Select Date", dates)

cursor.execute("SELECT * FROM records WHERE Date = ?", (selected_date,))
rows = cursor.fetchall()

col_names = [desc[0] for desc in cursor.description]
df = pd.DataFrame(rows, columns=col_names)

df["Data"] = df["Data"].apply(lambda x: json.loads(x))
json_df = df["Data"].apply(pd.Series)
full_df = pd.concat([df.drop(columns=["Data"]), json_df], axis=1)

st.subheader("Production Summary")
st.write(full_df[["UnitsProduced", "OrdersProcessed", "LaborHours"]].sum())

st.subheader("Cost Summary")
cost_cols = [c for c in full_df.columns if c.startswith("Actual_")]
st.write(full_df[cost_cols].sum())
import io

st.subheader("Export Data")

csv = full_df.to_csv(index=False).encode("utf-8")
st.download_button("Download CSV", csv, "data.csv", "text/csv")

excel_buffer = io.BytesIO()
full_df.to_excel(excel_buffer, index=False)
st.download_button("Download Excel", excel_buffer.getvalue(), "data.xlsx")
