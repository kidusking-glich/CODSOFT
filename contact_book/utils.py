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
        .stApp {background-color: #121212; color: #e0e0e0;}
        .stButton>button {background-color: #1e1e1e; color:#e0e0e0;}
        .stTextInput>div>input {background-color:#1e1e1e; color:#e0e0e0;}
        </style>
        """
    else:
        return """
        <style>
        .stApp {background-color: #f5f5f5; color: #111;}
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
    with st.container():
        cols = st.columns([3, 2, 2, 1])
        cols[0].markdown(f"**{contact['name']}**\n📞 {contact['phone']}\n✉️ {contact['email']}\n🏠 {contact['address']}")
        cols[1].markdown(f"Created: {contact['created_at']}")
        if cols[2].button("✏️ Edit", key=f"edit_{contact['id']}"):
            on_edit(contact)
        if cols[3].button("🗑️ Delete", key=f"delete_{contact['id']}"):
            on_delete(contact)
        st.markdown("---")

# =========================
# Render Empty State
# =========================
def render_empty_state(message):
    st.markdown(f"""
    <div style='text-align:center; padding:40px; color:#888;'>
        {message}
    </div>
    """, unsafe_allow_html=True)
