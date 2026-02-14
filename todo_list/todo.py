import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(page_title="Task Manager", layout="centered")
st.title(":orange[📝 To-Do List|] :blue[CodSoft Internship]")

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
FILE_PATH = "todo.json"

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
with st.form("new_task", clear_on_submit=True):
    col1, col2, col3 = st.columns([3, 1.2, 0.8])
    
    with col1:
        title = st.text_input("Task Title", placeholder="Enter your task...", label_visibility="collapsed")
    
    with col2:
        date = st.date_input("Due Date", label_visibility="collapsed")
    
    with col3:
        submit = st.form_submit_button("➕ Add Task", use_container_width=True)
    
    if submit and title:
        new_id = max([t['id'] for t in tasks], default=0) + 1
        tasks.append({
            "id": new_id,
            "title": title,
            "isCompleted": False,
            "dueDate": str(date)
        })
        save_data(tasks)
        st.success("✅ Task added!")
        st.rerun()
    elif submit and not title:
        st.warning("⚠️ Please enter a task title!")

# 3. DISPLAY TASKS
st.subheader("Your Tasks")

if len(tasks) == 0:
    st.markdown("""
    <div style="text-align: center; padding: 40px; color: #666;">
        🎉 No tasks yet. Add your first task above!
    </div>
    """, unsafe_allow_html=True)
else:
    for i, task in enumerate(tasks):
        # Use a container with a border for a "card" look
        with st.container(border=True):
            col1, col2, col3, col4 = st.columns([0.08, 0.45, 0.30, 0.15])
            
            # Checkbox for completion
            is_done = col1.checkbox("Done", value=task["isCompleted"], key=f"check_{task['id']}", label_visibility="collapsed")
            
            # Title styling
            if is_done:
                col2.markdown(f"~~{task['title']}~~")
            else:
                col2.markdown(f"**{task['title']}**")
            
            # Due Date and Completed badge
            if is_done:
                col3.markdown(f"<span style='background-color: #28a745; color: white; padding: 4px 12px; border-radius: 12px; font-size: 12px;'>✅ Completed</span>", unsafe_allow_html=True)
            else:
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
pending_count = len(tasks) - completed_count

# Display metrics in 3 columns
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("📋 Total Tasks", len(tasks))

with col2:
    st.metric("✅ Completed", completed_count)

with col3:
    st.metric("⏳ Pending", pending_count)

