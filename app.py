import streamlit as st
from datetime import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Life Optimizer", page_icon="🚀", layout="centered")

# --- SESSION STATE INITIALIZATION ---
# Using standard Python types instead of Pandas DataFrames
if 'xp' not in st.session_state:
    st.session_state.xp = 0
if 'level' not in st.session_state:
    st.session_state.level = 1
if 'freezes' not in st.session_state:
    st.session_state.freezes = 2
if 'habits' not in st.session_state:
    # Dictionary to store habit name and its completion status
    st.session_state.habits = {
        "Gym": False,
        "Coding": False,
        "Reading": False
    }

# --- LOGIC ---
def update_xp(habit_name):
    # Logic to add or subtract XP based on checkbox state
    if st.session_state[habit_name]:
        st.session_state.xp += 10
    else:
        st.session_state.xp -= 10
    
    # Level calculation: Level = 1 + (Total XP / 100)
    st.session_state.level = 1 + (st.session_state.xp // 100)

# --- UI ---
st.title("🚀 Life Optimizer")

# Level and Freeze Stats
col1, col2 = st.columns(2)
with col1:
    st.metric("Level", f"{st.session_state.level} Warrior")
with col2:
    st.metric("Streak Freezes", st.session_state.freezes)

# XP Progress Bar (Standard Python Math)
progress_val = (st.session_state.xp % 100) / 100
st.progress(progress_val)
st.caption(f"{st.session_state.xp % 100} / 100 XP to Next Level")

st.divider()

# Daily Tasks Section
st.header("Daily Tasks")
for habit in list(st.session_state.habits.keys()):
    st.checkbox(
        habit, 
        value=st.session_state.habits[habit], 
        key=habit, 
        on_change=update_xp, 
        args=(habit,)
    )

# Weekly Momentum Heatmap (Visualized using Columns)
st.header("Weekly Momentum")
days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
m_cols = st.columns(7)
for i, col in enumerate(m_cols):
    with col:
        st.write(days[i])
        # Simple logic to show a 'filled' box for demo purposes
        st.info("🟦") 

st.divider()

# Streak Freeze Button
if st.button("❄️ Use Streak Freeze"):
    if st.session_state.freezes > 0:
        st.session_state.freezes -= 1
        st.snow()
        st.success("Freeze Used! Momentum Saved.")
    else:
        st.error("No Freezes left!")
        
