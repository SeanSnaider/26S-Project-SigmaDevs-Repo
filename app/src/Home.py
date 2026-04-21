##################################################
# This is the main/entry-point file for the
# sample application for your project
##################################################

# Set up basic logging infrastructure
import logging
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# import the main streamlit library as well
# as SideBarLinks function from src/modules folder
import streamlit as st
from modules.nav import SideBarLinks

# streamlit supports regular and wide layout (how the controls
# are organized/displayed on the screen).
st.set_page_config(layout='wide')

# If a user is at this page, we assume they are not
# authenticated.  So we change the 'authenticated' value
# in the streamlit session_state to false.
st.session_state['authenticated'] = False

# Use the SideBarLinks function from src/modules/nav.py to control
# the links displayed on the left-side panel.
# IMPORTANT: ensure src/.streamlit/config.toml sets
# showSidebarNavigation = false in the [client] section
SideBarLinks(show_home=True)

# ***************************************************
#    The major content of this page
# ***************************************************

logger.info("Loading the Home page of the app")
st.title('PortIQ')
st.write('#### Hi! As which user would you like to log in?')

personas = [
    "Andrew Rock - Quantitative Trader",
    "John Data - Data Analyst",
    "Katrina Williams - Chief Information Officer",
    "Jane Doe - Beginner Investor",
]

persona_map = {
    "Andrew Rock - Quantitative Trader": {
        "role": "quant_trader",
        "first_name": "Andrew",
        "page": "pages/00_Quant_Trader_Home.py",
    },
    "John Data - Data Analyst": {
        "role": "data_analyst",
        "first_name": "John",
        "page": "pages/10_Data_Analyst_Home.py",
    },
    "Katrina Williams - Chief Information Officer": {
        "role": "CIO",
        "first_name": "Katrina",
        "page": "pages/20_CIO_IAM.py",
    },
    "Jane Doe - Beginner Investor": {
        "role": "beginner_user",
        "first_name": "Jane",
        "page": "pages/40_Beginner_User_Home.py",
    },
}

selected = st.selectbox("Select a persona", personas)

if st.button("Log In", type="primary", use_container_width=True):
    user = persona_map[selected]
    st.session_state['authenticated'] = True
    st.session_state['role'] = user["role"]
    st.session_state['first_name'] = user["first_name"]
    logger.info(f"Logging in as {selected}")
    st.switch_page(user["page"])
