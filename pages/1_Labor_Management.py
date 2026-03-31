import streamlit as st

st.set_page_config(page_title="Labor Management", layout="wide")

# -----------------------------
# PAGE HEADER
# -----------------------------
st.title("📊 Labor Management Dashboard")
st.markdown("Use this tool to calculate productivity, staffing needs, and performance using industrial engineering standards.")

st.divider()

# -----------------------------
# INPUT SECTIONS
# -----------------------------
st.header("🧮 Input Data")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Supervisor Inputs")
    observed_time = st.number_input("Observed Time per Unit (seconds)", min_value=0.0, step=0.1)
    rating = st.number_input("Performance Rating (%)", min_value=0.0, max_value=200.0, step=1.0)
    allowance = st.number_input("Allowance (%)", min_value=0.0, max_value=50.0, step=1.0) / 100
    demand = st.number_input("Daily Demand (units)", min_value=0, step=1)

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
    hours_worked = st.number_input("Hours Worked", min_value=0.0, step=0.25)
with col4:
    units_completed = st.number_input("Units Completed", min_value=0, step=1)

notes = st.text_area("Notes (barriers, equipment issues, coaching, training needs)")

st.divider()

# -----------------------------
# CALCULATIONS
# -----------------------------
st.header("📈 Results")

if observed_time > 0 and rating > 0 and demand > 0:

    # Industrial Engineering Calculations
    normal_time = observed_time * (rating / 100)
    standard_time = normal_time / (1 - allowance)
    required_hours = (demand * standard_time) / 3600
    available_hours = workers * (available_minutes / 60)
    utilization = required_hours / available_hours if available_hours > 0 else 0
    daily_cost = available_hours * labor_cost

    # Employee Productivity
    uph = units_completed / hours_worked if hours_worked > 0 else 0
    target_uph = 3600 / standard_time if standard_time > 0 else 0
    productivity = (uph / target_uph) if target_uph > 0 else 0
    variance = uph - target_uph

    # -----------------------------
    # DISPLAY RESULTS
    # -----------------------------
    colA, colB, colC = st.columns(3)

    with colA:
        st.metric("Normal Time (sec)", f"{normal_time:.2f}")
        st.metric("Standard Time (sec)", f"{standard_time:.2f}")
        st.metric("Required Labor Hours", f"{required_hours:.2f}")

    with colB:
        st.metric("Available Labor Hours", f"{available_hours:.2f}")
        st.metric("Utilization (%)", f"{utilization*100:.1f}%")
        st.metric("Daily Labor Cost", f"${daily_cost:,.2f}")

    with colC:
        st.metric("Units per Hour", f"{uph:.2f}")
        st.metric("Target UPH", f"{target_uph:.2f}")
        st.metric("Productivity (%)", f"{productivity*100:.1f}%")

    st.divider()

    # Variance Panel
    with st.expander("📉 Variance Details"):
        st.write(f"**Variance from Target UPH:** {variance:.2f}")
        if variance < 0:
            st.error("Below target — review barriers or training needs.")
        else:
            st.success("Above target — great performance.")

else:
    st.info("Enter supervisor inputs to calculate results.")

st.divider()

# -----------------------------
# NOTES SECTION
# -----------------------------
st.header("📝 Notes & Observations")
st.write(notes if notes else "No notes entered.")
