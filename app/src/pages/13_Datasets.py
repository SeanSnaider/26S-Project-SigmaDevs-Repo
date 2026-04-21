import logging
logger = logging.getLogger(__name__)

import streamlit as st
import pandas as pd
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.header("Datasets")

st.write(f"### Hi, {st.session_state['first_name']}.")

st.write("Review and manage datasets associated with your user account.")

col1, col2 = st.columns([1, 3])
with col1:
    user_id = st.number_input("User ID", min_value=1, value=2, step=1)
with col2:
    st.write("")
    st.write("")
    load_all = st.button(
        "Load Datasets",
        type="primary",
        use_container_width=True
    )

if not load_all:
    st.stop()

#load all datasets for the user
try:
    all_ds_res = requests.get(f"http://web-api:4000/datasets/{user_id}")
    all_ds_data = all_ds_res.json()
    if all_ds_res.status_code != 200:
        st.error(f"Could not load datasets: {all_ds_data}")
        st.stop()
    all_ds_df = pd.DataFrame(all_ds_data)
except Exception as e:
    logger.error(f"Error loading datasets for user {user_id}: {e}")
    st.error("Failed to load datasets overview.")
    st.stop()

st.subheader("All Datasets")
if len(all_ds_df) > 0:
    st.dataframe(all_ds_df, use_container_width=True, hide_index=True)
else:
    st.info("No datasets found for this user.")
    st.stop()
st.divider()

#slector for thedatasets 
dataset_options = {
    f"{row['dataset_id']} - {row['name']}": row['dataset_id']
    for _, row in all_ds_df.iterrows()
}

selected_ds = st.selectbox(
    "Select Dataset",
    list(dataset_options.keys()),
    index=0
)
dataset_id = dataset_options[selected_ds]

try:
    ds_res = requests.get(f"http://web-api:4000/datasets/{user_id}/{dataset_id}")
    ds_data = ds_res.json()
    if ds_res.status_code != 200:
        st.error(f"Could not load selected dataset: {ds_data}")
        st.stop()
except Exception as e:
    logger.error(f"Error loading dataset {dataset_id}: {e}")
    st.error("Failed to load dataset details.")
    st.stop()

st.subheader("Dataset Detail")
col1, col2, col3 = st.columns(3)
col1.metric("Dataset ID", ds_data.get("dataset_id", "—"))
col2.metric("Name", ds_data.get("name", "—"))
col3.metric("Type", ds_data.get("type", "—"))

st.divider()

st.subheader("Detailed Dataset Records")
st.dataframe(pd.DataFrame([ds_data]), use_container_width=True, hide_index=True)
st.divider()

st.subheader("Dataset Type Distribution")
if "type" in all_ds_df.columns:
    type_counts = all_ds_df["type"].value_counts().reset_index()
    type_counts.columns = ["Type", "Count"]
    st.bar_chart(type_counts.set_index("Type"), use_container_width=True)
st.divider()
