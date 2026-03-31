import streamlit as st
import pandas as pd
from data_utils import read_rows

st.title("📊 Reports & Charts")

rows = read_rows("performance_history.csv")

if not rows:
    st.info("No performance data available yet.")
else:
    df = pd.DataFrame(rows)
    df["uph"] = df["uph"].astype(float)
    df["productivity"] = df["productivity"].astype(float)
    df["variance"] = df["variance"].astype(float)

    st.subheader("UPH by Entry")
    st.line_chart(df["uph"])

    st.subheader("Productivity (%) by Entry")
    prod_df = df.copy()
    prod_df["productivity_pct"] = prod_df["productivity"] * 100
    st.line_chart(prod_df["productivity_pct"])

    st.subheader("Variance (UPH) by Entry")
    st.bar_chart(df["variance"])
