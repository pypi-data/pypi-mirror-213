"""
- Title:            Utils Info. Wrapper on top of Pandas for common data info functions
- Project/Topic:    Utils Tabular Data. Practical functions for Data Science
- Author/s:         Angel Martinez-Tenor
- Dev Date:         2017 - 2022

- Status:           Planning

- Acknowledgements. Partially Based on:
    - Personal Repo: https://github.com/angelmtenor/data-science-keras/blob/master/helper_ds.py
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.express as px  # type hinting only
from IPython.display import Markdown, display

from smart_data_science.analysis.plot import plot_corr_matrix, plot_series
from smart_data_science.core import logger
from smart_data_science.core.system import get_memory_usage

log = logger.get_logger(__name__)

# import seaborn as sns
# import matplotlib.pyplot as plt


def mark(markdown_string: str):
    """Show markdown text (alias for display markdown)
    Args:
        markdown_string (str): markdown string"""
    display(Markdown(markdown_string))


def ratio_to_text(part: float, total: float) -> str:
    """Return a message with the pattern: part of total (part/total*100%). Used frequently for console/log.
        e.g.: part=1097, total=1125 -> "1097/1125 (98%)"
    Args:
        part (float): Part of the total.
        total (float): Total.
    Returns:
        str: normalized message
    """
    return f"{part}/{total}" if total == 0 else f"{part}/{total} ({part/total:.1%})"


def shape_to_text(df: pd.DataFrame) -> str:
    """Return a text with the shape of the input table with format Samples(rows),  Variables(columns)
    Args:
        df (pd.DataFrame): Table
    Returns:
        str: format "s samples, v variables"
    """
    return f"{df.shape[0]} samples, {df.shape[1]} variables"


def show_diff_shape(df: pd.DataFrame, df_reduced: pd.DataFrame) -> None:
    """Print a message with the differences in samples & variables from table df_start to table df_end
        Used to show the reduction of a table after a preprocessing step
    Args:
        df (pd.DataFrame): Source Table
        df_reduced (pd.DataFrame): Reduced Table
    """
    if df.shape == df_reduced.shape:
        log.info(f"Table not modified: {shape_to_text(df)}")
    else:
        log.info(f"Table modified to {shape_to_text(df_reduced)}")


def info_data(
    df: pd.DataFrame,
    table_name: str = "",
    unique: bool = False,
    missing: bool = False,
    var_names=False,
    plot=False,
    exclude_unique: list = None,
    samples: int = 5,
    types: bool = False,
    corr_matrix: bool = False,
    corr_matrix_sort_col: str = None,
) -> None:
    """Print the shape (rows, columns) & the variables of the input table.
    If unique/missing = True: Show graphs with distinct/missing values of each variable. Used in EDA notebooks
    Args:
        df (pd.DataFrame): Input Table
        table_name (str, optional): Caption Name to show (markdown). Defaults to "".
        unique (bool, optional): Show distinct values of each variable. Defaults to False.
        missing (bool, optional): Show missing values of each variable. Defaults to False.
        var_names (bool, optional): Show the list of variables. Defaults to False.
        plot (bool, optional): Plot the graphs. Defaults to False.
        exclude (list, optional): Exclude the variables in the list for plotting unique. Defaults to None.
        samples (int, optional): Number of samples to show. Defaults to 5.
        types (bool, optional): Show the types of each variable. Defaults to False.
        corr_matrix (bool, optional): Show the correlation matrix. Defaults to False.
        corr_matrix_sort_col (str, optional): Sort the correlation matrix by the column. Defaults to None.
    """
    if table_name:
        log.info(Markdown(f"## {table_name}"))
    log.info(f"{df.shape[0]:,} samples and {df.shape[1]:,} variables  ({get_memory_usage(df)} MB)")
    if var_names:
        log.info(f"{list(df)}")
    if unique:
        if exclude_unique is None:
            # exclude numerical variables
            exclude_unique = df.select_dtypes(include=np.number).columns.tolist()
        fig_unique = show_unique(df, plot=plot, exclude=exclude_unique)
        if fig_unique:
            fig_unique.show()
    if missing:
        fig_missing = show_missing(df, plot=plot)
        if fig_missing:
            fig_missing.show()

    if types:
        log.info(f"Types:\n{df.dtypes}")

    if corr_matrix:
        show_corr_matrix(df, sort_col=corr_matrix_sort_col)

    if samples:
        if samples > 0:
            log.info("Sample (random):")
            return df.sample(samples)

    return None


# ----- PLOTLY DEPENDANT


def show_unique(
    df: pd.DataFrame, columns: list[str] = None, plot: bool = True, limit_variables=None, exclude: list = None
) -> px.bar:
    """Plot or print (plot=False) the unique values of the list of the input columns/variables of the table
    Args:
        df (pd.DataFrame): Input table
        columns (list[str]): List of columns/Variables. Defaults to None (all columns).
        plot (bool, optional): Plot sorted graph with unique values of each variable. Defaults to True.
        limit_variables (int, optional): Limit the number of variables to plot. Defaults to None.
        exclude (list, optional): Exclude the variables in the list for plotting unique. Defaults to None.
    """

    data = df.copy()
    if isinstance(columns, str):
        columns = [columns]
    elif columns is None:
        columns = list(df)

    data = df[columns].nunique().sort_values(ascending=False)
    data = data[data > 0]

    if plot:
        data_to_plot = data.copy()
        if exclude:
            data_to_plot = data_to_plot.drop(exclude)
        fig = plot_series(data_to_plot, title="Unique Values", limit_variables=limit_variables)

        return fig

    with pd.option_context("display.max_rows", None, "display.max_columns", None):
        log.info(f"UNIQUE VALUES\n{data}")
    return None


# def show_distinct(df, figsize=None):
#     """
#     Display the number of the unique values of all the variables of the input dataframe
#     """
#     pd.options.plotting.backend = "matplotlib"
#     size = df.shape[0]
#     distinct_values = df.nunique()
#     distinct_values = distinct_values.sort_values(ascending=True)
#     value_ratio = distinct_values / size
#     if not figsize:
#         figsize = (8, value_ratio.shape[0] // 2 + 1)
#     figure = plt.figure(figsize=figsize)
#     plt.xlim([0, 1])
#     plt.xlabel("Distinct values / Size")
#     plt.title("Distinct Values")
#     value_ratio.plot(kind="barh")
#     for index, value in enumerate(distinct_values):
#         plt.text(value / size + 0.01, index, str(value))
#     plt.show()
#     return figure


def show_missing(df: pd.DataFrame, columns: list[str] = None, plot: bool = True, limit_variables=None) -> px.bar:
    """Plot or print (plot=False) the missing values of the list of the input columns/variables of the table
    Args:
        df (pd.DataFrame): Input table
        columns (list[str]): List of columns/Variables. Defaults to None (all columns).
        plot (bool, optional): Plot sorted graph with unique values of each variable. Defaults to True.
        limit_variables (int, optional): Limit the number of variables to plot. Defaults to None.
    """

    data = df.copy()
    data = data.replace(r"^\s*$", np.nan, regex=True)  # Blank spaces will be considered as empty

    if isinstance(columns, str):
        columns = [columns]
    elif columns is None:
        columns = list(data)

    data = data.isnull().sum().sort_values(ascending=False)
    data = data[data > 0]

    if data.size == 0:
        log.info("No missing values found\n")
        return None

    if plot:
        fig = plot_series(data, title="Missing Values", limit_variables=limit_variables)
        return fig

    log.info("MISSING VALUES \n ----------------")
    with pd.option_context("display.max_rows", None, "display.max_columns", None):
        log.info(data)
        return None


# --------------


def display_full(ds: pd.DataFrame | pd.Series, max_width=None) -> None:
    """Display complete rows of pandas series or dataframe  (no valid for logging)
    Args:
        ds (pd.DataFrame | pd.Series): Input pandas series or dataframe
        max_width (int, optional): Maximum width of the display. Defaults to None.
    """
    with pd.option_context("display.max_rows", None, "display.max_columns", None, "display.max_colwidth", max_width):
        display(ds)


def show_frame(df: pd.DataFrame, dataname: str = "", distinct: bool = True):
    """Display number of samples, variables & number of unique values for each variable.
    if 'display_missing' True: Also display a bar with missing values
    If the input is a pandas series, it is converted into a pandas dataframe with index as a column
    Args:
        df (pd.DataFrame): Input dataframe
        dataname (str): Name of the dataset
        distinct (bool): If True, display the number of unique values for each variable
    """
    if isinstance(df, pd.Series):
        df = pd.DataFrame(df.copy()).reset_index()
    if dataname:
        mark(f"### {dataname} <br><br>")
    mark(f"**SAMPLES: {df.shape[0]}**")
    mark(f"**VARIABLES: {df.shape[1]}**")
    if distinct:
        show_unique(df)


def get_frame_unique(df: pd.DataFrame) -> pd.DataFrame:
    """Return a dataframe with the number of unique values for each variable
    Args:
        df (pd.DataFrame): Input dataframe
    Returns:
        pd.DataFrame: Dataframe with the names of the variables of the input dataframe as index and the number
        of unique values (nunique) as "Unique Values"
    """
    distinct = {}
    for i in list(df):
        distinct[i] = df[i].nunique()
    df_dist = pd.DataFrame(data=distinct.items())
    df_dist.columns = ["Variable", "Unique Values"]
    df_dist = df_dist.set_index("Variable")
    return df_dist


def get_corr_matrix(df: pd.DataFrame, only_numeric=True, sort_col: str = None):
    """Return the correlation matrix of the input dataframe
    Args:
        df (pd.DataFrame): Input dataframe
        only_numeric (bool, optional): If True, only numeric variables are considered. Defaults to True.
        sort_by (list, optional): List of variables to sort the correlation matrix. Defaults to [].
    Returns:
        pd.DataFrame: Correlation matrix
    """

    if only_numeric:
        corr_matrix = df.corr(numeric_only=True)
    else:
        corr_matrix = df.corr()
    # sort by target
    if sort_col is not None:
        corr_matrix = corr_matrix.sort_values(by=sort_col, ascending=False)
        # list of sorted columns
        column_order = corr_matrix.index.tolist()
        # reorder the matrix
        corr_matrix = corr_matrix.loc[column_order, column_order]
    # remove the upper triangle
    corr_matrix = corr_matrix.where(np.tril(np.ones(corr_matrix.shape), k=-1).astype(bool))
    return corr_matrix


def show_corr_matrix(df: pd.DataFrame, sort_col: str = None) -> None:
    """Plot the correlation matrix of the input dataframe
    Args:
        df (pd.DataFrame): Input dataframe
        sort_col (list, optional): List of variables to sort the correlation matrix. Defaults to [].

    """

    df_corr = get_corr_matrix(df, sort_col=sort_col).round(3)
    # fig = px.imshow(corr_matrix, title="Correlation Matrix", width=800, height=800)

    fig = plot_corr_matrix(df_corr)

    fig.show()
