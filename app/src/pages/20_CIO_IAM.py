import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

BASE_URL = "http://web-api:4000"

st.title("IAM - PortIQ")

# --- Search user ---
st.write("### Users")
search_name = st.text_input("Search username")

try:
    response = requests.get(f"{BASE_URL}/user/users")
    if response.status_code == 200:
        users_data = response.json()
        if search_name:
            users_data = [u for u in users_data if search_name.lower() in u.get("username", "").lower()]
        st.dataframe(users_data, use_container_width=True)
    else:
        st.warning("No users found.")
except Exception as e:
    st.error(f"Error fetching users: {e}")

st.divider()

# --- Search role and view permissions ---
st.write("### Role Permissions")
role_id_input = st.number_input("Search Role (by Role ID)", min_value=1, step=1, value=1)

try:
    role_resp = requests.get(f"{BASE_URL}/role/roles/{int(role_id_input)}")
    if role_resp.status_code == 200:
        perms = role_resp.json()
        if perms:
            st.caption(f"Role Name: **{perms[0].get('name', 'N/A')}**")
        st.dataframe(perms, use_container_width=True)
    else:
        st.warning("Role not found or has no permissions.")
except Exception as e:
    st.error(f"Error fetching permissions: {e}")

st.divider()

# --- Add permission to role ---
st.write("### Add Permission to Role")
with st.form("add_permission_form"):
    target_role_id = st.number_input("Role ID", min_value=1, step=1)
    permission_id = st.number_input("Permission ID", min_value=1, step=1)
    table_id = st.number_input("Table ID", min_value=1, step=1)
    can_read = st.checkbox("Can Read")
    can_write = st.checkbox("Can Write")
    can_create = st.checkbox("Can Create")
    submitted = st.form_submit_button("Submit")

    if submitted:
        payload = {
            "permission_id": int(permission_id),
            "table_id": int(table_id),
            "Can_Read": int(can_read),
            "Can_Write": int(can_write),
            "Can_CREATE": int(can_create),
        }
        try:
            post_resp = requests.post(
                f"{BASE_URL}/role/roles/{int(target_role_id)}/permissions",
                json=payload
            )
            if post_resp.status_code == 201:
                st.success("Permission added successfully.")
            else:
                st.error(f"Error: {post_resp.json().get('error', 'Unknown error')}")
        except Exception as e:
            st.error(f"Request failed: {e}")
