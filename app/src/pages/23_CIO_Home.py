import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.title(f"Welcome CIO {st.session_state['first_name']}.")
st.write('### What would you like to do today?')

if st.button('Manage Users & Roles (IAM)',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/20_CIO_IAM.py')

if st.button('View System Logs',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/21_CIO_Logs.py')

if st.button('LLM Management',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/22_CIO_LLM_Mgmt.py')
