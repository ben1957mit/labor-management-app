import streamlit as st
import pandas as pd
from data_utils import read_rows

st.title("📅 Daily Summary")

rows = read_rows("performance_history.csv")

if not rows:
    st.info("No performance data available yet.")
else:
    df = pd.DataFrame(rows)
    df["hours_worked"] = df["hours_worked"].astype(float)
    df["units_completed"] = df["units_completed"].astype(float)
    df["uph"] = df["uph"].astype(float)
    df["productivity"] = df["productivity"].astype(float)
    df["daily_cost"] = df["daily_cost"].astype(float)

    dates = sorted(df["date"].unique())
    selected_date = st.selectbox("Select Date", dates, index=len(dates)-1)

    day_df = df[df["date"] == selected_date]

    total_units = day_df["units_completed"].sum()
    total_hours = day_df["hours_worked"].sum()
    avg_uph = day_df["uph"].mean()
    avg_prod = day_df["productivity"].mean() * 100
    total_cost = day_df["daily_cost"].max() if not day_df["daily_cost"].isna().all() else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Units", f"{total_units:.0f}")
    col2.metric("Total Hours", f"{total_hours:.2f}")
    col3.metric("Average UPH", f"{avg_uph:.2f}")

    col4, col5 = st.columns(2)
    col4.metric("Average Productivity (%)", f"{avg_prod:.1f}%")
    col5.metric("Daily Labor Cost (approx)", f"${total_cost:,.2f}")

    st.divider()
    st.subheader("Detail Table")
    st.dataframe(day_df, use_container_width=True)

    st.download_button(
        "Download Daily Summary (CSV)",
        data=day_df.to_csv(index=False).encode("utf-8"),
        file_name=f"daily_summary_{selected_date}.csv",
        mime="text/csv",
    )
