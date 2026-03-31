import streamlit as st
from datetime import datetime
from data_utils import append_row, read_rows, today_str

st.title("🧑‍🏫 Coaching Log")

st.subheader("Add Coaching Entry")

employee = st.text_input("Employee Name")
issue_type = st.selectbox("Issue Type", ["Performance", "Attendance", "Quality", "Safety", "Behavior", "Other"])
notes = st.text_area("Coaching Notes")
supervisor = st.text_input("Supervisor Name")
follow_up = st.date_input("Follow-up Date", datetime.today())

if st.button("Save Coaching Entry"):
    row = {
        "date": today_str(),
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "employee": employee,
        "issue_type": issue_type,
        "notes": notes,
        "supervisor": supervisor,
        "follow_up": follow_up.isoformat(),
    }
    append_row("coaching_log.csv", list(row.keys()), row)
    st.success("Coaching entry saved to coaching_log.csv")

st.divider()
st.subheader("Coaching Log History")

rows = read_rows("coaching_log.csv")
if rows:
    st.dataframe(rows, use_container_width=True)
else:
    st.info("No coaching entries recorded yet.")
