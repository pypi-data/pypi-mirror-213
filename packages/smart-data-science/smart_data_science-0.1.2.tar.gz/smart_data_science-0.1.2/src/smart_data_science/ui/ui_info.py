"""
- Title:            Info Utils User Interface (Streamlit)
- Project/Topic:    Utils Tabular Data. Practical functions for Data Science
- Author/s:         Angel Martinez-Tenor
- Dev Date:         2017 - 2022

- Status:           Planning
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st

from smart_data_science.analysis import info
from smart_data_science.core import io

MAX_SAMPLES_SHOWN_IN_TABLES = 20000  # Max samples shown in each table to avoid overload in UI

current_date = pd.Timestamp.today()
current_date_string = current_date.strftime("%Y_%m_%d")


def info_file(filepath: str | Path, st_col=None) -> None:
    """Show the update date of the filepath in the streamlit's UI (= creation_date)
    Highlighted in Green: Updated in the current date
    Highlighted in yellow: Not updated in the current date (useful for changes & incidents data)
    Args:
        filepath: The path to the file to get the update date
        st_col: The streamlit column to use for the UI
    """
    creation_date = io.get_creation_date(filepath)
    creation_date_string = creation_date.strftime(" %B %d, %Y - %H:%M")
    if not st_col:
        st_col, _ = st.columns([2, 2.5])
    if creation_date:
        if creation_date.date() == current_date.date():
            st_col.success(f"Last Update: &nbsp;&nbsp; {creation_date_string} &nbsp;&nbsp; UP TO DATE")
        else:
            st_col.write(f"Last update: &nbsp;&nbsp; {creation_date_string}")
    else:
        st_col.write(f"{filepath} does not found")


def ui_info_data(
    df: pd.DataFrame,
    n_samples: int = MAX_SAMPLES_SHOWN_IN_TABLES,
    show_features: bool = False,
    default_on: bool = False,
) -> None:
    """Show number of rows, columns, graph with unique values of each variable and the first n_samples
    Args:
        df: The dataframe to show info about
        n_samples: The number of samples to show in the table
        show_table: Show the table with the first n_samples
        show_features: Show the columns/variables of the dataframe
        show_unique: Show the unique values of each variable
        show_missing: Show the missing values of each variable

    """

    st.write(f"**{df.shape[0]} Samples &nbsp; &nbsp; &nbsp; {df.shape[1]} Variables**")

    numerical = df.select_dtypes(include=np.number).columns.tolist()
    non_numerical = df.select_dtypes(exclude=np.number).columns.tolist()

    col1, _, col2 = st.columns([3, 1, 3])  # 1, 3, 1, 3])
    if show_features:
        # Text features if any....

        col1.write("Numerical Variables")
        for i in numerical:
            col1.write(f"**- {i}**")

        col2.write("Non Numerical Variables")
        for i in non_numerical:
            col2.write(f"**- {i}**")

    show_summary_distinct_missing = st.checkbox("Show Distinct & Missing Values", value=False)
    if show_summary_distinct_missing:
        col1, _, col2 = st.columns([3, 1, 3])  # 1, 3, 1, 3])
        col1.write(info.show_unique(df))
        missing_plot = info.show_missing(df)
        if missing_plot is not None:
            col2.write(info.show_missing(df))
        else:
            col2.write("No missing values")

    show_table = st.checkbox("Show Table", value=default_on)
    if show_table:
        if n_samples < df.shape[0]:
            st.write(f"Showing {n_samples} out of {df.shape[0]} Samples:")
        st.write(df.head(n_samples))


# def ui_info_data_old(df, n_samples=5000, show_summary_distinct_checkbox=True, key=None):
#     """Show in the UI the number of rows, columns, graph with unique
#       values of each variable and the first n_samples"""
#     st.write(f'Rows: {"&nbsp; "} {df.shape[0]} {"&nbsp; "*4} Columns: {"&nbsp; "} {df.shape[1]}')

#     if show_summary_distinct_checkbox:
#         show_summary_distinct = st.checkbox("Show Distinct Values", key=key)
#         if show_summary_distinct:
#             st.write(info.show_unique(df.reset_index()))
#     if n_samples >= df.shape[0]:
#         st.write("All data:")
#     else:
#         st.write(f"First {n_samples} rows:")
#     st.write(df.head(n_samples))


def explore_elements_of_frame(
    df: pd.DataFrame,
    key: str = "EXPLORE_ELEMENT_DATA",
    ordered: bool = False,
) -> str:
    """Show a selection box with the index of the input dataframe and display the selected element or subdataframe
    Args:
        df: The dataframe to show the selection box for
        key: The key to use for the selection box (optional)
        ordered: If True, the selection box will be ordered (optional)
    Returns:
        str: The selected element

    """
    # st.write("_" * 30)
    col1, _, _, _, _ = st.columns([3, 3, 1, 1, 1])

    if df.shape[0] == 0:
        st.warning("Empty Table")
        return None

    options = df.index.unique()

    if ordered:
        options = options.sort_values()

    selected_id = col1.selectbox(label="Select an ID to explore:", options=options, key=key)
    st.write("")
    df_selected = df.loc[selected_id]

    if df_selected.shape[0] == 1 or isinstance(df_selected, pd.Series):
        if st.checkbox("Show as text", True):
            show_empty_variables = st.checkbox(label="Show Empty Variables", value=True)

            # if isinstance(df_selected,pd.Series):
            for index, value in df_selected.items():
                if value or show_empty_variables:
                    st.write(f"- **{index}**: {value}")
        else:
            st.write(pd.DataFrame(df_selected).T.astype("str"))
    else:
        st.write(pd.DataFrame(df_selected).T.astype("str"))

    return selected_id


def explore_elements_of_frame_lite(df, key="EXPLORE_ELEMENT"):
    """Show a selection box with the index of the frame 'df' and display the selected element (text) or subdataframe"""
    options = df.index.unique().sort_values()
    selected_id = st.selectbox(label="Select an ID to explore:", options=options, key=key)
    st.write("")
    df_selected = df.loc[selected_id]

    if isinstance(
        df_selected, pd.Series
    ):  # if only 1 result found (series instead of dataframe), print series as text:
        for index, value in df_selected.items():
            if value:
                st.write(f"- **{index}**: {value}")
    else:
        st.write(df_selected.reset_index())


def perform_query(df: pd.DataFrame) -> pd.DataFrame:
    """
    Display filters to select range of variables & return the subdataframe after applying the filters
    Args:
        df: The dataframe to perform the query on
    Returns:
        pd.DataFrame: The subdataframe after applying the query
    """
    df = df.copy()
    col1, _, col2, _, col3 = st.columns([3, 1, 3, 1, 4])

    numerical = df.select_dtypes(include=np.number).columns.tolist()
    non_numerical = df.select_dtypes(exclude=np.number).columns.tolist()

    for i in numerical[:3]:  # LAYOUT SCENARIO-DEPENDENT
        min_value = int(df[i].min())
        max_value = int(df[i].max())
        selected_values = col1.slider(i, min_value, max_value, (min_value, max_value))
        df = df[df[i] >= selected_values[0]]
        df = df[df[i] <= selected_values[1]]

    for i in numerical[3:]:
        min_value = int(df[i].min())
        max_value = int(df[i].max())
        selected_values = col2.slider(i, min_value, max_value, (min_value, max_value))
        df = df[df[i] >= selected_values[0]]
        df = df[df[i] <= selected_values[1]]

    for i in non_numerical:
        values = sorted(df[i].unique().tolist())
        selected_values = col3.multiselect(label=i, options=values, default=values)
        df = df[df[i].isin(selected_values)]

    return df


def show_result_header():
    """Custom result header to display in all the function sections"""
    st.write("_" * 30)
    st.markdown("### Results:")
    st.write("")


def show_dict_as_table(input_dict: dict, label: str) -> None:
    """Show a dictionary as a table
    Args:
        input_dict (dict): dictionary to show
        label (str): label of the table (header)
    """
    series = pd.Series(input_dict)
    series.name = label
    st.table(series)
