import streamlit as st

st.set_page_config(page_title="Labor Management IE App", layout="wide")

st.title("Labor Management App (Industrial Engineering)")

st.markdown(
    """
This app uses basic industrial engineering labor standards to estimate:
- Standard time per unit  
- Required labor hours and workers  
- Utilization and labor cost  
"""
)

st.sidebar.header("Input parameters")

# --- Work content inputs ---
st.sidebar.subheader("Work content (per unit)")
observed_time_sec = st.sidebar.number_input(
    "Observed time per unit (seconds)",
    min_value=0.0,
    value=60.0,
    step=1.0,
)
performance_rating = st.sidebar.number_input(
    "Performance rating (%)",
    min_value=50.0,
    max_value=150.0,
    value=100.0,
    step=1.0,
)
allowance_percent = st.sidebar.number_input(
    "Allowance (%)",
    min_value=0.0,
    max_value=50.0,
    value=15.0,
    step=1.0,
)

# --- Demand and schedule inputs ---
st.sidebar.subheader("Demand and schedule")
daily_demand_units = st.sidebar.number_input(
    "Daily demand (units/day)",
    min_value=0.0,
    value=500.0,
    step=10.0,
)
available_minutes_per_worker = st.sidebar.number_input(
    "Available work time per worker (minutes/shift)",
    min_value=1.0,
    value=480.0,
    step=10.0,
)
num_workers = st.sidebar.number_input(
    "Number of workers",
    min_value=1,
    value=10,
    step=1,
)

# --- Cost and utilization inputs ---
st.sidebar.subheader("Cost and utilization")
labor_cost_per_hour = st.sidebar.number_input(
    "Labor cost per worker per hour ($/hr)",
    min_value=0.0,
    value=20.0,
    step=1.0,
)
target_utilization_percent = st.sidebar.number_input(
    "Target utilization (%)",
    min_value=50.0,
    max_value=100.0,
    value=85.0,
    step=1.0,
)

# --- Calculations ---
# Normal time (sec)
normal_time_sec = observed_time_sec * (performance_rating / 100.0)

# Standard time (sec)
allowance_decimal = allowance_percent / 100.0
if allowance_decimal >= 1.0:
    st.error("Allowance must be less than 100%.")
    st.stop()

standard_time_sec = normal_time_sec / (1.0 - allowance_decimal)

# Required labor hours per day
required_labor_hours = (daily_demand_units * standard_time_sec) / 3600.0

# Available labor hours per day
available_hours_per_worker = available_minutes_per_worker / 60.0
available_labor_hours = num_workers * available_hours_per_worker

# Utilization
utilization = required_labor_hours / available_labor_hours if available_labor_hours > 0 else 0.0

# Required workers (based on demand)
required_workers = required_labor_hours / available_hours_per_worker if available_hours_per_worker > 0 else 0.0

# Units per worker per hour
units_per_worker_per_hour = (
    daily_demand_units / available_labor_hours if available_labor_hours > 0 else 0.0
)

# Daily labor cost
daily_labor_cost = available_labor_hours * labor_cost_per_hour

# Target utilization comparison
target_utilization = target_utilization_percent / 100.0
utilization_gap = utilization - target_utilization

# --- Layout for outputs ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Time standards")
    st.metric(
        "Observed time per unit",
        f"{observed_time_sec:,.2f} sec"
    )
    st.metric(
        "Normal time per unit",
        f"{normal_time_sec:,.2f} sec"
    )
    st.metric(
        "Standard time per unit",
        f"{standard_time_sec:,.2f} sec"
    )

    st.subheader("Labor requirements")
    st.metric(
        "Required labor hours per day",
        f"{required_labor_hours:,.2f} hrs"
    )
    st.metric(
        "Required workers (based on demand)",
        f"{required_workers:,.2f} workers"
    )

with col2:
    st.subheader("Utilization and productivity")
    st.metric(
        "Available labor hours per day",
        f"{available_labor_hours:,.2f} hrs"
    )
    st.metric(
        "Actual utilization",
        f"{utilization*100:,.1f} %"
    )
    st.metric(
        "Target utilization",
        f"{target_utilization_percent:,.1f} %"
    )
    st.metric(
        "Utilization gap (actual - target)",
        f"{utilization_gap*100:,.1f} %"
    )

    st.subheader("Cost and output")
    st.metric(
        "Daily labor cost",
        f"${daily_labor_cost:,.2f}"
    )
    st.metric(
        "Units per worker per hour",
        f"{units_per_worker_per_hour:,.2f} units/hr"
    )

st.markdown("---")
st.markdown(
    """
**Notes**

- **Normal time** = Observed time × Performance rating  
- **Standard time** = Normal time ÷ (1 − Allowance)  
- **Required workers** is based on demand and standard time, assuming one shift.  
- Adjust demand, allowances, and workers to test different labor plans.
"""
)
