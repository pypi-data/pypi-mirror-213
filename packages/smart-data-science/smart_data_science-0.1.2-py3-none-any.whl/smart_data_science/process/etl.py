"""
- Title:            Utils ETL. Wrapper on top of io & transforms modules for automated ETL processes
- Project/Topic:    Utils Tabular Data. Practical functions for Data Science
- Author/s:         Angel Martinez-Tenor
- Dev Date:         2017 - 2022

- Status:           Planning
"""

from __future__ import annotations

import pandas as pd

from smart_data_science.core import logger
from smart_data_science.core.io import get_available_datafiles, load_datafile
from smart_data_science.process.clean import normalize_data

log = logger.get_logger(__name__)


def load_normalize_all_data_files(
    datapath: str, match_string: str = "", usecols: list[str] = None
) -> dict[str, pd.DataFrame]:
    """Load the data files (parquet, csv or xlsx) found in datapath, preprocess them, and return a dict with filenames
     as keys and dataframes as values
    Args:
        datapath (str): Directory with datafiles to preprocess
        match_string (str, optional): if provided, the files of preprocess must contain this text, . Defaults to "".
        usecols (list, optional): List of columns/variables to load. Defaults to None (all columns).
    Returns:
        dict[str, pd.DataFrame]: Dictionary with key = table name (file name), and value = Normalized Table
    """
    dict_df = {}
    dict_filepaths = get_available_datafiles(datapath, match_string)
    for table_name, filepath in dict_filepaths.items():
        log.info(f"Loading {table_name}")
        df = load_datafile(filepath, usecols)
        log.info(f"Preprocessing {table_name}")
        df = normalize_data(df)
        dict_df[table_name] = df
    log.info(f"Preprocessing finished. {len(dict_df)} tables loaded")

    return dict_df
