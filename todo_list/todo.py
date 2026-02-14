import streamlit as st
import pandas as pd
import json
import os


st.title(":orange[To-Do List|] :blue[CodSoft Internship]")

st.header(":blue-background[To-Do List Application]")
st.write("Manage your daily tasks efficiently using Python & Streamlit")

# ============================================
# UNDERSTANDING SESSION STATE IN STREAMLIT
# ============================================
# Streamlit reruns the entire script when you interact with widgets.
# To keep data between reruns, we use st.session_state.
# Think of it like a temporary memory that remembers values across interactions.
# ============================================

# 1. Setup & Data Loading
st.set_page_config(page_title="Task Manager", layout="centered")
FILE_PATH = "todo.json"

# Initialize session state for form inputs
if "task_title" not in st.session_state:
    st.session_state.task_title = ""
if "task_date" not in st.session_state:
    st.session_state.task_date = None

def load_data():
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r") as f:
            return json.load(f)
    return []

def save_data(data):
    with open(FILE_PATH, "w") as f:
        json.dump(data, f, indent=4)

tasks = load_data()

# --- HEADER ---
st.markdown("---")

# 2. ADD NEW TASK
with st.form("new_task"):
    title = st.text_input("Task Title", value=st.session_state.task_title)
    date = st.date_input("Due Date", value=st.session_state.task_date)
    submit = st.form_submit_button("Save Task")
    
    if submit and title:
        new_id = max([t['id'] for t in tasks], default=0) + 1
        tasks.append({
            "id": new_id,
            "title": title,
            "isCompleted": False,
            "dueDate": str(date)
        })
        save_data(tasks)
        # Clear input fields
        st.session_state.task_title = ""
        st.session_state.task_date = None
        st.success("Task added successfully!")
        st.rerun()

# 3. DISPLAY TASKS
st.subheader("Your Tasks")

for i, task in enumerate(tasks):
    # Use a container with a border for a "card" look
    with st.container(border=True):
        col1, col2, col3, col4 = st.columns([0.1, 0.5, 0.3, 0.1])
        
        # Checkbox for completion
        is_done = col1.checkbox("Done", value=task["isCompleted"], key=f"check_{task['id']}", label_visibility="collapsed")
        
        # Title styling (strike-through if done)
        if is_done:
            col2.markdown(f"~~{task['title']}~~")
        else:
            col2.markdown(f"**{task['title']}**")
            
        # Due Date
        col3.caption(f"📅 {task['dueDate']}")
        
        # Delete button
        if col4.button("🗑️", key=f"delete_{task['id']}"):
            tasks.pop(i)
            save_data(tasks)
            st.rerun()

        # Update state if checkbox changed
        if is_done != task["isCompleted"]:
            tasks[i]["isCompleted"] = is_done
            save_data(tasks)
            st.rerun()

# 4. QUICK STATS
st.markdown("---")
completed_count = sum(1 for t in tasks if t["isCompleted"])
st.info(f"You have completed {completed_count} out of {len(tasks)} tasks.")

