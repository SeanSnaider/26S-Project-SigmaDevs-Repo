import logging
logger = logging.getLogger(__name__)

import streamlit as st
import pandas as pd
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.header("Visualizations")

st.write(f"### Hi, {st.session_state['first_name']}.")
st.write("View, create, update, and delete visualization records.")

col1, col2 = st.columns([1, 3])
with col1:
    user_id = st.number_input("User ID", min_value=1, value=2, step=1)
with col2:
    st.write("")

BASE_URL = "http://web-api:4000/visualizations"

tab1, tab2, tab3, tab4 = st.tabs([
    'All Visualizations',
    'Lookup Visualization',
    'Create / Update Visualization',
    'Delete Visualization'
])

#tab to look up ALL visualizations
with tab1:
    st.subheader("All Visualizations")
    if st.button("Load All Visualizations", use_container_width=True):
        try:
            res = requests.get(f"{BASE_URL}/{user_id}")
            data = res.json()
            if res.status_code != 200:
                st.error(f"Could not load visualizations: {data}")
            else:
                df = pd.DataFrame(data)
                if len(df) > 0:
                    st.dataframe(df, use_container_width=True, hide_index=True)
                else:
                    st.info("No visualizations found.")
        except Exception as e:
            logger.error(f"Error loading visualizations: {e}")
            st.error("Failed to load visualizations.")

#tab to look up a (emphasis on a, looking only for a singular one) visualization
with tab2:
    st.subheader("Lookup One Visualization")
    lookup_viz_id = st.number_input("Visualization ID", min_value=1, value=1,
                                    step=1, key="lookup_viz")
    if st.button("Get Visualization Details", use_container_width=True):
        try:
            res = requests.get(f"{BASE_URL}/{user_id}/{lookup_viz_id}")
            data = res.json()
            if res.status_code != 200:
                st.error(f"Could not load visualization: {data}")
            else:
                st.dataframe(pd.DataFrame([data]), use_container_width=True,
                             hide_index=True)
        except Exception as e:
            logger.error(f"Error loading visualization {lookup_viz_id}: {e}")
            st.error("Failed to load visualization details.")

#tab to create new visualizations
with tab3:
    st.subheader("Create New Visualization")

    with st.form("create_viz_form"):
        c1, c2 = st.columns(2)
        with c1:
            create_title = st.text_input("Title")
            create_chart_type = st.text_input("Chart Type")
        with c2:
            create_dataset_id = st.number_input("Dataset ID", min_value=1,
                                                value=1, step=1)

        create_submit = st.form_submit_button("Create Visualization")
        if create_submit:
            payload = {
                "title": create_title,
                "chart_type": create_chart_type,
                "VizDataSet": int(create_dataset_id),
            }
            try:
                res = requests.post(f"{BASE_URL}/{user_id}", json=payload)
                if res.status_code in (200, 201):
                    st.success("Visualization created successfully.")
                else:
                    st.error(f"Failed to create visualization: {res.json()}")
            except Exception as e:
                logger.error(f"Error creating visualization: {e}")
                st.error("Failed to create visualization.")

    st.divider()
    st.subheader("Update Existing Visualization")

    with st.form("update_viz_form"):
        u1, u2 = st.columns(2)
        with u1:
            update_viz_id = st.number_input("Visualization ID to Update",
                                            min_value=1, value=1, step=1)
            update_title = st.text_input("Updated Title")
        with u2:
            update_chart_type = st.text_input("Updated Chart Type")
            update_dataset_id = st.number_input("Updated Dataset ID", min_value=1,
                                                value=1, step=1)

        update_submit = st.form_submit_button("Update Visualization")
        if update_submit:
            payload = {
                "title": update_title,
                "chart_type": update_chart_type,
                "VizDataSet": int(update_dataset_id),
            }
            try:
                res = requests.put(f"{BASE_URL}/{user_id}/{update_viz_id}",
                                   json=payload)
                if res.status_code == 200:
                    st.success("Visualization updated successfully.")
                else:
                    st.error(f"Failed to update visualization: {res.json()}")
            except Exception as e:
                logger.error(f"Error updating visualization {update_viz_id}: {e}")
                st.error("Failed to update visualization.")

#tab to delete the visualizations
with tab4:
    st.subheader("Delete Visualization")
    delete_viz_id = st.number_input("Visualization ID to Delete", min_value=1,
                                    value=1, step=1, key="delete_viz")
    if st.button("Delete Visualization", use_container_width=True):
        try:
            res = requests.delete(f"{BASE_URL}/{user_id}/{delete_viz_id}")
            if res.status_code == 200:
                st.success("Visualization deleted successfully.")
            else:
                st.error(f"Failed to delete visualization: {res.json()}")
        except Exception as e:
            logger.error(f"Error deleting visualization {delete_viz_id}: {e}")
            st.error("Failed to delete visualization.")
