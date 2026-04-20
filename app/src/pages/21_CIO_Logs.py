import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

BASE_URL = "http://web-api:4000"

st.title("App Administration - Logs")

# Logs table 
st.write("### Recent Logs")
search_user = st.text_input("Search User")

try:
    load_resp = requests.get(f"{BASE_URL}/action/actions") # get all the dataset load actions
    deploy_resp = requests.get(f"{BASE_URL}/action/deployments") # get all the app delpoyment actions

    logs = []
    if load_resp.status_code == 200:
        logs.append(load_resp.json()) # api call success
    if deploy_resp.status_code == 200:
        logs.append(deploy_resp.json()) # api call success

    if search_user:
        logs = [l for l in logs if search_user.lower() in l.get("username", "").lower()] # search for user for any actions they performed

    if logs:
        st.dataframe(logs, use_container_width=True) # make a table
    else:
        st.info("No logs found.") # no logs found error
except Exception as e:
    st.error(f"Error fetching logs: {e}") # api call failed

st.divider()

# User actions
st.write("### User Management")
with st.form("user_actions_form"): 
    user_id_input = st.number_input("User ID", min_value=1, step=1)
    remove_user = st.checkbox("Remove user")
    encrypt_all = st.checkbox("Encrypt data for all users?")
    submitted = st.form_submit_button("Submit")

    if submitted: 
        if remove_user: # removes specified user with DELETE request
            try:
                del_resp = requests.delete(f"{BASE_URL}/user/users/{int(user_id_input)}")
                if del_resp.status_code == 200: # api call success
                    st.success(f"User {int(user_id_input)} removed successfully.")
                else:
                    st.error(f"Error removing user: {del_resp.json().get('error', 'Unknown error')}") # no user found error
            except Exception as e: # api call failed
                st.error(f"Delete request failed: {e}")

        if encrypt_all: # encrypts password data for all users
            try:
                enc_resp = requests.put(f"{BASE_URL}/user/users")
                if enc_resp.status_code == 200: # api call success
                    st.success("All user data encrypted successfully.")
                else:
                    st.error(f"Error encrypting data: {enc_resp.json().get('error', 'Unknown error')}") # no users found error
            except Exception as e:
                st.error(f"Encrypt request failed: {e}") # api call failed
