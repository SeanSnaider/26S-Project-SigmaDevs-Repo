import logging
logger = logging.getLogger(__name__)

import streamlit as st
import pandas as pd
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.header("Data Cleaning")

st.write(f"### Hi, {st.session_state['first_name']}.")

#load all cleaning methods for the overview table
try:
    all_methods_res = requests.get("http://web-api:4000/datacleaningmethods/")
    all_methods_data = all_methods_res.json()
    if all_methods_res.status_code != 200:
        st.error(f"Could not load data cleaning methods: {all_methods_data}")
        st.stop()
    all_methods_df = pd.DataFrame(all_methods_data)
except Exception as e:
    logger.error(f"Error loading all cleaning methods: {e}")
    st.error("Failed to load data cleaning methods overview.")
    st.stop()

st.subheader("All Data Cleaning Methods")
if len(all_methods_df) > 0:
    st.dataframe(all_methods_df, use_container_width=True, hide_index=True)
else:
    st.info("No data cleaning method records found.")
    st.stop()
st.divider()

#method selector for detail view
method_id_input = st.number_input(
    "Select Method ID",
    min_value=1,
    value=int(all_methods_df.iloc[0]["method_id"]) if len(all_methods_df) > 0 else 1,
    step=1
)

try:
    method_res = requests.get(f"http://web-api:4000/datacleaningmethods/{method_id_input}")
    method_data = method_res.json()
    if method_res.status_code != 200:
        st.error(f"Could not load selected method: {method_data}")
        st.stop()
except Exception as e:
    logger.error(f"Error loading method {method_id_input}: {e}")
    st.error("Failed to load method details.")
    st.stop()

st.subheader("Method Detail")
col1, col2, col3 = st.columns(3)
col1.metric("Method ID", method_data.get("method_id", "—"))
col2.metric("Method Type", method_data.get("method_type", "—"))
col3.metric("Method Order", method_data.get("method_order", "—"))

st.divider()

st.subheader("Method Detail Table")
st.dataframe(pd.DataFrame([method_data]), use_container_width=True, hide_index=True)
st.divider()

#update controls for the method
st.subheader("Update Method")

left_col, right_col = st.columns(2)
with left_col:
    new_parameter = st.text_input(
        "Update Parameter",
        value=str(method_data.get("parameter", ""))
    )
    if st.button("Save Parameter", use_container_width=True):
        payload = {"parameter": new_parameter}
        update_res = requests.put(
            f"http://web-api:4000/datacleaningmethods/{method_id_input}",
            json=payload
        )
        if update_res.status_code == 200:
            st.success("Parameter updated successfully.")
        else:
            st.error("Failed to update parameter.")

with right_col:
    new_method_type = st.text_input(
        "Update Method Type",
        value=str(method_data.get("method_type", ""))
    )
    if st.button("Save Method Type", use_container_width=True):
        payload = {"method_type": new_method_type}
        update_res = requests.put(
            f"http://web-api:4000/datacleaningmethods/{method_id_input}",
            json=payload
        )
        if update_res.status_code == 200:
            st.success("Method type updated successfully.")
        else:
            st.error("Failed to update method type.")

st.divider()

#create a new method
st.subheader("Create New Cleaning Method")
with st.form("create_method_form"):
    create_col1, create_col2 = st.columns(2)
    with create_col1:
        method_type = st.text_input("Method Type")
        parameter = st.text_input("Parameter")
    with create_col2:
        method_order = st.number_input("Method Order", min_value=1, value=1, step=1)
        cleaning_dataset = st.number_input("Dataset ID", min_value=1, value=1, step=1)

    create_submitted = st.form_submit_button("Create Method")
    if create_submitted:
        payload = {
            "method_type": method_type,
            "parameter": parameter,
            "method_order": int(method_order),
            "CleaningDataSet": int(cleaning_dataset),
        }
        create_res = requests.post("http://web-api:4000/datacleaningmethods/", json=payload)
        if create_res.status_code in (200, 201):
            st.success("New cleaning method created successfully.")
        else:
            st.error("Failed to create cleaning method. Please fill out every field.")
