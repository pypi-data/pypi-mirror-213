"""
- Title:            Utils User Interface. Streamlit template for UI with tabular data
- Project/Topic:    Utils Tabular Data. Practical functions for Data Science
- Author/s:         Angel Martinez-Tenor
- Dev Date:         2017 - 2022

- Status:           Planning
"""

# TO IMPROVE: Add UI functions from Other Developments, as tabular-ml-product-template

from __future__ import annotations

import time

import pandas as pd
import streamlit as st

from smart_data_science import info_system, load_sample, logger
from smart_data_science.ui.ui_info import explore_elements_of_frame, perform_query, ui_info_data

# from smart_data_science.ui.ui_io import load_image

# PATH_LOGO = "logo.jpg"

LABEL = "Utils Tabular Data"
APP_PASSWORD = "AI_2023"

MAX_SAMPLES_SHOWN_IN_TABLES = 20000  # Max samples shown in each table to avoid overload in UI

# Streamlit Content
SECTION_EXPLORE = " Explore"

SECTIONS = (SECTION_EXPLORE,)


# Session State

SESSION_STATE_VARIABLES: list = []
SESSION_STATE_DATAFRAMES: list = []

for session_var in SESSION_STATE_VARIABLES:
    if session_var not in st.session_state:
        st.session_state[session_var] = None


for session_var in SESSION_STATE_DATAFRAMES:
    if session_var not in st.session_state:
        st.session_state[session_var] = pd.DataFrame()

# Logger
if ("logger" not in st.session_state) and st.session_state["access_granted"]:
    log = logger.init(level=10, simple_format=True, subfolder="exploration_app", filename_modifier="")
    st.session_state["logger"] = log
else:
    log = logger.get_logger(__name__)
    if ("init_info_shown" not in st.session_state) and (st.session_state["access_granted"]):
        log.info("\n\n--------------- Exploration App --------------- \n")
        log.info(info_system())
        st.session_state["init_info_shown"] = True

current_date = pd.Timestamp.today()
current_date_string = current_date.strftime("%Y_%m_%d")


start_time = time.time()


# set page title
st.set_page_config(page_title=f"{LABEL}", layout="wide")  # , page_icon='')

# Hide Menu button & Footer
st.markdown(
    """ <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """,
    unsafe_allow_html=True,
)

# Reduce Padding
st.markdown(
    f""" <style>
    .reportview-container .main .block-container{{
        padding-top: {0}rem;
        padding-right: {5}rem;
        padding-left: {3}rem;
        padding-bottom: {2}rem;
    }} </style> """,
    unsafe_allow_html=True,
)


def main() -> None:
    """Main Streamlit app (UI). (successful password only)"""
    st.header(selected_section)

    # -----------------------------EXPLORE PREDICTION SECTION. Priority: Interactive Dependency Graphs

    if selected_section == SECTION_EXPLORE:
        df = load_sample()

        ui_info_data(df.astype("object").reset_index(), show_features=True)

        st.write("#### Filter the Data")
        df_sub = perform_query(df)

        ui_info_data(df_sub.astype("object").reset_index(), default_on=True)

        if not df_sub.empty:
            st.write("#### Explore individual samples")
            explore_elements_of_frame(df_sub, ordered=True)


# Streamlit Entrypoint

# logo = ui_io.load_image(PATH_LOGO)
# if logo:
#     st.sidebar.image(logo)

st.sidebar.title(LABEL)
st.sidebar.header("Exploration App for Utils Tabular Data")
# st.sidebar.write(f"Template:\n{UI_TEMPLATE}")
selected_section = st.sidebar.selectbox(label="", options=(SECTIONS), index=0)

if st.session_state["access_granted"] is None:
    # log.debug("Requesting password")
    st.write("### Enter the Password:")
    password = st.text_input("", type="password")
    if password == APP_PASSWORD:
        st.session_state["access_granted"] = True
        st.write("")
        st.success("Access Granted")
        # log.debug("Access Granted")
        st.write("")
        time.sleep(0.5)
        st.experimental_rerun()

if st.session_state["access_granted"]:
    main()
    st.write("_" * 30)
    end_time = time.time()
    time_elapsed_info = f"Ready ({end_time-start_time:.2f} seconds)"
    # log.debug(time_elapsed_info)
    st.write()
    st.write(time_elapsed_info)
