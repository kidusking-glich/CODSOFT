import streamlit as st
import json
import os
from datetime import date, datetime

# ============================================
# THEME STYLES
# ============================================
def apply_theme():
    if "theme" not in st.session_state:
        st.session_state.theme = "light"
    
    if st.session_state.theme == "dark":
        return """
        <style>
        .stApp {background-color: #121212 !important; color: #e0e0e0 !important;}
        .stContainer {border: 1px solid #2c2c2c !important; border-radius: 8px !important;}
        .stTextInput input, .stDateInput input {background-color: #1e1e1e !important; color: #e0e0e0 !important; border: 1px solid #333 !important;}
        .stSelectbox div[data-baseweb="select"] > div {background-color: #1e1e1e !important; color: #e0e0e0 !important;}
        .stButton > button {background-color: #1e1e1e !important; color: #e0e0e0 !important; border: 1px solid #333 !important;}
        .stButton > button:hover {background-color: #2c2c2c !important; border-color: #4a9eff !important;}
        .stFormSubmitButton > button[kind="secondary"] {background-color: #4a9eff !important; color: white !important; border: none !important;}
        div[data-testid="stMetric"] {background-color: #1e1e1e !important; border: 1px solid #2c2c2c !important; border-radius: 8px !important; padding: 10px !important;}
        div[data-testid="stMetricLabel"] {color: #888 !important;}
        div[data-testid="stMetricValue"] {color: #e0e0e0 !important;}
        h2, h3 {color: #e0e0e0 !important;}
        .empty-state {color: #aaa !important;}
        </style>
        """
    else:
        return """
        <style>
        .stContainer {border: 1px solid #e0e0e0 !important; border-radius: 8px !important;}
        .stFormSubmitButton > button[kind="secondary"] {background-color: #4a9eff !important; color: white !important; border: none !important;}
        .empty-state {color: #666 !important;}
        </style>
        """

def toggle_theme():
    st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"
    st.rerun()

def get_empty_state_color():
    return "#aaa" if st.session_state.theme == "dark" else "#666"

# ============================================
# DATA MANAGEMENT
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

# ============================================
# TASK OPERATIONS
# ============================================
import uuid

def generate_task_id():
    return str(uuid.uuid4())[:8]

def add_task(tasks, title, due_date):
    new_id = generate_task_id()
    tasks.append({
        "id": new_id,
        "title": title,
        "isCompleted": False,
        "dueDate": str(due_date)
    })
    return tasks

def update_task_status(tasks, task_id, is_completed):
    for task in tasks:
        if task['id'] == task_id:
            task['isCompleted'] = is_completed
            break
    return tasks

def delete_task(tasks, task_id):
    return [t for t in tasks if t['id'] != task_id]

def edit_task(tasks, task_id, new_title, new_date):
    for task in tasks:
        if task['id'] == task_id:
            task['title'] = new_title
            task['dueDate'] = str(new_date)
            break
    return tasks

# ============================================
# FILTER & SORT
# ============================================
def filter_tasks(tasks, search_query="", filter_option="All"):
    filtered = tasks.copy()
    
    if search_query:
        filtered = [t for t in filtered if search_query.lower() in t['title'].lower()]
    
    if filter_option == "Pending":
        filtered = [t for t in filtered if not t['isCompleted']]
    elif filter_option == "Completed":
        filtered = [t for t in filtered if t['isCompleted']]
    elif filter_option == "Overdue":
        today = date.today()
        filtered = [t for t in filtered 
                   if not t['isCompleted'] and datetime.strptime(t['dueDate'], '%Y-%m-%d').date() < today]
    
    return filtered

def sort_tasks(tasks, sort_option="Pending First"):
    if sort_option == "Pending First":
        return sorted(tasks, key=lambda x: x['isCompleted'])
    elif sort_option == "Completed First":
        return sorted(tasks, key=lambda x: not x['isCompleted'])
    elif sort_option == "Due Date":
        return sorted(tasks, key=lambda x: datetime.strptime(x['dueDate'], '%Y-%m-%d'))
    return tasks

# ============================================
# STATS
# ============================================
def get_stats(tasks):
    completed = sum(1 for t in tasks if t['isCompleted'])
    return {
        "total": len(tasks),
        "completed": completed,
        "pending": len(tasks) - completed
    }

# ============================================
# UI COMPONENTS
# ============================================
def render_task_card(task, original_index):
    with st.container(border=True):
        col1, col2, col3, col4, col5 = st.columns([0.08, 0.40, 0.25, 0.12, 0.15])
        
        # Checkbox
        is_done = col1.checkbox("Done", value=task["isCompleted"], key=f"check_{task['id']}", label_visibility="collapsed")
        
        # Title
        col2.markdown(f"**{task['title']}**")
        
        # Status badge
        if is_done:
            col3.markdown(f"<span style='background-color: #28a745; color: white; padding: 4px 12px; border-radius: 12px; font-size: 12px;'>✅ Completed</span>", unsafe_allow_html=True)
        else:
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
        
        # Delete button (simple confirmation with inline buttons)
        delete_key = f"confirm_delete_{task['id']}"
        if delete_key not in st.session_state:
            st.session_state[delete_key] = False
        
        if not st.session_state[delete_key]:
            if col5.button("🗑️", key=f"delete_{task['id']}"):
                st.session_state[delete_key] = True
                st.rerun()
        else:
            # Show confirmation inline using buttons_container
            col5.markdown("❓ **Confirm?**")
            col5a, col5b = col5.columns(2)
            if col5a.button("✅", key=f"yes_{task['id']}", use_container_width=True):
                return "delete", task['id']
            if col5b.button("❌", key=f"no_{task['id']}", use_container_width=True):
                st.session_state[delete_key] = False
                st.rerun()
        
        return "update", is_done, task['id']

def render_empty_state(message):
    color = get_empty_state_color()
    st.markdown(f"""
    <div style="text-align: center; padding: 40px; color: {color};">
        {message}
    </div>
    """, unsafe_allow_html=True)
