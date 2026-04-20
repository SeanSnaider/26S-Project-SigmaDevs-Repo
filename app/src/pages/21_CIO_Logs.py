import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

BASE_URL = "http://web-api:4000"

st.title("App Administration - Logs")

# --- Logs table ---
# TODO: requires a GET /action/logs?limit=7 endpoint that returns the last 7 actions with username + action_type
st.write("### Recent Logs")
search_user = st.text_input("Search User")

try:
    load_resp = requests.get(f"{BASE_URL}/action/actions")
    deploy_resp = requests.get(f"{BASE_URL}/action/deployments")

    logs = []
    if load_resp.status_code == 200:
        logs.append(load_resp.json())
    if deploy_resp.status_code == 200:
        logs.append(deploy_resp.json())

    if search_user:
        logs = [l for l in logs if search_user.lower() in l.get("username", "").lower()]

    if logs:
        st.dataframe(logs, use_container_width=True)
    else:
        st.info("No logs found.")
except Exception as e:
    st.error(f"Error fetching logs: {e}")

st.divider()

# --- User actions ---
st.write("### User Management")
with st.form("user_actions_form"):
    user_id_input = st.number_input("User ID", min_value=1, step=1)
    remove_user = st.checkbox("Remove user")
    encrypt_all = st.checkbox("Encrypt data for all users?")
    submitted = st.form_submit_button("Submit")

    if submitted:
        if remove_user:
            try:
                del_resp = requests.delete(f"{BASE_URL}/user/users/{int(user_id_input)}")
                if del_resp.status_code == 200:
                    st.success(f"User {int(user_id_input)} removed successfully.")
                else:
                    st.error(f"Error removing user: {del_resp.json().get('error', 'Unknown error')}")
            except Exception as e:
                st.error(f"Delete request failed: {e}")

        if encrypt_all:
            try:
                enc_resp = requests.put(f"{BASE_URL}/user/users")
                if enc_resp.status_code == 200:
                    st.success("All user data encrypted successfully.")
                else:
                    st.error(f"Error encrypting data: {enc_resp.json().get('error', 'Unknown error')}")
            except Exception as e:
                st.error(f"Encrypt request failed: {e}")
