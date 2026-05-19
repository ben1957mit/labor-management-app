import streamlit as st
import pandas as pd
import sqlite3
from fpdf import FPDF

st.set_page_config(page_title="Kaizen PDF Export", layout="wide")

DB_FILE = "kaizen_records.db"

# -----------------------------
# LOAD DATA
# -----------------------------
conn = sqlite3.connect(DB_FILE)
df = pd.read_sql_query("SELECT rowid, * FROM kaizen", conn)

st.title("🧾 Kaizen PDF Export")

if df.empty:
    st.warning("No Kaizen records found.")
    st.stop()

# -----------------------------
# SELECT KAIZEN RECORD
# -----------------------------
kaizen_id = st.selectbox("Select a Kaizen to Export", df["rowid"])
record = df[df["rowid"] == kaizen_id].iloc[0]

# -----------------------------
# PDF GENERATION FUNCTION
# -----------------------------
def generate_pdf(record, kaizen_id):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    # Title
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Kaizen Report", ln=True, align="C")
    pdf.ln(5)

    # Body
    pdf.set_font("Arial", size=12)
    for col in record.index:
        if col == "rowid":
            continue
        text = f"{col}: {record[col]}"
        pdf.multi_cell(0, 10, text)
        pdf.ln(1)

    filename = f"Kaizen_{kaizen_id}.pdf"
    pdf.output(filename)
    return filename

# -----------------------------
# EXPORT BUTTON
# -----------------------------
if st.button("Generate PDF"):
    filename = generate_pdf(record, kaizen_id)

    with open(filename, "rb") as f:
        st.download_button(
            label="Download PDF",
            data=f,
            file_name=filename,
            mime="application/pdf"
        )

    st.success("PDF generated successfully.")
