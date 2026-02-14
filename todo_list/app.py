import streamlit as st
from utils import (
    apply_theme, toggle_theme, get_empty_state_color,
    load_data, save_data, add_task, update_task_status, delete_task, edit_task,
    filter_tasks, sort_tasks, get_stats, render_task_card, render_empty_state
)
from datetime import datetime

st.set_page_config(page_title="Task Manager", layout="centered")
st.title(":orange[📝 To-Do List|] :blue[CodSoft Internship]")
st.header(":blue-background[To-Do List Application]")
st.write("Manage your daily tasks efficiently using Python & Streamlit")

# ============================================
# THEME TOGGLE
# ============================================
st.markdown(apply_theme(), unsafe_allow_html=True)

col_themeToggle, col_spacer = st.columns([1, 5])
with col_themeToggle:
    if st.button("🌙" if st.session_state.theme == "light" else "☀️"):
        toggle_theme()

st.markdown("---")

# ============================================
# LOAD DATA
# ============================================
if "tasks" not in st.session_state:
    st.session_state.tasks = load_data()

tasks = st.session_state.tasks

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
        tasks = add_task(tasks, title, date)
        save_data(tasks)
        st.success("✅ Task added!")
        st.rerun()
    elif submit and not title:
        st.warning("⚠️ Please enter a task title!")

# ============================================
# SEARCH, FILTER & SORT
# ============================================
col_search, col_filter, col_sort = st.columns([2, 1, 1])

with col_search:
    search_query = st.text_input("🔍 Search tasks...", placeholder="Search by title...")

with col_filter:
    filter_option = st.selectbox("Filter", ["All", "Pending", "Completed", "Overdue"])

with col_sort:
    sort_option = st.selectbox("Sort by", ["Pending First", "Completed First", "Due Date"])

# Apply filter and sort
filtered_tasks = filter_tasks(tasks, search_query, filter_option)
filtered_tasks = sort_tasks(filtered_tasks, sort_option)

# ============================================
# DISPLAY TASKS
# ============================================
st.subheader("Your Tasks")

if len(filtered_tasks) == 0:
    if search_query or filter_option != "All":
        render_empty_state("🔍 No tasks found matching your filters.")
    else:
        render_empty_state("🎉 No tasks yet. Add your first task above!")
else:
    for task in filtered_tasks:
        original_index = next(j for j, t in enumerate(tasks) if t['id'] == task['id'])
        result = render_task_card(task, original_index)
        
        if result[0] == "delete":
            tasks = delete_task(tasks, result[1])
            save_data(tasks)
            st.rerun()
        elif result[0] == "update":
            _, is_done, task_id = result
            if is_done != task["isCompleted"]:
                tasks = update_task_status(tasks, task_id, is_done)
                save_data(tasks)
                st.rerun()

# ============================================
# EDIT TASK MODAL
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
            tasks = edit_task(tasks, st.session_state.edit_task_id, edit_title, edit_date)
            save_data(tasks)
            del st.session_state.edit_task_id
            st.success("✅ Task updated!")
            st.rerun()
        
        if cancel_edit:
            del st.session_state.edit_task_id
            st.rerun()

# ============================================
# STATS & PROGRESS
# ============================================
st.markdown("---")
stats = get_stats(tasks)

if stats["total"] > 0:
    progress = stats["completed"] / stats["total"]
    st.progress(progress, text=f"Progress: {stats['completed']}/{stats['total']} tasks ({int(progress*100)}%)")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("📋 Total Tasks", stats["total"])
with col2:
    st.metric("✅ Completed", stats["completed"])
with col3:
    st.metric("⏳ Pending", stats["pending"])
