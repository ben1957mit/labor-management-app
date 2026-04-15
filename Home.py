import streamlit as st

# -----------------------------------------
# SIDEBAR NAVIGATION
# -----------------------------------------
st.sidebar.title("Navigation")

st.sidebar.markdown("""
### Data Entry
- Operator Entry
- Site Management
- Category Management

### Data Tools
- Database Viewer

### Dashboards
- Dynamic Dashboard
- Daily Summary
- Rollup Dashboard

### Forecasting
- Forecasting
""")

# -----------------------------------------
# MAIN HOME PAGE
# -----------------------------------------
st.title("📊 Labor & Cost Management System")

st.write("""
Welcome to your centralized labor, production, and cost management platform.

Use the sidebar to navigate through:
- Daily operator data entry  
- Site and category administration  
- Database inspection  
- Dynamic dashboards  
- Forecasting and analytics  
""")

st.info("Select a page from the sidebar to get started.")
