"""
- Title:            Utils Transform. Wrapper on top of Pandas for practical data transformation & Preprocessing steps
- Project/Topic:    Utils Tabular Data. Practical functions for Data Science
- Author/s:         Angel Martinez-Tenor
- Dev Date:         2017 - 2022

- Status:           Planning

- Acknowledgements. Partially Based on:
    - Personal Repo: https://github.com/angelmtenor/data-science-keras/blob/master/helper_ds.py
"""

from __future__ import annotations

import pandas as pd

from smart_data_science.core import logger

log = logger.get_logger(__name__)

#  ---- BASIC TRANSFORMATION FUNCTIONS --------


def join_variables(ds: pd.Series, sep: str = " ") -> str:
    """Join columns: Return a concatenated string with the variables separated by sep from a series (index + value)
    Args:
        ds (pd.Series): Input Series
        sep (str, optional): Separator. Defaults to " ".
    Returns:
        str: Concatenated String
    """
    return sep.join(ds.values.astype(str))


def diff_frames(df1: pd.DataFrame, df2: pd.DataFrame, columns: list[str] = None) -> pd.DataFrame:
    """Return a table composed by rows not matched between the inputs dataframes only
        If a list of columns/variables are provided, the dataframes will be filtered before the comparison
    Args:
        df1 (pd.DataFrame): Table 1 to compare
        df2 (pd.DataFrame): Table 2 to compare
        columns (list[str], optional): _description_. Defaults to empty (all columns).
    Returns:
        pd.DataFrame: Table with not matched rows only
    """
    df1, df2 = df1.copy(), df2.copy()
    if columns:
        df1, df2 = df1[columns], df2[columns]
    return pd.concat([df1.drop_duplicates(), df2.drop_duplicates()]).drop_duplicates(keep=False)


def fill_nan_on_index(df, df_cache, warn_duplicated_index_in_cache=True) -> pd.DataFrame:
    """Fill NA/NaN values of the input df table with df_cache based on the index. Allows duplicated indexes.
    This is a Workaround of a limitation in Pandas fillna method in indexes with duplicated values.
    Args:
        df (pd.DataFrame): Input dataframe
        df_cache (pd.DataFrame): Cache dataframe with structure as df
        warn_duplicated_index_in_cache (bool, optional): Warn if duplicated indexes in cache. Defaults to True.

    Returns:
        pd.DataFrame: Dataframe with filled NA/NaN values. Original columns & original indexes ordered
    """
    df_original = df.copy()
    usecols = df_original.columns

    df["sorted_index"] = range(len(df))  # generate incremental column to keep original order (index may be duplicated)

    if warn_duplicated_index_in_cache and df_cache.index.has_duplicates:
        log.warning("Cache input with duplicated values \n")
        df_cache = df_cache[~df_cache.index.duplicated(keep="first")]

    df_temp = df[~df.index.duplicated(keep="first")].copy()
    df_temp = df_temp.fillna(df_cache)
    df = df.join(df_temp, how="left", lsuffix="_old")
    df["sorted_index"] = df["sorted_index_old"]

    # reconstruct original table
    df = df.sort_values("sorted_index", ascending=True)[usecols]

    # assert df_original.index.equals(df.index), log.critical("Indexes are not equal")
    try:
        assert df_original.index.equals(df.index)
    except AssertionError:
        log.critical("Indexes are not equal")

    return df


def multi_to_single_index(index):
    """
    Concatenates a list of tuples into a single index.

    Parameters:
    index (list): List of tuples to be concatenated.

    Returns:
    pandas.Index: Concatenated single index.
    """
    # Map each tuple to a string and join with space
    concatenated = [" ".join(map(str, tpl)) for tpl in index]

    # Create a pandas Index from the concatenated list
    single_index = pd.Index(concatenated)

    return single_index


# FUTURE IMPROVEMENT: INCLUDE A FUNCTION/CLASS FOR DATA ANONYMIZATION
