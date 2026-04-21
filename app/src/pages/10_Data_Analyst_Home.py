# the starting page for john data

import logging

logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.title(f"Welcome Data Analyst, {st.session_state['first_name']}.")
st.write('### What would you like to do today?')

if st.button('View Dashboard Layouts',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/11_Dashboard_Layouts.py')

if st.button('Manage Data Cleaning Methods',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/12_Data_Cleaning.py')

if st.button('Manage Datasets',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/13_Datasets.py')

if st.button('Manage Visualizations',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/14_Visualizations.py')
