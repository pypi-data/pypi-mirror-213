"""
- Title:            ML CONTRIBUTIONS. Smart Regressor for tabular data
- Project/Topic:    Smart Data Science. Practical functions for Data Science  (side project)
- Author/s:         Angel Martinez-Tenor
- Dev Date:         2018 -2023

- Status:           In progress.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import shap
from sklearn.pipeline import Pipeline

from smart_data_science.core import logger

# from smart_data_science.ml.plot_contributions import plot_contributions_summary

log = logger.get_logger(__name__)


def generate_shap_explainer(ml_pipeline: Pipeline = None, ml_model=None):
    """Generate the explainer for the model
    Args:
        ml_pipeline (sklearn.pipeline.Pipeline): ML pipeline with the model in the last step
        ml_model (sklearn.base.BaseEstimator): ML model (both ml_pipeline and ml_model cannot be set)
    Returns:
        shap.TreeExplainer: explainer for the model
    """

    if ml_model is None and ml_pipeline is None:
        raise ValueError("ml_model and ml_pipeline cannot be both None")
    if ml_model is not None and ml_pipeline is not None:
        raise ValueError("ml_model and ml_pipeline cannot be both set")

    if ml_model is None:
        ml_model = ml_pipeline[-1]

    explainer = shap.TreeExplainer(ml_model, feature_perturbation="tree_path_dependent")

    return explainer


def get_x_transformed(ml_pipeline: Pipeline, df: pd.DataFrame, sorted_features: list) -> tuple[np.ndarray, list]:
    """
    Args:
        df (pd.DataFrame): Data to predict
        sorted_features (list): list of features sorted as in the trained model
        ml_pipeline (sklearn.pipeline.Pipeline): ML pipeline with the model in the last step
    Returns:
        tuple[np.ndarray, list]: x_transformed, feature_names_transformed


    """

    features = sorted_features.copy()

    if ml_pipeline is not None:
        preprocessor = ml_pipeline[:-1]
        feature_names_transformed = list(preprocessor.get_feature_names_out())
        x_transformed = preprocessor.transform(df[features])

    else:
        feature_names_transformed = features
        x_transformed = df[features].copy()

    if not isinstance(x_transformed, (np.ndarray, pd.DataFrame)):
        log.warning(
            "x_transformed is not a numpy array or pandas dataframe. \
                    Converting to numpy array"
        )
        x_transformed = x_transformed.toarray()

        feature_names_transformed = list(preprocessor.get_feature_names_out())

    return x_transformed, feature_names_transformed


def get_shap_values(explainer: shap.Explainer, x_transformed: np.ndarray) -> np.ndarray:
    """Get the contributions of each feature to the prediction (SHAP)
    Args:
        explainer (shap.TreeExplainer): explainer for the model
        x_transformed (np.ndarray): data transformed
    Returns:
        pd.DataFrame: contributions to the prediction (SHAP)
    """

    shap_values = explainer.shap_values(x_transformed, check_additivity=False)
    return shap_values


def get_grouped_contributions_from_shap_values(
    shap_values: np.ndarray, feature_names_transformed: list, categorical_features: list, df: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Transform Shap Values to a dataframe with categorical contributions grouped"""

    # Generate dataframe with Combined categorical features
    df_contributions = pd.DataFrame(index=df.index, columns=feature_names_transformed, data=shap_values).round(3)
    for col in categorical_features:
        if df[col].dtype == "boolean":
            cat_col = [f"cat__{col}_{cat}" for cat in df[col].map({True: "1.0", False: "0.0"}).unique()]
        else:
            cat_col = [f"cat__{col}_{cat}" for cat in df[col].cat.categories]
        cat_col = [c for c in cat_col if c in df_contributions.columns]
        df_contributions[col] = df_contributions[cat_col].sum(axis=1)
        df_contributions = df_contributions.drop(columns=cat_col)
    # remove suffix num__ if exists:
    df_contributions.columns = [col.rsplit("num__", maxsplit=1)[-1] for col in df_contributions.columns]

    df_contributions = df_contributions.astype("float32").round(3)

    # check if column dtype is boolean
    df_contributions_summary = (
        df_contributions.apply(abs).mean().sort_values(ascending=False).astype("float32").round(3)
    )
    # )
    # if plot:
    #     plot_contributions_summary(df_contributions_summary)

    # def _add_top_contributions(df, X, shap_values, model_features):  # TO IMPROVE: Add to df_pred
    #     """Add top 3 influencing features to the dataframe
    #     Args:
    #         df (pd.DataFrame): dataframe to add the top 3 influencing features
    #         X (pd.DataFrame): dataframe or numpy array with the features
    #         shap_values (np.array): array of Shapley values
    #         model_features (list): list of the features
    #     Returns:
    #         df (pd.DataFrame): dataframe with the top 3 influencing features

    #     """

    #     df = df.copy()

    #     list_influencing = ["1st_influencing", "2nd_influencing", "3rd_influencing"]
    #     for col in list_influencing:
    #         df[col] = None

    #     for sample in range(X.shape[0]):
    #         sh = shap_values[sample].round(2)
    #         top = abs(sh).argsort()[-3:][::-1]

    #         for idx, col in enumerate(list_influencing):
    #             df.iloc[
    #                 sample, df.columns.get_loc(col)
    #             ] = f"{model_features[top[0]]}: {(X.iloc[sample, top[idx]])} ({sh[top[idx]]:+.2f})"

    #     return df

    return df_contributions, df_contributions_summary


# Old Dev - Classifier

# def generate_explainer(pipeline, X, pycaret_pipeline=False):
#     """Generate an explainer based on Shapley Values"""
#     # import churn_insights
#     # pipeline = load_pipeline()
#     # X_transformed = pipeline[:-1].transform(X)
#     # churn_insights.generate_and_save_explainer(final_pipeline, X)

#     print("\nGenerating Explainer with all samples (Shapley)")

#     transformed_features = None

#     x_transformed = pipeline[:-1].transform(X)

#     if pycaret_pipeline:
#         transformed_features = x_transformed.columns
#     else:
#         transformed_features = get_column_names_from_ColumnTransformer(pipeline["preprocessor"])

#     explainer = shap.TreeExplainer(
#         pipeline[-1],
#         data=x_transformed,
#         feature_names=transformed_features,
#         feature_perturbation="interventional",
#         model_output="probability",
#     )
#     return explainer


# def evaluate_explainer(pipeline, X_train, X_test, pycaret_pipeline=False):
#     """Fit Shapley-based explained on train set & evaluate on test set"""

#     print("\nGenerating and computing Explainer (Shapley)")

#     transformed_features = None

#     x_train_transformed = pipeline[:-1].transform(X_train)
#     x_test_transformed = pipeline[:-1].transform(X_test)

#     if pycaret_pipeline:
#         transformed_features = x_train_transformed.columns
#     else:
#         transformed_features = get_column_names_from_ColumnTransformer(pipeline["preprocessor"])

#     explainer = shap.TreeExplainer(pipeline[-1], data=x_train_transformed, feature_names=transformed_features)

#     shap_values = explainer(x_test_transformed)

#     plot_global(shap_values)

#     # shap.plots.waterfall(shap_values[15, :, 1])
#     # shap.plots.force(shap_values[15, :, 1])


# # def generate_and_save_explainer(model, data):
# #     explainer = generate_explainer(model, data)
# #     #shap_values = generate_shap_values(explainer, data)
# #     save_explainer(explainer)


# def save_explainer(explainer, filename=PATH_EXPLAINER, shap_values=False, pycaret_pipeline=False):
#     """Save the explainer"""
#     if pycaret_pipeline:  # force path
#         filename = PATH_EXPLAINER_PYCARET

#     joblib.dump(explainer, filename, compress=True)
#     print(f"Explainer Saved: \t{filename}")

#     # if GOOGLE_CLOUD:
#     #     google_cloud.save_to_bucket(filename)

#     # if shap_values:
#     #     joblib.dump(shap_values, filename='shap_values.joblib', compress=True)


# def load_explainer(filename=PATH_EXPLAINER, pycaret_pipeline=False):
#     """Load the explainer"""
#     if pycaret_pipeline:  # force path
#         filename = PATH_EXPLAINER_PYCARET

#     # if GOOGLE_CLOUD:
#     #     google_cloud.load_from_bucket(filename)

#     explainer = joblib.load(filename)
#     print(f"Explainer Loaded:\t{filename}")
#     return explainer


# def generate_shap_values(explainer, X=None):
#     """Auxiliary. Compute the Shapley values of the data X (dataset of features)"""
#     shap_values = explainer(X)
#     return shap_values

# def get_contributions(pipeline, explainer, X, sorted=True, pycaret_pipeline=False):
#     """Return contributions of all the samples in X"""
#     x_transformed = pipeline[:-1].transform(X)
#     shap_values_input = explainer(x_transformed)
#     vals = shap_values_input.values

#     # # values.ndim==3
#     # if vals.ndim == 2:  # rf / lightgbm differences
#     #     vals = vals[:, 1]

#     if pycaret_pipeline:
#         transformed_features = x_transformed.columns
#     else:
#         transformed_features = get_column_names_from_ColumnTransformer(pipeline["preprocessor"])

#     fe = pd.DataFrame(index=X.index, columns=transformed_features, data=vals).round(3)
#     return fe
