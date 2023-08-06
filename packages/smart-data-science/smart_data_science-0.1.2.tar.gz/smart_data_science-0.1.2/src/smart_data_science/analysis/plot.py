"""
- Title:            Utils Plot. Wrapper on top of Plotly
- Project/Topic:    Utils Tabular Data. Practical functions for Data Science
- Author/s:         Angel Martinez-Tenor
- Dev Date:         2017 - 2022

- Status:           Planning

- Acknowledgements. Partially Based on:
    - Personal Repo: https://github.com/angelmtenor/data-science-keras/blob/master/helper_ds.py
"""
from __future__ import annotations

import pandas as pd
import plotly.express as px

from smart_data_science.core import logger

log = logger.get_logger(__name__)


def plot_series(data, title, limit_variables=None) -> px.bar:
    """Plot a series with the input data as a horizontal bar chart
    Args:
        data (pd.Series): Input data
        title (str): Title of the plot
        limit_variables (int, optional): Limit the number of variables to plot. Defaults to None.
    """

    data = data.head(limit_variables)[::-1]
    fig = px.bar(
        data,
        orientation="h",
        text=data,
        title=title,
        width=800,
        height=200 + 40 * data.size,
    )
    fig.update_layout(
        showlegend=False,
        yaxis_title="",
        xaxis_title="",
        #     xaxis_range=[0, data.shape[0]],
    )
    fig.update_layout(
        yaxis_tickfont_size=14,
        xaxis_tickfont_size=14,
        margin={"l": 150, "b": 100},
    )

    return fig


def plot_corr_matrix(df_corr: pd.DataFrame):
    """Plot the correlation matrix of the input dataframe
    Args:
        df_corr (pd.DataFrame): Sorted Correlation Matrix dataframe
    """

    fig = px.imshow(df_corr, title="Correlation Matrix", text_auto=True, color_continuous_scale="Viridis")

    # fig = go.Figure(
    #     data=go.Heatmap(
    #         z=df_corr,
    #         x=df_corr.columns,
    #         y=df_corr.columns,
    #         colorscale="Viridis",
    #         colorbar=dict(title="Correlation"),
    #         zmin=-1,
    #         zmax=1,
    #         showscale=True,
    #         text=df_corr,
    #     )
    # )
    fig.update_layout(
        yaxis_tickfont_size=14,
        xaxis_tickfont_size=14,
        margin={"l": 150, "b": 100},
        height=250 + 50 * len(df_corr.columns),
    )
    return fig
