import streamlit as st
import pandas as pd
import sqlite3
from fpdf import FPDF

st.set_page_config(page_title="Kaizen PDF Export", layout="wide")

DB_FILE = "kaizen_records.db"
conn = sqlite3.connect(DB_FILE)

st.title("🧾 Kaizen PDF Export")

df = pd.read_sql_query("SELECT rowid, * FROM kaizen", conn)

if df.empty:
    st.warning("No Kaizen records found.")
    st.stop()

kaizen_id = st.selectbox("Select a Kaizen to Export", df["rowid"])

record = df[df["rowid"] == kaizen_id].iloc[0]

if st.button("Generate PDF"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Kaizen Report", ln=True, align="C")
    pdf.ln(5)

    for col in df.columns:
        if col == "rowid":
            continue
        pdf.multi_cell(0, 10, f"{col}: {record[col]}")
        pdf.ln(1)

    filename = f"Kaizen_{kaizen_id}.pdf"
    pdf.output(filename)

    with open(filename, "rb") as f:
        st.download_button("Download PDF", f, file_name=filename)

    st.success("PDF generated successfully.")
