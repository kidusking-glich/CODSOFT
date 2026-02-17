import streamlit as st
from datetime import datetime
import csv
import io

# =========================
# Theme & styling helpers
# =========================
def apply_theme():
    if "theme" not in st.session_state:
        st.session_state.theme = "light"

    if st.session_state.theme == "dark":
        return """
        <style>
        .stApp {background-color: #121212 !important; color: #e0e0e0 !important;}
        .stContainer {border: 1px solid #2c2c2c !important; border-radius: 8px !important;}
        .stTextInput input, .stTextArea textarea {background-color: #1e1e1e !important; color: #e0e0e0 !important; border: 1px solid #333 !important;}
        .stButton > button {background-color: #1e1e1e !important; color: #e0e0e0 !important; border: 1px solid #333 !important;}
        .stButton > button:hover {background-color: #2c2c2c !important; border-color: #4a9eff !important;}
        .stFormSubmitButton > button[kind="secondary"] {background-color: #4a9eff !important; color: white !important; border: none !important;}
        div[data-testid="stMetric"] {background-color: #1e1e1e !important; border: 1px solid #2c2c2c !important; border-radius: 8px !important; padding: 10px !important;}
        div[data-testid="stMetricLabel"] {color: #888 !important;}
        div[data-testid="stMetricValue"] {color: #e0e0e0 !important;}
        h1, h2, h3 {color: #e0e0e0 !important;}
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

# =========================
# CSV Export
# =========================
def export_csv(contacts):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Name", "Phone", "Email", "Address", "Created At"])
    for c in contacts:
        writer.writerow([c["id"], c["name"], c["phone"], c["email"], c["address"], c["created_at"]])
    return output.getvalue()

# =========================
# Render Contact Card
# =========================
def render_contact_card(contact, on_edit, on_delete):
    # Convert sqlite3.Row to dict if needed
    contact_dict = dict(contact) if not isinstance(contact, dict) else contact
    
    with st.container(border=True):
        # Use columns for better layout
        col_info, col_date, col_actions = st.columns([3, 1.5, 1])
        
        # Contact Information with icons
        with col_info:
            st.markdown(f"**👤 {contact_dict['name']}**")
            if contact_dict.get('phone'):
                st.markdown(f"📞 {contact_dict['phone']}")
            if contact_dict.get('email'):
                st.markdown(f"✉️ {contact_dict['email']}")
            if contact_dict.get('address'):
                st.markdown(f"🏠 {contact_dict['address']}")
        
        # Created date
        with col_date:
            if contact_dict.get('created_at'):
                st.caption(f"📅 Added: {contact_dict['created_at']}")
        
        # Action buttons
        with col_actions:
            # Check for delete confirmation state
            delete_confirm_key = f"confirm_delete_{contact_dict['id']}"
            
            if delete_confirm_key not in st.session_state:
                st.session_state[delete_confirm_key] = False
            
            if not st.session_state[delete_confirm_key]:
                col_edit, col_del = st.columns(2)
                if col_edit.button("✏️", key=f"edit_{contact_dict['id']}", use_container_width=True):
                    on_edit(contact_dict)
                if col_del.button("🗑️", key=f"delete_{contact_dict['id']}", use_container_width=True):
                    st.session_state[delete_confirm_key] = True
                    st.rerun()
            else:
                # Show confirmation
                st.markdown("❓ **Confirm?**")
                col_yes, col_no = st.columns(2)
                if col_yes.button("✅", key=f"yes_{contact_dict['id']}", use_container_width=True):
                    on_delete(contact_dict)
                    st.session_state[delete_confirm_key] = False
                    st.rerun()
                if col_no.button("❌", key=f"no_{contact_dict['id']}", use_container_width=True):
                    st.session_state[delete_confirm_key] = False
                    st.rerun()

# =========================
# Render Empty State
# =========================
def render_empty_state(message):
    theme_color = "#aaa" if st.session_state.theme == "dark" else "#666"
    st.markdown(f"""
    <div style="text-align: center; padding: 40px; color: {theme_color};">
        {message}
    </div>
    """, unsafe_allow_html=True)

# =========================
# Get Contact Stats
# =========================
def get_contact_stats(contacts):
    return {
        "total": len(contacts),
    }

