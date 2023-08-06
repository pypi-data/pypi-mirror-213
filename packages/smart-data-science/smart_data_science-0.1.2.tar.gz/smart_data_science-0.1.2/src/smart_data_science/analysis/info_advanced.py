"""
- Title:            Utils Info Advanced. Wrapper on top of Pandas and Pandas Profiling
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
from pandas_profiling import ProfileReport
from scipy.spatial import distance
from sklearn.preprocessing import StandardScaler

from smart_data_science.core import logger

log = logger.get_logger(__name__)


def generate_report(df: pd.DataFrame, title: str, save=True) -> ProfileReport:
    """Generate and return a pandas profiling report
    Args:
        df (pd.DataFrame): Input table
        title (str): Title of the report
    Returns:
        ProfileReport: Pandas Profiling Report
    """

    log.debug(f"Generating Report of {title}")
    report = ProfileReport(df, title=title, minimal=True)
    if save:
        filename = f"Report {title}.html"
        report.to_file(filename)
        log.info(f"Report saved: {filename}")
    return report


def find_similar_samples(
    df: pd.DataFrame,
    target_sample: pd.Series,
    filter_cols: list | None = None,
    numerical_cols: list | None = None,
    n_samples: int = 10,
) -> pd.DataFrame:
    """
    Find the n most similar samples to the target sample in the given dataset.

    Parameters:
    -----------
    df : pandas.DataFrame
        The dataset to search for similar samples in.
    target_sample : pandas.Series with the sample to compare against.
    filter_cols : list of str or None, default=None
        A list of column names to filter the dataset by before searching for similar samples.
    numerical_cols : list of str or None, default=None
        A list of numeric column names to use in calculating the similarity between samples.
    n_samples : int, default=10
        The number of most similar samples to return.

    Returns:
    --------
    pandas.DataFrame
        A dataframe with the selected target row and the n most similar rows found in the dataset.
    """
    df_filtered = df.copy()

    # filter by the selected rows
    if filter_cols is not None:
        for col in filter_cols:
            df_filtered = df_filtered[df_filtered[col] == target_sample[col]].copy()

    df_target = pd.DataFrame(target_sample).T

    if len(df_filtered) == 0:
        print("No similar samples found in the dataset for the selected rows")
        print("Try removing some filters")
        return df_target

    df_all = pd.concat([df_target, df_filtered])

    # Select only the numeric rows
    df_num = df_all[numerical_cols].copy()

    # Convert to numpy array
    if isinstance(df_num, pd.DataFrame):
        X = df_num.values
    else:
        X = df_num

    # Standardize the data
    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    # Get the first row
    row = X[0]

    # Get the Euclidean distance between the first row and all the other rows
    distances = np.array([distance.euclidean(row, X[i]) for i in range(len(X))])

    # Get the n rows with the lowest distance
    my_rows = np.argsort(distances)[1 : n_samples + 1]  # noqa: E203

    # Return the n rows as a list
    nearest_samples = list(my_rows)

    # Build the resulting dataframe
    df_result = df_all.iloc[[0] + list(nearest_samples), :].drop_duplicates()

    return df_result
