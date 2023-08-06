"""
- Title:            ML PLOT REGRESSOR. Utils for ML plots
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


def plot_predictions_vs_target(df: pd.DataFrame, target: str, predicted="predicted", group_col=None) -> go.Figure:
    """
    Creates a plot with the predictions using Plotly -Regression Only
    Args:
        df: pandas DataFrame with the data.
        target: string with the name of the target variable.
        predicted: string with the name of the predicted variable.
        group_col: string with the name of the column to group by.

    """

    fig = df.plot(
        kind="scatter", x=target, y=predicted, color=group_col, title=f"Prediction vs. Actual {target} (test set)"
    )
    return fig


# def regressor_eval(reg, x_test, y_test, plotly_fig=True, show_plot=True):
#     """Show the evaluation of a ML regressor (tested on tree-based sklearn models)"""
#     y_pred = reg.predict(x_test)
#     display(Markdown(f"Test size: {x_test.shape[0]} samples"))
#     display(
#         Markdown(
#             "R2 Score: **{:.3f}** &nbsp;&nbsp;&nbsp; MAD: **{:.3f}**".format(
#                 r2_score(y_test, y_pred), median_absolute_error(y_test, y_pred)
#             )
#         )
#     )

#     if show_plot:
#         # add to inputs of the function?
#         title = "Test set evaluation"
#         xaxis_title = None
#         # yaxis_title = (None,)

#         lay = go.Layout(
#             title=title,
#             width=700,
#             height=500,
#             xaxis_title=xaxis_title,
#             yaxis_title=xaxis_title,
#             plot_bgcolor="rgba(0,0,0,0)",
#         )

#         df = pd.DataFrame(data={"True": y_test, "Predicted": y_pred})
#         fig = df.plot.hist()
#         fig.update_layout(lay, barmode="overlay")
#         fig.update_traces(opacity=0.8)

#         fig.show()
