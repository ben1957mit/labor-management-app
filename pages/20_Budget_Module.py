import streamlit as st
import pandas as pd
import io
import altair as alt

from modules.budget_calculator import (
    LaborRole, LaborData, BudgetItem, BudgetCategory, DistributionCenterBudget
)

# ---------------------------------------------------------
# PAGE TITLE
# ---------------------------------------------------------
st.title("📦 Distribution Center Budget & Labor Cost Module")

# ---------------------------------------------------------
# MULTI-LOCATION SUPPORT
# ---------------------------------------------------------
st.sidebar.header("Location Selector")
locations = ["Dallas DC", "Houston DC", "Atlanta DC"]
selected_location = st.sidebar.selectbox("Select Distribution Center", locations)

st.write(f"### Location: {selected_location}")

# ---------------------------------------------------------
# LABOR DATA INPUT (Editable Table)
# ---------------------------------------------------------
st.subheader("👷 Labor Data")

default_labor = pd.DataFrame({
    "role": ["Picker", "Forklift Operator"],
    "hourly_rate": [18, 20],
    "overtime_rate": [27, 30],
    "hours": [160, 150],
    "overtime_hours": [10, 5]
})

labor_df = st.data_editor(default_labor, num_rows="dynamic")

# Convert labor table → LaborData objects
labor_entries = []
for _, row in labor_df.iterrows():

    # Skip invalid rows
    if pd.isna(row["role"]) or pd.isna(row["hourly_rate"]) or pd.isna(row["hours"]):
        continue

    try:
        hourly_rate = float(row["hourly_rate"])
        overtime_rate = float(row["overtime_rate"])
        hours = float(row["hours"])
        overtime_hours = float(row["overtime_hours"])
    except:
        continue

    role = LaborRole(
        name=str(row["role"]).strip(),
        hourly_rate=hourly_rate,
        overtime_rate=overtime_rate
    )

    labor_entries.append(
        LaborData(
            role=role,
            hours=hours,
            overtime_hours=overtime_hours
        )
    )

# ---------------------------------------------------------
# BUDGET TABLE (Editable)
# ---------------------------------------------------------
st.subheader("🏗 Budget Categories")

default_budget = pd.DataFrame({
    "category": ["Facility", "Utilities", "Supplies"],
    "item": ["Lease", "Electricity", "Stretch Wrap"],
    "amount": [45000, 12000, 3000]
})

budget_df = st.data_editor(default_budget, num_rows="dynamic")

# Convert budget table → BudgetCategory objects (with validation)
categories = {}

for _, row in budget_df.iterrows():

    # Skip empty or invalid rows
    if pd.isna(row["category"]) or pd.isna(row["item"]) or pd.isna(row["amount"]):
        continue

    try:
        amount = float(row["amount"])
    except:
        continue

    cat = str(row["category"]).strip()
    item_name = str(row["item"]).strip()

    if cat == "" or item_name == "":
        continue

    if cat not in categories:
        categories[cat] = BudgetCategory(name=cat, items=[])

    categories[cat].items.append(
        BudgetItem(
            name=item_name,
            amount=amount
        )
    )

# ---------------------------------------------------------
# BUILD BUDGET ENGINE
# ---------------------------------------------------------
dc_budget = DistributionCenterBudget(
    labor_data=labor_entries,
    categories=categories
)

# ---------------------------------------------------------
# SUMMARY METRICS
# ---------------------------------------------------------
st.subheader("📊 Budget Summary")

col1, col2, col3 = st.columns(3)
col1.metric("Labor Cost", f"${dc_budget.total_labor_cost():,.2f}")
col2.metric("Non-Labor Cost", f"${dc_budget.total_non_labor_cost():,.2f}")
col3.metric("Total Cost", f"${dc_budget.total_cost():,.2f}")

units = st.number_input("Units processed this month", min_value=0, value=50000)
st.metric("Cost Per Unit", f"${dc_budget.cost_per_unit(units):,.4f}")

# ---------------------------------------------------------
# CHARTS (Labor Trend + Category Breakdown)
# ---------------------------------------------------------
st.subheader("📈 Cost Visualization")

# Labor cost trend (sample trend)
trend_df = pd.DataFrame({
    "Month": ["Jan", "Feb", "Mar", "Apr"],
    "Labor Cost": [
        dc_budget.total_labor_cost() * 0.9,
        dc_budget.total_labor_cost(),
        dc_budget.total_labor_cost() * 1.1,
        dc_budget.total_labor_cost()
    ]
})

line_chart = alt.Chart(trend_df).mark_line(point=True).encode(
    x="Month",
    y="Labor Cost"
)

st.altair_chart(line_chart, use_container_width=True)

# Category breakdown
cat_df = pd.DataFrame({
    "Category": list(categories.keys()),
    "Cost": [cat.total() for cat in categories.values()]
})

bar_chart = alt.Chart(cat_df).mark_bar().encode(
    x="Category",
    y="Cost",
    color="Category"
)

st.altair_chart(bar_chart, use_container_width=True)

# ---------------------------------------------------------
# EXPORT TO EXCEL
# ---------------------------------------------------------
st.subheader("📤 Export Budget to Excel")

excel_buffer = io.BytesIO()
with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
    labor_df.to_excel(writer, sheet_name="Labor Data", index=False)
    budget_df.to_excel(writer, sheet_name="Budget Items", index=False)
    cat_df.to_excel(writer, sheet_name="Category Summary", index=False)

st.download_button(
    label="Download Excel File",
    data=excel_buffer.getvalue(),
    file_name=f"{selected_location}_budget.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

