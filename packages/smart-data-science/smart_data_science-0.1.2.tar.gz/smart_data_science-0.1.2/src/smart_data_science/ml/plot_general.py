"""
- Title:            ML PLOT. Utils for ML plots (generic)
- Project/Topic:    Smart Data Science. Practical functions for Data Science  (side project)
- Author/s:         Angel Martinez-Tenor
- Dev Date:         2023

- Status:           In progress.
"""


import pandas as pd

from smart_data_science.core import logger

# import plotly.express as px
# import plotly.graph_objects as go


pd.options.plotting.backend = "plotly"


log = logger.get_logger(__name__)


# TO BE REMOVED IF NO FUNCTIONALITY IS ADDED


# def feature_importances(model, data, target, top=10, plotly_fig=True):
#     """Show feature importances (tested on tree-based sklearn models)"""

#     features = data.columns
#     features = [i for i in features if i not in target]

#     n = len(features)
#     if not top or n < top:
#         top = n

#     importances = pd.DataFrame(data={"Importances": model.feature_importances_}, index=features)
#     importances = importances.sort_values("Importances", ascending=False).round(3).head(top)

#     figsize = (6, importances.shape[0] // 3 + 1)

#     if plotly_fig:
#         lay = go.Layout(
#             title="Most important features",
#             width=600,
#             height=importances.shape[0] * 35 + 30,
#             margin=dict(t=50, b=40),
#             plot_bgcolor="rgba(0,0,0,0)",
#         )

#         fig = importances.sort_values("Importances", ascending=True).plot.bar(
#             # kind="bar",
#             # color="blue",
#             orientation="h",
#         )
#         fig.update_layout(lay)
#         fig.show()

#     else:
#         importances.plot.barh(figsize=figsize)
#         plt.gca().invert_yaxis()
#         plt.show()


# def mapbox(
#     df,
#     lat,
#     lon,
#     color_column=None,
#     size=None,
#     size_max=15,
#     hover_name=None,
#     zoom=7,
#     height=500,
#     width=None,
#     style="carto-positron",  # open-street-map
#     hover_data=None,
#     color_continuous_scale=None,
# ):
#     """pLotly mapbox for open-street-map & USGSImageryOnly"""

#     fig = px.scatter_mapbox(
#         df,
#         lat,
#         lon,
#         color=color_column,
#         size=size,
#         size_max=size_max,
#         hover_name=hover_name,
#         zoom=zoom,
#         height=height,
#         width=width,
#         hover_data=hover_data,
#         color_continuous_scale=color_continuous_scale,
#     )

#     if style == "USGSImageryOnly":
#         fig.update_layout(
#             mapbox_style="white-bg",
#             mapbox_layers=[
#                 {
#                     "below": "traces",
#                     "sourcetype": "raster",
#                     "source": [
#       "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"  # noqa=E501
#                     ],
#                 }
#             ],
#         )

#     else:
#         fig.update_layout(mapbox_style=style)

#     fig.update_layout(margin={"r": 0, "t": 10, "l": 0, "b": 0}, showlegend=False)
#     fig.show()
