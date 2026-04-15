import streamlit as st

st.set_page_config(page_title="Home", layout="wide")

# -----------------------------------------
# OPTIONAL: Sidebar header (safe)
# -----------------------------------------
st.sidebar.title("Labor Management System")

st.sidebar.info("Use the sidebar page list to navigate.")

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

st.success("Select a page from the sidebar to get started.")
