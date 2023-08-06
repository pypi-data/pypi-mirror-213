"""
- Title:            Utils Clean. Wrapper on top of Pandas for common data cleaning and normalization (best practices)
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
from pandas.errors import ParserError

from smart_data_science.core import logger
from smart_data_science.core.system import get_memory_usage

log = logger.get_logger(__name__)


#  ---- BASIC CLEANING / NORMALIZATION FUNCTIONS -----

# DATAFRAMES -----------------------------------------------------------------------------------------------------------


def remove_rows(df: pd.DataFrame, ignore_index=True) -> pd.DataFrame:
    """Remove duplicated rows and rows with no data
    Args:
        df (pd.DataFrame): Input table
    Returns:
        pd.DataFrame: Table with useful rows
    """
    df = df.copy()
    source_nrows = df.shape[0]

    if not ignore_index:
        index_name = df.index.name
        df = df.reset_index()

    df = df.drop_duplicates()  # .reset_index(drop=True)

    if not ignore_index:
        df = df.set_index(index_name)

    # df = df.loc[:,~df.columns.duplicated()].copy()
    df = df.dropna(axis=0, how="all")
    nrows_removed = source_nrows - df.shape[0]
    if nrows_removed > 0:
        log.debug(f"{nrows_removed} Rows Removed ({nrows_removed/source_nrows*100:.1f}%)")
    return df


def remove_columns(df: pd.DataFrame, drop_constant_columns=False) -> pd.DataFrame:
    """Remove columns with no relevant data
    Args:
        df (pd.DataFrame): Input table
    Returns:
        pd.DataFrame: Table without non useful data
    """

    # A: Remove columns without values or with only one value

    df = df.copy()
    source_variables = set(df)
    source_n_variables = df.shape[1]
    df = df.dropna(axis=1, how="all")

    if drop_constant_columns:
        df = df.loc[:, df.nunique() > 1]

    if removed_variables := list(source_variables - set(df)):  # pylint: disable-msg=E0001
        n_removed_variables = len(removed_variables)
        log.debug(f"{n_removed_variables} Variables Removed ({n_removed_variables/source_n_variables*100:.1f}%):")
        log.debug(removed_variables)
    return df


def normalize_variable_names(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize the variable names: Remove special characters, spaces and convert to lowercase
    Args:
        df (pd.DataFrame): Input table
    Returns:
        pd.DataFrame: Table with normalized variable names
    """
    df = df.copy()
    df.columns = df.columns.str.lower().str.replace(" ", "_", regex=False).str.replace("[^a-z0-9_]", "", regex=True)

    # normalize index name if string
    if isinstance(df.index.name, str):
        df.index.name = df.index.name.lower().replace(" ", "_").replace("[^a-z0-9_]", "")
    # df.columns = [c.replace("\n", " ") for c in list(df)]  # remove carriage return from headers
    df.columns = [c[:30] for c in list(df)]  # limit header length
    return df


def restore_schema(df: pd.DataFrame, df_ref: pd.DataFrame, n_decimals=2) -> pd.DataFrame:
    """Restore the schema of a dataframe. Used after a resample ot rolling operation (integers covert to floats)
    Args:
        df (pd.DataFrame): Input table
        df_ref (pd.DataFrame): Reference (it can be empty)
        n_decimals (int, optional): Number of decimals to round the float numbers. Defaults to 2.
    Returns:
        pd.DataFrame: Table with restored schema
    """
    df = df.copy()
    # df = df[df_ref.columns]
    for c in df_ref.columns:
        if df_ref[c].dtype.kind in "iu":
            df[c] = df[c].round()
        elif df_ref[c].dtype.kind in "f":
            df[c] = df[c].round(n_decimals)
        df[c] = df[c].astype(df_ref[c].dtype)
    return df


def optimize_schema(
    df: pd.DataFrame, uniqueness_threshold: float = 0.2, reduce_to_32_bits=True, force_categorical: list = None
) -> pd.DataFrame:
    """Optimize schema and Reduce memory usage of a dataframe
    Args:
        df (pd.DataFrame): Input table
        uniqueness_threshold (float, optional): Threshold to consider a variable as categorical. Defaults to 0.2.
        reduce_to_32_bits (bool, optional): Reduce memory usage from 64 to 32 bits. Defaults to True.
        categorical_columns (list, optional): List of columns to force as categorical. Defaults to None.

    Returns:
        pd.DataFrame: table with reduced memory usage
    """
    df = df.copy()
    source_memory = get_memory_usage(df)

    # convert to best type (pandas)
    df = df.convert_dtypes()

    # detect datetime columns (not in pandas)
    for c in list(df.columns[df.dtypes == "object"]) + list(df.columns[df.dtypes == "string"]):
        try:
            df[c] = pd.to_datetime(df[c])
            log.debug(f"Column {c} converted to datetime")
        except (ParserError, ValueError):
            pass

    if reduce_to_32_bits:  # Reduce from 64 to 32 bits
        df[df.select_dtypes("Float64").columns] = df.select_dtypes("Float64").astype("Float32")
        df[df.select_dtypes("Int64").columns] = df.select_dtypes("Int64").astype("Int32")

    for i in df.select_dtypes("string").columns:
        if df[i].nunique() / df.shape[0] < uniqueness_threshold:
            df[i] = df[i].astype("category")

    if force_categorical:
        for i in force_categorical:
            df[i] = df[i].astype("category")

    for i in df.select_dtypes("category").columns:
        df[i] = df[i].cat.remove_unused_categories()

    reduced_memory = get_memory_usage(df)
    if reduced_memory <= source_memory:
        log.debug(f" - Optimize Schema: Data Size reduced from {source_memory} to {reduced_memory} MB")
    else:
        log.warning(f" - Optimize Schema: Data Size increased from {source_memory} to {reduced_memory} MB")
    return df


def normalize_data(df: pd.DataFrame, drop_constant_columns=False, ignore_index=True) -> pd.DataFrame:
    """Normalize the data: Optimize the schema, Reduce Memory and Clean Variable Names
    Args:
        df (pd.DataFrame): Input table
    Returns:
        pd.DataFrame: Normalized table
    """
    df = df.copy()

    df = remove_columns(df, drop_constant_columns)
    df = remove_rows(df, ignore_index)

    df = normalize_variable_names(df)
    df = optimize_schema(df)
    return df


def force_schema(df: pd.DataFrame, schema: dict):
    """Force the schema of the dataframe to the given types
    Args:
        df (pd.DataFrame): Dataframe to force schema
        schema (dict): Schema to force
    Returns:
        pd.DataFrame: Dataframe with forced schema
    """
    df = df.copy()

    for i in df.columns:
        if i in schema.get("int_vars", []):
            df[i] = df[i].round().astype("Int32")
        elif i in schema.get("float_vars", []):
            df[i] = df[i].round(2).astype("Float32")
        elif i in schema.get("categorical_vars", []):
            # df[i] = df[i].apply(lambda x: None if isinstance(x, list) else x)
            df[i] = df[i].astype("category")
        elif i in schema.get("bool_vars", []):
            df[i] = df[i].astype("bool")
    return df


def check_variables(df: pd.DataFrame, needed_variables: list) -> None:
    """
    Check if all the variables from the list or set 'needed_variables' are columns of the input dataframe 'df.
    Generate an assertion error showing the missing the variables if any
    Args:
        df (pd.DataFrame): Input dataframe
        needed_variables (list): List of variables to check
    """
    missing_variables = set(needed_variables).difference(set(df))
    assert not missing_variables, f"ERROR: MISSING VARIABLES: {missing_variables}"


# TEXT ---------------------------------------------------------------------


def remove_words_with_digits(text: str) -> str:
    """
    Return a string with words not containing digits
    Args:
        text (str): Input text
    Returns:
        str: Text without words containing digits
    """
    clean_text = " ".join(s for s in text.split() if not any(c.isdigit() for c in s))
    return clean_text


custom_stopwords = ["by", "of", "for", "in", "and", "on", "to"]
pattern_custom_stopwords = rf"\b(?:{'|'.join(custom_stopwords)})\b"


def clean_text_for_clustering(text_series: pd.Series) -> pd.Series:
    """
    Custom cleaning for text data: remove digits, stopwords, punctuation, etc.
    Args:
        text_series (pd.Series): Input text series
    Returns:
        pd.Series: Cleaned text series
    """
    text_series = text_series.fillna("EMPTY")  # fix tf idf issues
    text_series = text_series.str.lower()
    text_series = text_series.copy()
    start_nunique = text_series.nunique()
    text_series = text_series.str.replace("[^a-zA-Z]", " ", regex=True).str.strip()
    text_series = text_series.apply(remove_words_with_digits)
    # text_series = text_series.apply(remove_months)
    text_series = text_series.str.replace(r"\b\w\b", "", regex=True)
    text_series = text_series.str.replace(pattern_custom_stopwords, "", regex=True)
    text_series = text_series.replace(r"\s+", " ", regex=True)
    # text_series = text_series.str[:600]
    text_series = text_series.fillna("EMPTY")  # fix tf idf issues
    end_unique = text_series.nunique()
    print(f"Text series cleaned. From {start_nunique} to {end_unique} unique texts")
    return text_series


def clean_text_series_basic(text_series: pd.Series) -> pd.Series:
    """Apply basic text cleaning (used for all text variables)
    Args:
        text_series (pd.Series): Raw Text Series
    Returns:
        pd.Series: Normalized Text Series
    """
    # Basic cleaning applied to all text variables
    ds = text_series.copy().replace(np.nan, "", regex=True).astype(str)
    ds = ds.str.replace(r"[\,,\.]", "", regex=True)  # TESTING
    ds = ds.str.strip()
    return ds


def clean_text_series_advanced(text_series: pd.Series) -> pd.Series:
    """Apply Custom text cleaning (used for selected variables only)
    Args:
        text_series (pd.Series): Raw Text Series
    Returns:
        pd.Series: Normalized Text Series
    """
    ds = text_series.copy()
    ds = (
        ds.str.lower()
    )  # by default all are upper(), but lower() is the standard method used  (also offer a better visualization)
    ds = ds.str.replace(r"\w*\d\w*", "", regex=True)  # remove words containing digits
    ds = ds.str.replace("[^a-zA-Z]", " ", regex=True)  # remove non alphanumeric characters
    # ds = ds.str.replace(r"(?<!\S)[a-z]+(?!\S)", "", regex=True)  # remove words with non alphanumeric characters
    ds = ds.str.replace(r"\b\w\b", "", regex=True)  # added: remove all single characters
    # ds = ds.str.findall('\w{4,}').str.join('')  # remove all words with less than x chars
    # Remove Stopwords.
    # CUSTOM_STOPWORDS = ["from", "to", "stock", "see", "attached", "illustration", "with", "a", "and", "the", "in"]
    # pattern_custom_stopwords = r"\b(?:{})\b".format("|".join(CUSTOM_STOPWORDS))
    # ds = ds.str.replace(pattern_custom_stopwords, '', regex=True)
    ds = ds.replace(r"\s+", " ", regex=True).str.strip()
    return ds


# LIST ---------------------------------------------------------------------
def empty_list(df: pd.DataFrame) -> np.ndarray:
    """
    Return an array of empty lists: used to fill a column of the dataframe with an empty list
    Args:
        df (pd.DataFrame): Input dataframe
    Returns:
        np.array: Array of empty lists
    """
    return np.empty((len(df), 0)).tolist()


def remove_items(input_list: list, existing_list: list) -> list:
    """
    Remove the items of the 'input_list' that matches any item of the 'existing_list'
    Args:
        input_list (list): List of items to be removed
        existing_list (list): List of items to be compared
    Returns:
        list: List of items wof 'input_list' without the items of the 'existing_list'
    """
    clean_list = [i for i in input_list if i not in existing_list]
    clean_list = list(set(clean_list))
    return clean_list


def string_to_list(txt: str, sep: str = ",") -> list:
    """
    Returns a list of stripped strings from a comma separated input text  (or custom separation 'sep')
    Args:
        txt (str): Input text
        sep (str, optional): Separator. Defaults to ","
    Returns:
        list: List of strings
    """
    clean_list = []
    if txt:
        items = txt.split(sep)
        clean_list = [i.strip() for i in items]
    return clean_list


# def remove_months(text):
#     """
#     Return a string with month names removed
#     """
#     clean_text = " ".join(s for s in text.split() if s.lower() not in months + months_short)
#     return clean_text
