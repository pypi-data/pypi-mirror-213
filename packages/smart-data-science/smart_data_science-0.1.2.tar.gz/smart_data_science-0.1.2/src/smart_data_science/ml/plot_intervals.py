"""
- Title:            ML PLOT INTERVAL PREDICTIONS. Utils for ML plots
- Project/Topic:    Smart Data Science. Practical functions for Data Science  (side project)
- Author/s:         Angel Martinez-Tenor
- Dev Date:         2023

- Status:           In progress.
"""


import pandas as pd

# import plotly.express as px
import plotly.graph_objects as go

from smart_data_science.core import logger

pd.options.plotting.backend = "plotly"


log = logger.get_logger(__name__)


def plot_interval_predictions(
    df: pd.DataFrame,
    true_col: str,
    label_units: str,
    pred_col: str = "predicted",
    pred_lower_col: str = "predicted_lower",
    pred_upper_col: str = "predicted_upper",
    confidence_interval_label: str = "95%",
    regression: bool = True,
) -> go.Figure:
    """
    Creates a plot with interval predictions using Plotly.

    :param df: pandas DataFrame with the data.
    :param target: string with the name of the target variable.
    :param title_target: string with the title of the target variable.
    :return: a Plotly Figure object.
    """

    if regression is False:
        pred_col = "predicted_proba"  # EXPERIMENTAL ONLY

    fig = go.Figure()

    # Add actual values
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df[true_col],
            name=true_col,
            marker_color="rgb(55, 83, 109)",
        )
    )
    fig.update_traces(mode="markers")

    # Add predicted values
    fig.add_trace(
        go.Scatter(x=df.index, y=df[pred_col], mode="lines+markers", name="Predicted", marker_color="rgb(55, 200, 55)")
    )

    # Add layout
    fig.update_layout(
        title="Interval Predictions",
        # xaxis=dict(title="Samples", tickmode="linear", titlefont_size=16, tickfont_size=14),
        xaxis={"title": "Samples", "tickmode": "linear", "titlefont_size": 16, "tickfont_size": 14},
        # yaxis=dict(
        #     title=label_units,
        #     titlefont_size=16,
        #     tickfont_size=14,
        # ),
        yaxis={"title": label_units, "titlefont_size": 16, "tickfont_size": 14},
        # legend=dict(x=0, y=1.0, bgcolor="rgba(255, 255, 255, 0)", bordercolor="rgba(255, 255, 255, 0)"),
        legend={"x": 0, "y": 1.0, "bgcolor": "rgba(255, 255, 255, 0)", "bordercolor": "rgba(255, 255, 255, 0)"},
    )

    # Add interval predictions
    fig.add_traces(
        [
            go.Scatter(x=df.index, y=df[pred_upper_col], mode="lines", line_color="rgba(0,0,0,0)", showlegend=False),
            go.Scatter(
                x=df.index,
                y=df[pred_lower_col],
                mode="lines",
                line_color="rgba(0,0,0,0)",
                name=confidence_interval_label,
                fill="tonexty",
                fillcolor="rgba(255, 100, 100, 0.25)",
            ),
        ]
    )
    # dict(x=1, y=0.5))
    fig.update_layout(legend={"x": 1, "y": 0.5})

    return fig
