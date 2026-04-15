import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.title('Chief Information Officer Home Page')
st.write('### What would you like to do today?')

if st.button('Update ML Models',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/21_ML_Model_Mgmt.py')
