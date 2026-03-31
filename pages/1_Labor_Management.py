import streamlit as st
from datetime import datetime
from data_utils import append_row, today_str

st.set_page_config(page_title="Labor Management", layout="wide")

st.title("📊 Labor Management Dashboard")
st.markdown("Use this tool to calculate productivity, staffing needs, and performance using industrial engineering standards.")

st.divider()

# Supervisor mode toggle
supervisor_mode = st.toggle("🔐 Supervisor Mode", value=True)

# -----------------------------
# INPUT SECTIONS
# -----------------------------
st.header("🧮 Input Data")

col1, col2 = st.columns(2)

with col1:
    if supervisor_mode:
        st.subheader("Supervisor Inputs")
        observed_time = st.number_input("Observed Time per Unit (seconds)", min_value=0.0, step=0.1)
        rating = st.number_input("Performance Rating (%)", min_value=0.0, max_value=200.0, step=1.0)
        allowance = st.number_input("Allowance (%)", min_value=0.0, max_value=50.0, step=1.0) / 100
        demand = st.number_input("Daily Demand (units)", min_value=0, step=1)
    else:
        observed_time = 0.0
        rating = 0.0
        allowance = 0.0
        demand = 0

with col2:
    st.subheader("Labor Inputs")
    available_minutes = st.number_input("Available Minutes per Worker", min_value=0, step=1)
    workers = st.number_input("Number of Workers", min_value=0, step=1)
    labor_cost = st.number_input("Labor Cost per Hour ($)", min_value=0.0, step=0.5)
    target_util = st.number_input("Target Utilization (%)", min_value=0.0, max_value=150.0, step=1.0)

st.divider()

# -----------------------------
# EMPLOYEE INPUTS
# -----------------------------
st.header("👷 Employee Inputs")

col3, col4 = st.columns(2)

with col3:
    employee_name = st.text_input("Employee Name")
    hours_worked = st.number_input("Hours Worked", min_value=0.0, step=0.25)
with col4:
    units_completed = st.number_input("Units Completed", min_value=0, step=1)

notes = st.text_area("Notes (barriers, equipment issues, coaching, training needs)")

st.divider()

# -----------------------------
# CALCULATIONS
# -----------------------------
st.header("📈 Results")

can_calc_supervisor = supervisor_mode and observed_time > 0 and rating > 0 and demand > 0
can_calc_employee = hours_worked > 0 and units_completed > 0

normal_time = standard_time = required_hours = available_hours = utilization = daily_cost = 0
uph = target_uph = productivity = variance = 0

if can_calc_supervisor:
    normal_time = observed_time * (rating / 100)
    standard_time = normal_time / (1 - allowance) if (1 - allowance) > 0 else 0
    required_hours = (demand * standard_time) / 3600
    available_hours = workers * (available_minutes / 60) if available_minutes > 0 else 0
    utilization = required_hours / available_hours if available_hours > 0 else 0
    daily_cost = available_hours * labor_cost

if can_calc_employee and standard_time > 0:
    uph = units_completed / hours_worked
    target_uph = 3600 / standard_time
    productivity = uph / target_uph if target_uph > 0 else 0
    variance = uph - target_uph

if not can_calc_supervisor:
    st.info("Enter supervisor inputs in Supervisor Mode to calculate IE-based results.")

if can_calc_employee and standard_time == 0 and supervisor_mode:
    st.warning("Standard time is zero — check observed time, rating, and allowance.")

if can_calc_employee:
    colA, colB, colC = st.columns(3)

    with colA:
        st.metric("Units per Hour", f"{uph:.2f}")
        st.metric("Target UPH", f"{target_uph:.2f}")
    with colB:
        st.metric("Productivity (%)", f"{productivity*100:.1f}%")
        st.metric("Variance (UPH)", f"{variance:.2f}")
    with colC:
        # Badge
        if productivity >= 1.05:
            st.success("🟢 Above Target")
        elif 0.95 <= productivity < 1.05:
            st.warning("🟡 Near Target")
        else:
            st.error("🔴 Below Target")

if can_calc_supervisor:
    st.subheader("Supervisor Metrics")
    colS1, colS2, colS3 = st.columns(3)
    with colS1:
        st.metric("Normal Time (sec)", f"{normal_time:.2f}")
        st.metric("Standard Time (sec)", f"{standard_time:.2f}")
    with colS2:
        st.metric("Required Labor Hours", f"{required_hours:.2f}")
        st.metric("Available Labor Hours", f"{available_hours:.2f}")
    with colS3:
        st.metric("Utilization (%)", f"{utilization*100:.1f}%")
        st.metric("Daily Labor Cost", f"${daily_cost:,.2f}")

st.divider()

# -----------------------------
# SAVE / EXPORT
# -----------------------------
st.header("💾 Save & Export")

if st.button("Save Entry to CSV") and can_calc_employee:
    row = {
        "date": today_str(),
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "employee_name": employee_name,
        "hours_worked": hours_worked,
        "units_completed": units_completed,
        "uph": uph,
        "target_uph": target_uph,
        "productivity": productivity,
        "variance": variance,
        "observed_time": observed_time,
        "rating": rating,
        "allowance": allowance,
        "demand": demand,
        "available_minutes": available_minutes,
        "workers": workers,
        "labor_cost": labor_cost,
        "required_hours": required_hours,
        "available_hours": available_hours,
        "utilization": utilization,
        "daily_cost": daily_cost,
        "notes": notes,
    }
    append_row(
        "performance_history.csv",
        fieldnames=list(row.keys()),
        row=row,
    )
    st.success("Entry saved to performance_history.csv")

st.caption("Performance data is stored in data/performance_history.csv")

st.divider()

st.header("📝 Notes & Observations")
st.write(notes if notes else "No notes entered.")
