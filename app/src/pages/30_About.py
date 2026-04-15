import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.write("# About this App")

st.markdown(
    """
    PortIQ, an application that allows both technical and non technical users the ability to learn how to trade through interactive realtime graphs, games, and customizable dashboards. When building this application, we decided to utilize existing platforms, such as Yahoo! Finance, to get our data. With this data, we format in a surplus of ways to allow for our users to learn and understand market patterns faster. With users being able to pick where they get their data from and how to organize it, we bring something that is not on the market, the ability to learn and customize. We are building this application to not only help those who are experienced, but those who are new to all investing. With games such as the start market game, where we start users with $100,000 dollars of paper money, and allow them to make investments and give them AI feedback on their trades, we allow them not only to learn what decisions to make, but why they should make them. More experienced users are also favored, having customizable dashboards and selectable databases allows those with immense experience to make their own custom profile to best help their needs. PortIQ, whether it is being used by someone who just started, or the most experienced trader, will allow everyone to make the most informed and proper financial decisions to turn their 100’s into 1000’s.


    Stay tuned for more information and features to come!
    """
)

# Add a button to return to home page
if st.button("Return to Home", type="primary"):
    st.switch_page("Home.py")
