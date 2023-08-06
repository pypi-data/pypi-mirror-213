"""
- Title:            ML PLOT CLASSIFIER. Utils for ML plots
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


def plot_target_distribution(target_series):
    """Barplot target distribution"""
    lay = go.Layout(
        yaxis_title="Count",
        xaxis_title="Target",
        title="Target Distribution",
        width=500,
        height=300,
        margin={"t": 50, "b": 20},
        plot_bgcolor="rgba(0,0,0,0)",
    )

    v = target_series.value_counts()
    labels = [str(i) for i in v.index]
    if all(i.isnumeric() for i in labels):
        v.index = (
            "C" + str(i) for i in labels
        )  # numbers only as string are not well displayed in the confusion matrix axes

    fig = v.plot.bar()
    fig.update_layout(lay)
    fig.show()


# def plot_fancy_confusion_matrix(y_true, y_pred, labels, normalized=True):
#     """adapted:  https://github.com/oegedijk/explainerdashboard/blob/master/explainerdashboard/explainer_plots.py"""

#     cm = confusion_matrix(y_true, y_pred)

#     cm_original = cm.copy()
#     cm_sum = cm.sum(axis=1)

#     if labels is None:
#         labels = [str(i) for i in range(cm.shape[0])]

#     else:
#         labels = [str(i) for i in labels]
#         if all([i.isnumeric() for i in labels]):
#             labels = [
#                 "C" + str(i) for i in labels
#             ]  # numbers only as string are not well displayed in the confusion matrix axes

#     if normalized:
#         cm = np.round(100 * cm / cm.sum(axis=1), 1)
#         zmax = 100
#     else:
#         zmax = len(y_true)

#     data = [
#         go.Heatmap(
#             z=cm,
#             x=labels,
#             y=labels,
#             zmin=0,
#             zmax=zmax,
#             colorscale="Blues",
#             showscale=False,
#         )
#     ]
#     layout = go.Layout(
#         title="Normalized Confusion Matrix (%)",
#         xaxis=dict(side="bottom"),  # constrain="domain"),
#         yaxis=dict(autorange="reversed", side="left", scaleanchor="x", scaleratio=1),
#         plot_bgcolor="#fff",
#         yaxis_title="True Label",
#         xaxis_title="Predicted Label",
#         height=500,
#         width=500,
#         margin=dict(t=100, b=100),
#         # margin=dict(t=50)
#     )
#     fig = go.Figure(data, layout)
#     annotations = []
#     for x in range(cm.shape[0]):
#         for y in range(cm.shape[1]):
#             text = f"{cm[x, y]:1g}"  # + '%' if normalized else str(cm[x,y])
#             color = "#fff" if cm[x, y] > zmax / 2 else "#000"
#             annotations.append(
#                 go.layout.Annotation(
#                     x=fig.data[0].x[y],
#                     y=fig.data[0].y[x],
#                     text=text,
#                     showarrow=False,
#                     font=dict(size=15 - 0.5 * len(labels), color=color),
#                     hovertext=f"{cm_original[x, y]} of {cm_sum[x]}",
#                 )
#             )

#     fig.update_layout(annotations=annotations)
#     fig.show()
