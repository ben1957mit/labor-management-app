import streamlit as st

st.set_page_config(page_title="Labor Management Instructions", layout="wide")

st.title("Labor Management App — Instructions")

st.markdown("""
## 🧭 Purpose of the App
The Labor Management App helps supervisors and employees measure productivity using **industrial engineering (IE) standards**.  
It calculates:
- Normal time  
- Standard time  
- Required labor hours  
- Required workers  
- Utilization  
- Productivity %  
- Units per hour  
- Variance from target  
- Performance rating  

---

## 👷 Employee Instructions

### What employees enter
- **Hours worked**
- **Units completed**
- **Optional notes** (barriers, equipment issues, training needs)

### What the app calculates for employees
- Units per hour (UPH)  
- Productivity %  
- Variance from target  
- Performance rating  

### Employee workflow
1. Go to the **Labor Management** page  
2. Enter **hours worked**  
3. Enter **units completed**  
4. Add optional notes  
5. Review your results  

---

## 🧑‍💼 Supervisor Instructions

### What supervisors enter
- Observed time per unit (seconds)  
- Performance rating (%)  
- Allowance (%)  
- Daily demand (units)  
- Available minutes per worker  
- Number of workers  
- Labor cost per hour  
- Target utilization (%)  

### What the app calculates for supervisors
- Normal time  
- Standard time  
- Required labor hours  
- Required workers  
- Available labor hours  
- Actual vs. target utilization  
- Daily labor cost  
- Units per worker per hour  

### Supervisor workflow
1. Enter **observed time**, **rating**, and **allowance**  
2. Enter **demand**, **available minutes**, and **number of workers**  
3. Enter **labor cost** and **target utilization**  
4. Review:
   - Standard time  
   - Required labor hours  
   - Required workers  
   - Utilization  
   - Labor cost  
   - Productivity metrics  
5. Use the notes section to document:
   - Coaching conversations  
   - Barriers  
   - Equipment issues  
   - Training needs  

---

## 📊 Industrial Engineering Math Used

### Normal Time
Observed Time × (Rating ÷ 100)

### Standard Time
Normal Time ÷ (1 − Allowance)

### Required Labor Hours
(Demand × Standard Time) ÷ 3600

### Available Labor Hours
Workers × (Available Minutes ÷ 60)

### Utilization
Required Hours ÷ Available Hours

### Units per Worker per Hour
Total Units ÷ Available Hours

The app performs all calculations automatically.

---

## 🎯 How to Use the Results

### Supervisors use results to:
- Coach employees  
- Identify training needs  
- Adjust staffing  
- Improve workflow  
- Track performance trends  

### Employees use results to:
- Understand expectations  
- Track their own performance  
- Improve safely and consistently  
""")
