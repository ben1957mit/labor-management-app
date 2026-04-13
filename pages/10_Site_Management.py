import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Site Management", layout="wide")

DB_FILE = "daily_cost_records.db"

# -----------------------------
# DATABASE SETUP
# -----------------------------
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# Dedicated sites table
cursor.execute("""
CREATE TABLE IF NOT EXISTS sites (
    SiteName TEXT PRIMARY KEY
)
""")
conn.commit()

st.title("🏭 Multi‑Site Management")

# -----------------------------
# EXISTING SITES
# -----------------------------
st.subheader("Existing Sites")

sites_df = pd.read_sql_query("SELECT SiteName AS Site FROM sites ORDER BY SiteName", conn)

if sites_df.empty:
    st.info("No sites defined yet. Add a site below.")
else:
    st.dataframe(sites_df, use_container_width=True)

# -----------------------------
# ADD NEW SITE
# -----------------------------
st.subheader("Add New Site")

new_site = st.text_input("Site Name")

col_add, col_delete = st.columns(2)

with col_add:
    if st.button("Add Site"):
        if new_site.strip() == "":
            st.warning("Site name cannot be empty.")
        else:
            try:
                cursor.execute("INSERT INTO sites (SiteName) VALUES (?)", (new_site.strip(),))
                conn.commit()
                st.success(f"Site '{new_site.strip()}' added!")
                st.experimental_rerun()
            except sqlite3.IntegrityError:
                st.warning("This site already exists.")

# -----------------------------
# DELETE SITE (OPTIONAL)
# -----------------------------
with col_delete:
    if not sites_df.empty:
        site_to_delete = st.selectbox("Delete Site", sites_df["Site"])
        if st.button("Confirm Delete"):
            cursor.execute("DELETE FROM sites WHERE SiteName = ?", (site_to_delete,))
            conn.commit()
            st.success(f"Site '{site_to_delete}' deleted.")
            st.experimental_rerun()
