import streamlit as st
from database_init import init_db

st.set_page_config(page_title="Category Management", layout="wide")

# Initialize DB
conn, cursor = init_db()

st.title("🗂️ Budget Category Management")

# ---------------------------------------------------
# LOAD EXISTING CATEGORIES
# ---------------------------------------------------
cursor.execute("SELECT CategoryName FROM cost_categories ORDER BY CategoryName")
categories = [row[0] for row in cursor.fetchall()]

# ---------------------------------------------------
# ADD NEW CATEGORY
# ---------------------------------------------------
st.subheader("Add New Budget Category")

new_category = st.text_input("Category Name")

if st.button("Add Category"):
    if new_category.strip() == "":
        st.error("Category name cannot be empty")
    else:
        try:
            cursor.execute(
                "INSERT INTO cost_categories (CategoryName) VALUES (?)",
                (new_category.strip(),)
            )
            conn.commit()
            st.success(f"Category '{new_category}' added successfully")
            st.experimental_rerun()
        except Exception as e:
            st.error(f"Error: {e}")

# ---------------------------------------------------
# LIST + DELETE CATEGORIES
# ---------------------------------------------------
st.subheader("Existing Categories")

if not categories:
    st.info("No categories found")
else:
    for cat in categories:
        col1, col2 = st.columns([4, 1])
        col1.write(cat)
        if col2.button("Delete", key=f"del_{cat}"):
            cursor.execute("DELETE FROM cost_categories WHERE CategoryName = ?", (cat,))
            conn.commit()
            st.warning(f"Deleted category: {cat}")
            st.experimental_rerun()

