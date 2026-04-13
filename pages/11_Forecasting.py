import streamlit as st
import pandas as pd
import sqlite3
import json
import numpy as np
import altair as alt
from datetime import timedelta

st.set_page_config(page_title="Forecasting & Projections", layout="wide")

DB_FILE = "daily_cost_records.db"

# -----------------------------
# LOAD DATA
# -----------------------------
conn = sqlite3.connect(DB_FILE)
df = pd.read_sql_query("SELECT * FROM records", conn)

if df.empty:
    st.info("No data available yet. Enter data on the Operator Entry page.")
    st.stop()

df["Date"] = pd.to_datetime(df["Date"])

# -----------------------------
# UNPACK JSON FIELDS
# -----------------------------
expanded_rows = []
for _, row in df.iterrows():
    base = {
        "Date": row["Date"],
        "Units Produced": row["UnitsProduced"],
        "Orders Processed": row["OrdersProcessed"],
        "Labor Hours": row["LaborHours"],
    }
    try:
        extra = json.loads(row["Data"])
        base.update(extra)
    except:
        pass
    expanded_rows.append(base)

df = pd.DataFrame(expanded_rows)

# -----------------------------
# SITE-AWARE FILTERING
# -----------------------------
st.sidebar.title("Filters")

if "Site" in df.columns:
    site_list = df["Site"].dropna().unique()
    if len(site_list) > 0:
        selected_site = st.sidebar.selectbox("Select Site", site_list)
        df = df[df["Site"] == selected_site]
    else:
        st.sidebar.info("No site values found yet. Enter new records with a Site selected.")
else:
    st.sidebar.info("Site column not found. Multi-site support not fully configured.")

if df.empty:
    st.info("No data available for the selected filters.")
    st.stop()

# -----------------------------
# PAGE TITLE
# -----------------------------
st.title("📈 Forecasting & Projections")

st.markdown(
    "This page shows 7‑day and 30‑day moving averages plus a simple linear regression "
    "forecast for key metrics."
)

# -----------------------------
# METRIC SELECTION
# -----------------------------
metric_options = ["Units Produced", "Orders Processed", "Labor Hours"]
metric = st.selectbox("Select Metric to Forecast", metric_options)

metric_df = df[["Date", metric]].dropna().sort_values("Date")

if metric_df.empty:
    st.info(f"No data available for metric: {metric}")
    st.stop()

# -----------------------------
# MOVING AVERAGES
# -----------------------------
metric_df = metric_df.set_index("Date").asfreq("D")
metric_df[metric] = metric_df[metric].interpolate()

metric_df["7D_MA"] = metric_df[metric].rolling(window=7, min_periods=1).mean()
metric_df["30D_MA"] = metric_df[metric].rolling(window=30, min_periods=1).mean()

# -----------------------------
# LINEAR REGRESSION FORECAST
# -----------------------------
history_days = st.sidebar.slider("History window (days) for regression", 30, 180, 90)
forecast_horizon = st.sidebar.slider("Forecast horizon (days)", 7, 30, 14)

hist_df = metric_df.last(f"{history_days}D").dropna(subset=[metric])

if len(hist_df) < 5:
    st.warning("Not enough historical data for a reliable regression. Showing moving averages only.")
    do_regression = False
else:
    do_regression = True

if do_regression:
    X = (hist_df.index - hist_df.index.min()).days.values.reshape(-1, 1)
    y = hist_df[metric].values

    # Simple linear regression using numpy polyfit
    coeffs = np.polyfit(X.flatten(), y, 1)
    slope, intercept = coeffs[0], coeffs[1]

    last_date = metric_df.index.max()
    future_dates = [last_date + timedelta(days=i) for i in range(1, forecast_horizon + 1)]
    X_future = (pd.to_datetime(future_dates) - hist_df.index.min()).days.values
    y_future = slope * X_future + intercept

    forecast_df = pd.DataFrame(
        {
            "Date": future_dates,
            "Forecast": y_future,
        }
    ).set_index("Date")
else:
    forecast_df = pd.DataFrame(columns=["Forecast"])

# -----------------------------
# COMBINED HISTORICAL + FORECAST
# -----------------------------
combined = metric_df.copy()
if do_regression and not forecast_df.empty:
    combined = pd.concat([combined, forecast_df], axis=0)

# -----------------------------
# TREND CHART
# -----------------------------
st.subheader(f"Trend & Forecast for {metric}")

base = alt.Chart(combined.reset_index()).encode(x="Date:T")

actual_line = base.mark_line(color="#1f77b4").encode(
    y=alt.Y(f"{metric}:Q", title=metric),
    tooltip=["Date:T", alt.Tooltip(f"{metric}:Q", format=".2f")]
)

ma7_line = base.mark_line(color="#ff7f0e", strokeDash=[4, 4]).encode(
    y="7D_MA:Q",
    tooltip=["Date:T", alt.Tooltip("7D_MA:Q", title="7D MA", format=".2f")]
)

ma30_line = base.mark_line(color="#2ca02c", strokeDash=[2, 2]).encode(
    y="30D_MA:Q",
    tooltip=["Date:T", alt.Tooltip("30D_MA:Q", title="30D MA", format=".2f")]
)

if do_regression and not forecast_df.empty:
    forecast_line = base.mark_line(color="#d62728").encode(
        y="Forecast:Q",
        tooltip=["Date:T", alt.Tooltip("Forecast:Q", format=".2f")]
    )
    chart = (actual_line + ma7_line + ma30_line + forecast_line).properties(height=400)
else:
    chart = (actual_line + ma7_line + ma30_line).properties(height=400)

st.altair_chart(chart, use_container_width=True)

# -----------------------------
# FORECAST TABLES
# -----------------------------
st.subheader("Forecast Table")

if do_regression and not forecast_df.empty:
    forecast_table = forecast_df.copy()
    forecast_table.index = forecast_table.index.date
    st.dataframe(
        forecast_table.reset_index().rename(columns={"index": "Date"}),
        use_container_width=True,
    )
else:
    st.info("Forecast table not available due to insufficient historical data.")

st.subheader("Recent History with Moving Averages")

history_table = metric_df[[metric, "7D_MA", "30D_MA"]].last("30D").copy()
history_table.index = history_table.index.date

st.dataframe(
    history_table.reset_index().rename(columns={"index": "Date"}),
    use_container_width=True,
)
