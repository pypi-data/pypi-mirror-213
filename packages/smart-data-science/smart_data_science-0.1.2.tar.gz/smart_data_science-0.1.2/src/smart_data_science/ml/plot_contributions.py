"""
- Title:            ML PLOT CONTRIBUTIONS. Utils for ML plots
- Project/Topic:    Smart Data Science. Practical functions for Data Science  (side project)
- Author/s:         Angel Martinez-Tenor
- Dev Date:         2023

- Status:           In progress.
"""


import pandas as pd
import plotly.express as px

from smart_data_science.core import logger

# import plotly.graph_objects as go


pd.options.plotting.backend = "plotly"


log = logger.get_logger(__name__)


def plot_contributions_summary(df: pd.DataFrame, title: str = "Feature contributions"):
    """
    Plot the contributions of the features to the prediction
    Args:
        df: dataframe with the contributions
        title: title of the plot

    """

    # vals = df.apply(abs).mean().sort_values(ascending=False)
    # feature_importance = pd.DataFrame(list(zip(X_train.columns,vals)),columns=['col_name','feature_importance_vals'])
    # feature_importance.sort_values(by=['feature_importance_vals'],ascending=False,inplace=True)

    # shap.summary_plot(self.fe.values, feature_names=self.fe.columns, plot_type="bar")

    # display vals with horizontal bars
    fig = px.bar(
        x=df.values,
        y=df.index,
        orientation="h",
        title=title,
        labels={"x": "Global Shap Contribution", "y": ""},
    )
    # invert yaxis to show most significant feature at the top and augment size of the labels
    fig.update_layout(yaxis={"autorange": "reversed"}, yaxis_tickfont_size=14)
    # leave some space on the left margin to show the whole labels
    fig.update_layout(margin={"l": 150})
    # the height of the bars depends on the number of features. with more space

    fig.update_layout(height=150 + 50 * len(df))

    return fig


# def shap_general_contributions(explainer, shap_values, X, dict_labels=None):
#     """plot general contributions"""
#     if dict_labels:  # classification model
#         shap.summary_plot(shap_values, X, class_names=list(dict_labels.values()))
#     else:  # regression model
#         shap.summary_plot(shap_values, X)


# def shap_label_contributions(explainer, shap_values, X, label, dict_labels=None):
#     """plot contributions for a given label of a  classifier"""
#     label_id = [key for (key, value) in dict_labels.items() if value == label][0]
#     shap.summary_plot(shap_values[label_id], X)


# def shap_interactive_contributions(explainer, shap_values, X, label=None, dict_labels=None):
#     """plot interactive contributions (in case of classifier: for a given label"""
#     if dict_labels:  # classification model
#         label_id = [key for (key, value) in dict_labels.items() if value == label][0]
#         plot = shap.force_plot(explainer.expected_value[label_id], shap_values[label_id], X)
#     else:
#         plot = shap.force_plot(explainer.expected_value, shap_values, X)
#     display(plot)


# def shap_dependence(shap_values, X, feat, label=None, dict_labels=None):
#     """plot shap dependence of a feature (the other one is automatically selected"""
#     if dict_labels:  # classification
#         label_id = [key for (key, value) in dict_labels.items() if value == label][0]
#         shap.dependence_plot(feat, shap_values[label_id], X)
#     else:
#         shap.dependence_plot(feat, shap_values, X)


# def shap_single(explainer, shap_values, X, sample, label=None, dict_labels=None):
#     """plot the shap values of a single prediction"""
#     if dict_labels:  # classification
#         label_id = [key for (key, value) in dict_labels.items() if value == label][0]

#         plot = shap.force_plot(explainer.expected_value[label_id], shap_values[label_id][sample, :], X.iloc[sample])

#     else:
#         plot = shap.force_plot(explainer.expected_value, shap_values[sample, :], X.iloc[sample])

#     display(plot)
#


# def plot_global(shap_values):
#     """Plot the global contribution of the Shapley Values"""
#     if shap_values.values.ndim == 3:  # differences between rf & lightgbm
#         shap_values = shap_values[:, :, 1]

#     try:  # unresolved shap issue
#         shap.waterfall_plot(shap_values)
#         shap.bar_plot(shap_values)
#     except Exception:  # as error:
#         print("waterfall_plot failed, using plots.waterfall instead")
#         shap.plots.beeswarm(shap_values)
#         shap.plots.bar(shap_values)


# def plot_individual(shap_values_sample):
#     """Plot the individual contribution of the Shapley Values"""
#     if len(shap_values_sample) == 1:
#         shap_values_sample = shap_values_sample[0]

#     try:  # unresolved shap issue
#         shap.waterfall_plot(shap_values_sample)
#     except Exception:
#         print("waterfall_plot failed, using plots.waterfall instead")
#         shap.plots.waterfall(shap_values_sample)
#         shap.plots.force(shap_values_sample)


# # The charts will be needed in the UI only
# def get_individual_contributions(pipeline, explainer, X, sorted=True, pycaret_pipeline=False):
#     """Return a dataset with the contributions of the first sample from a given X (dataset of features)"""
#     """ Improvement: Return contributions of all the samples in X  """

#     x_transformed = pipeline[:-1].transform(X)
#     shap_values_input = explainer(x_transformed)
#     vals = shap_values_input.values[0]

#     # values.ndim==3
#     if vals.ndim == 2:  # rf / lightgbm differences
#         vals = vals[:, 1]

#     if pycaret_pipeline:
#         transformed_features = x_transformed.columns
#     else:
#         transformed_features = get_column_names_from_ColumnTransformer(pipeline["preprocessor"])

#     # Add to the response (json) along with the prediction & the base response
#     fe = pd.DataFrame(list(zip(transformed_features, vals)), columns=["feature", "contribution"])
#     fe = fe.set_index("feature").round(3)

#     if sorted:
#         fe = fe.reindex(fe["contribution"].abs().sort_values(ascending=False).index)
#     return fe
