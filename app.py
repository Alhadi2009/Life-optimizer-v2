import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Life Optimizer", page_icon="🚀", layout="centered")

# --- SESSION STATE INITIALIZATION (Data Persistence for the Session) ---
if 'xp' not in st.session_state:
    st.session_state.xp = 0
if 'level' not in st.session_state:
    st.session_state.level = 1
if 'streak_freezes' not in st.session_state:
    st.session_state.streak_freezes = 2  # Start with 2 freezes
if 'habits' not in st.session_state:
    st.session_state.habits = {
        "Gym / Workout": False,
        "Read 10 Pages": False,
        "Code for 30 Mins": False,
        "Drink 2L Water": False
    }

# --- FUNCTIONS ---
def calculate_level(xp):
    # Simple logic: Level up every 100 XP
    return 1 + (xp // 100)

def get_progress(xp):
    # Returns 0.0 to 1.0 for the progress bar
    return (xp % 100) / 100

def toggle_habit(habit_name):
    # Toggle the state
    st.session_state.habits[habit_name] = not st.session_state.habits[habit_name]
    
    # Add/Remove XP
    if st.session_state.habits[habit_name]:
        st.session_state.xp += 10
        st.toast(f"✅ {habit_name} complete! +10 XP")
    else:
        st.session_state.xp -= 10
        
    # Update Level
    new_level = calculate_level(st.session_state.xp)
    if new_level > st.session_state.level:
        st.balloons()
        st.success(f"🎉 LEVEL UP! You are now Level {new_level}!")
    st.session_state.level = new_level

# --- UI LAYOUT ---

# 1. Header & Level System
st.title("🚀 Life Optimizer")

col1, col2 = st.columns([3, 1])
with col1:
    st.subheader(f"Level {st.session_state.level} Warrior")
with col2:
    st.metric(label="Streak Freezes", value=st.session_state.streak_freezes, delta="❄️")

# XP Progress Bar
progress = get_progress(st.session_state.xp)
st.progress(progress)
st.caption(f"✨ {st.session_state.xp % 100} / 100 XP to Level {st.session_state.level + 1}")

st.markdown("---")

# 2. Daily Tasks
st.header("Daily Tasks")

# Display habits as checkboxes
for habit, is_done in st.session_state.habits.items():
    # We use a callback to handle the logic immediately when clicked
    st.checkbox(
        habit, 
        value=is_done, 
        key=habit, 
        on_change=toggle_habit, 
        args=(habit,)
    )

# Add new habit input
with st.expander("➕ Add a new habit"):
    new_habit = st.text_input("Habit Name")
    if st.button("Add Habit"):
        if new_habit and new_habit not in st.session_state.habits:
            st.session_state.habits[new_habit] = False
            st.rerun()

st.markdown("---")

# 3. Weekly Momentum (The Heatmap)
st.header("Weekly Momentum")

# Generating dummy data for the visual (Last 7 days)
# In a real app with a database, you would fetch real history here.
days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
cols = st.columns(7)

# Let's fake a history pattern for the demo
# 1 = Done, 0 = Missed, 2 = Freeze Used
fake_history = [1, 1, 0, 1, 2, 1, 0] 

today_idx = datetime.today().weekday() # Current day index

for i, col in enumerate(cols):
    day_name = days[i]
    status = fake_history[i]
    
    with col:
        st.write(f"**{day_name}**")
        if status == 1:
            st.markdown("🟩") # Success
        elif status == 2:
            st.markdown("❄️") # Freeze Used
        else:
            st.markdown("⬜") # Missed

# 4. The "Twist": Streak Freeze Mechanic
with st.expander("❄️ Manage Streak Freezes"):
    st.write("Too busy today? Use a save to keep your momentum.")
    if st.button("Use Streak Freeze (-1 Save)"):
        if st.session_state.streak_freezes > 0:
            st.session_state.streak_freezes -= 1
            st.toast("❄️ Streak Freeze Activated! Day saved.")
            st.rerun()
        else:
            st.error("No freezes left! Earn more by leveling up.")

