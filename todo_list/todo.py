import streamlit as st
import pandas as pd
import json
import os
from datetime import date, datetime

st.set_page_config(page_title="Task Manager", layout="centered")
st.title(":orange[📝 To-Do List|] :blue[CodSoft Internship]")

st.header(":blue-background[To-Do List Application]")
st.write("Manage your daily tasks efficiently using Python & Streamlit")

# ============================================
# DARK/LIGHT MODE TOGGLE
# ============================================
if "theme" not in st.session_state:
    st.session_state.theme = "light"

col_themeToggle, col_spacer = st.columns([1, 5])
with col_themeToggle:
    if st.button("🌙" if st.session_state.theme == "light" else "☀️"):
        st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"
        st.rerun()

# Apply theme
if st.session_state.theme == "dark":
    st.markdown("""
    <style>
    .stApp {background-color: #1e1e1e; color: white;}
    .stTextInput input, .stDateInput input {color: white;}
    </style>
    """, unsafe_allow_html=True)

# ============================================
# DATA LOADING & SAVING
# ============================================
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

# ============================================
# ADD NEW TASK
# ============================================
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

# ============================================
# SEARCH & FILTER
# ============================================
col_search, col_sort = st.columns([2, 1])

with col_search:
    search_query = st.text_input("🔍 Search tasks...", placeholder="Search by title...")

with col_sort:
    sort_option = st.selectbox("Sort by", ["Pending First", "Completed First", "Due Date"])

# Filter tasks based on search
if search_query:
    filtered_tasks = [t for t in tasks if search_query.lower() in t['title'].lower()]
else:
    filtered_tasks = tasks

# Sort tasks
if sort_option == "Pending First":
    filtered_tasks = sorted(filtered_tasks, key=lambda x: x['isCompleted'])
elif sort_option == "Completed First":
    filtered_tasks = sorted(filtered_tasks, key=lambda x: not x['isCompleted'])
elif sort_option == "Due Date":
    filtered_tasks = sorted(filtered_tasks, key=lambda x: x['dueDate'])

# ============================================
# DISPLAY TASKS
# ============================================
st.subheader("Your Tasks")

if len(filtered_tasks) == 0:
    if search_query:
        st.markdown("""
        <div style="text-align: center; padding: 40px; color: #666;">
            🔍 No tasks found matching your search.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align: center; padding: 40px; color: #666;">
            🎉 No tasks yet. Add your first task above!
        </div>
        """, unsafe_allow_html=True)
else:
    for i, task in enumerate(filtered_tasks):
        # Find original index in tasks list
        original_index = next(j for j, t in enumerate(tasks) if t['id'] == task['id'])
        
        # Use a container with a border for a "card" look
        with st.container(border=True):
            col1, col2, col3, col4, col5 = st.columns([0.08, 0.40, 0.25, 0.12, 0.15])
            
            # Checkbox for completion
            is_done = col1.checkbox("Done", value=task["isCompleted"], key=f"check_{task['id']}", label_visibility="collapsed")
            
            # Title styling
            if is_done:
                col2.markdown(f"~~{task['title']}~~")
            else:
                col2.markdown(f"**{task['title']}**")
            
            # Due Date, Overdue, or Completed badge
            if is_done:
                col3.markdown(f"<span style='background-color: #28a745; color: white; padding: 4px 12px; border-radius: 12px; font-size: 12px;'>✅ Completed</span>", unsafe_allow_html=True)
            else:
                # Check for overdue
                task_date = datetime.strptime(task['dueDate'], '%Y-%m-%d').date()
                today = date.today()
                
                if task_date < today:
                    col3.markdown(f"<span style='background-color: #dc3545; color: white; padding: 4px 12px; border-radius: 12px; font-size: 12px;'>⚠️ Overdue</span>", unsafe_allow_html=True)
                else:
                    col3.caption(f"📅 {task['dueDate']}")
            
            # Edit button
            if col4.button("✏️", key=f"edit_{task['id']}"):
                st.session_state.edit_task_id = task['id']
                st.session_state.edit_task_title = task['title']
                st.session_state.edit_task_date = task['dueDate']
                st.rerun()
            
            # Delete button
            if col5.button("🗑️", key=f"delete_{task['id']}"):
                tasks.pop(original_index)
                save_data(tasks)
                st.rerun()

            # Update state if checkbox changed
            if is_done != task["isCompleted"]:
                tasks[original_index]["isCompleted"] = is_done
                save_data(tasks)
                st.rerun()

# ============================================
# EDIT TASK MODAL (if edit button clicked)
# ============================================
if "edit_task_id" in st.session_state:
    st.markdown("---")
    st.subheader("✏️ Edit Task")
    
    with st.form("edit_task"):
        edit_title = st.text_input("Task Title", value=st.session_state.edit_task_title)
        edit_date = st.date_input("Due Date", value=datetime.strptime(st.session_state.edit_task_date, '%Y-%m-%d').date())
        
        col_save, col_cancel = st.columns(2)
        
        with col_save:
            save_edit = st.form_submit_button("💾 Save Changes")
        
        with col_cancel:
            cancel_edit = st.form_submit_button("❌ Cancel")
        
        if save_edit and edit_title:
            # Find and update task
            for task in tasks:
                if task['id'] == st.session_state.edit_task_id:
                    task['title'] = edit_title
                    task['dueDate'] = str(edit_date)
                    break
            save_data(tasks)
            del st.session_state.edit_task_id
            st.success("✅ Task updated!")
            st.rerun()
        
        if cancel_edit:
            del st.session_state.edit_task_id
            st.rerun()

# ============================================
# QUICK STATS
# ============================================
st.markdown("---")
completed_count = sum(1 for t in tasks if t['isCompleted'])
pending_count = len(tasks) - completed_count

# Display metrics in 3 columns
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("📋 Total Tasks", len(tasks))

with col2:
    st.metric("✅ Completed", completed_count)

with col3:
    st.metric("⏳ Pending", pending_count)

