import streamlit as st

st.set_page_config(page_title="Operations Toolkit", layout="wide")

st.title("Operations Toolkit")
st.subheader("Labor Management App — Instructions")

st.markdown("""
### Purpose
The Labor Management App helps supervisors and employees measure productivity using industrial engineering math. It calculates standard time, required labor hours, utilization, and performance based on the work completed during a shift.

---

### What Employees Do
Employees enter:
- Hours worked  
- Units completed  
- Optional notes  

The app calculates:
- Actual units per hour  
- Productivity percentage  
- Variance from target  
- Performance rating  

---

### What Supervisors Do
Supervisors enter:
- Observed time per unit (seconds)  
- Performance rating (%)  
- Allowance (%)  
- Target units per hour or target productivity  
- Daily demand (optional)  

The app calculates:
- Normal time  
- Standard time  
- Required labor hours  
- Required workers  
- Utilization  
- Daily labor cost  

---

### Step-by-Step Instructions

#### 1. Enter Work Content (Supervisor)
- Observed time per unit  
- Performance rating  
- Allowance percentage  

The app automatically calculates normal and standard time.

#### 2. Enter Demand and Schedule (Supervisor)
- Daily demand  
- Available minutes per worker  
- Number of workers  

This determines required labor hours and utilization.

#### 3. Enter Employee Output (Employee or Supervisor)
- Hours worked  
- Units completed  

The app calculates:
- Actual UPH  
- Productivity %  
- Variance  
- Performance rating  

#### 4. Review the Results
You will see:
- Standard time per unit  
- Required labor hours  
- Required workers  
- Actual vs. target utilization  
- Daily labor cost  
- Units per worker per hour  

#### 5. Add Notes (Optional)
Use notes to record:
- Barriers  
- Equipment issues  
- Training needs  
- Coaching conversations  

---

### How the Math Works
- Normal Time = Observed Time × Performance Rating  
- Standard Time = Normal Time ÷ (1 − Allowance)  
- Required Labor Hours = (Demand × Standard Time) ÷ 3600  
- Utilization = Required Hours ÷ Available Hours  
- Units per Worker per Hour = Total Units ÷ Total Hours  
""")
