import streamlit as st
from database import initialize_db
from database import add_contact, get_contacts, delete_contact, update_contact, search_contacts
from utils import apply_theme, toggle_theme, render_contact_card, render_empty_state, export_csv

initialize_db()

st.set_page_config(page_title="Advanced Contact Book", layout="centered")


from database import add_contact, get_contacts, update_contact, delete_contact, search_contacts

st.markdown(apply_theme(), unsafe_allow_html=True)

# ---- Header ----
st.title("📝 Contact Book | CodSoft Internship")
st.subheader("Manage your contacts efficiently")

# ---- Theme Toggle ----
col1, col2 = st.columns([1, 5])
with col1:
    if st.button("🌙" if st.session_state.theme == "light" else "☀️"):
        toggle_theme()

# ---- Add New Contact ----
with st.form("add_contact_form", clear_on_submit=True):
    name = st.text_input("Name")
    phone = st.text_input("Phone")
    email = st.text_input("Email")
    address = st.text_input("Address")
    submit = st.form_submit_button("➕ Add Contact")

    if submit and name and phone:
        add_contact(name, phone, email, address)
        st.success("✅ Contact added!")
        st.rerun()

# ---- Search & CSV Export ----
col_search, col_export = st.columns([3, 1])
with col_search:
    keyword = st.text_input("🔍 Search contacts...")

with col_export:
    contacts = get_contacts()
    csv_data = export_csv(contacts)
    st.download_button("📥 Export CSV", data=csv_data, file_name="contacts.csv", mime="text/csv")

# ---- Display Contacts ----
filtered_contacts = search_contacts(keyword) if keyword else get_contacts()

if not filtered_contacts:
    render_empty_state("📭 No contacts found. Add your first contact above!")
else:
    for c in filtered_contacts:
        def on_edit(contact):
            st.session_state.edit_contact_id = contact['id']
            st.session_state.edit_name = contact['name']
            st.session_state.edit_phone = contact['phone']
            st.session_state.edit_email = contact['email']
            st.session_state.edit_address = contact['address']
            st.rerun()

        def on_delete(contact):
            st.session_state.delete_contact_id = contact['id']
            st.rerun()

        render_contact_card(c, on_edit, on_delete)
