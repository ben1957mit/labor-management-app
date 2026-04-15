import streamlit as st

st.set_page_config(page_title="Home", layout="wide")

# Sidebar header only (SAFE)
st.sidebar.title("Labor Management System")

# Main content
st.title("📊 Labor & Cost Management System")

st.write("""
Welcome to your centralized labor, production, and cost management platform.

Use the sidebar to navigate through the application.
""")

st.success("Select a page from the sidebar to get started.")

