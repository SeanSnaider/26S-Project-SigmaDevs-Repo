import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome Quantitative Trader, {st.session_state['first_name']}.")
st.write('### What would you like to do today?')

if st.button('View Portfolio Performance',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/01_Portfolio_Performance.py')

if st.button('Compare Strategy vs Benchmark',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/02_Strategy_Benchmark.py')

if st.button('Analyze Risk Metrics',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/03_Risk_Analysis.py')

if st.button('Upload Trading Logs',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/04_Trading_Logs.py')