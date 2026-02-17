import streamlit as st
from database import initialize_db
from database import add_contact, get_contacts, delete_contact, update_contact, search_contacts
from utils import apply_theme, toggle_theme, render_contact_card, render_empty_state, export_csv, get_contact_stats

initialize_db()

st.set_page_config(page_title="Advanced Contact Book", layout="centered")

# Apply theme
st.markdown(apply_theme(), unsafe_allow_html=True)

# ---- Header ----
st.title("📝 Contact Book | CodSoft Internship")
st.subheader("Manage your contacts efficiently")

# ---- Theme Toggle ----
col1, col2 = st.columns([1, 5])
with col1:
    if st.button("🌙" if st.session_state.theme == "light" else "☀️"):
        toggle_theme()

st.markdown("---")

# ---- Add New Contact Form ----
with st.expander("➕ Add New Contact", expanded=False):
    with st.form("add_contact_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Name", placeholder="Enter name...")
            phone = st.text_input("Phone", placeholder="Enter phone number...")
        
        with col2:
            email = st.text_input("Email", placeholder="Enter email address...")
            address = st.text_input("Address", placeholder="Enter address...")
        
        submit = st.form_submit_button("➕ Add Contact", use_container_width=True)
        
        if submit and name and phone:
            success = add_contact(name, phone, email, address)
            if success:
                st.success("✅ Contact added!")
                st.toast("Contact added successfully!")
                st.rerun()
            else:
                st.error("⚠️ Contact with this phone number already exists!")

# ---- Search & CSV Export ----
col_search, col_export = st.columns([3, 1])
with col_search:
    keyword = st.text_input("🔍 Search contacts...", placeholder="Search by name or phone...")

with col_export:
    contacts = get_contacts()
    csv_data = export_csv(contacts)
    st.download_button("📥 Export CSV", data=csv_data, file_name="contacts.csv", mime="text/csv")

st.markdown("---")

# ---- Contact Statistics ----
stats = get_contact_stats(contacts)
col_stat1, col_stat2 = st.columns(2)
with col_stat1:
    st.metric("📊 Total Contacts", stats["total"])

# ---- Display Contacts ----
filtered_contacts = search_contacts(keyword) if keyword else get_contacts()

st.subheader(f"📇 Your Contacts ({len(filtered_contacts)})")

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
            # Handle pending delete
            st.session_state.delete_contact_id = contact['id']
            delete_contact(contact['id'])
            st.toast("🗑️ Contact deleted successfully!")
            st.rerun()

        render_contact_card(c, on_edit, on_delete)

# ---- Edit Contact Modal ----
if "edit_contact_id" in st.session_state:
    st.markdown("---")
    st.subheader("✏️ Edit Contact")
    
    with st.form("edit_contact_form"):
        edit_name = st.text_input("Name", value=st.session_state.edit_name)
        edit_phone = st.text_input("Phone", value=st.session_state.edit_phone)
        edit_email = st.text_input("Email", value=st.session_state.edit_email)
        edit_address = st.text_input("Address", value=st.session_state.edit_address)
        
        col_save, col_cancel = st.columns(2)
        
        with col_save:
            save_edit = st.form_submit_button("💾 Save Changes", use_container_width=True)
        
        with col_cancel:
            cancel_edit = st.form_submit_button("❌ Cancel", use_container_width=True)
        
        if save_edit and edit_name and edit_phone:
            success = update_contact(
                st.session_state.edit_contact_id,
                edit_name,
                edit_phone,
                edit_email,
                edit_address
            )
            if success:
                del st.session_state.edit_contact_id
                del st.session_state.edit_name
                del st.session_state.edit_phone
                del st.session_state.edit_email
                del st.session_state.edit_address
                st.success("✅ Contact updated!")
                st.toast("Contact updated successfully!")
                st.rerun()
            else:
                st.error("⚠️ Contact with this phone number already exists!")
        
        if cancel_edit:
            del st.session_state.edit_contact_id
            del st.session_state.edit_name
            del st.session_state.edit_phone
            del st.session_state.edit_email
            del st.session_state.edit_address
            st.rerun()

