import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.title(f"Welcome Beginner Investor, {st.session_state['first_name']}.")
st.write('### What would you like to do today?')

if st.button('View My Positions',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/41_Positions.py')

if st.button('View Dashboard',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/42_Dashboard.py')

if st.button('Chat with Portfolio Assistant',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/43_Chat.py')
