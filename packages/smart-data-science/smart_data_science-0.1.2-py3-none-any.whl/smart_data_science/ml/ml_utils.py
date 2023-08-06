"""
- Title:            ML UTILS. Smart Model for tabular data
- Project/Topic:    Smart Data Science. Practical functions for Data Science  (side project)
- Author/s:         Angel Martinez-Tenor
- Dev Date:         2018 -2023

- Status:           In progress.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from pickle import PicklingError

import joblib
import numpy as np
import pandas as pd
from IPython.display import display
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split

# from IPython.display import display
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from smart_data_science.core import logger

# from skopt import BayesSearchCV


log = logger.get_logger(__name__)


@dataclass
class ModelType:
    """
    Class to define the type of ML model (classifier or regressor)

    Example of usage:
       ml_type = ModelType(ModelType.REGRESSOR)
    """

    CLASSIFIER = "classifier"
    REGRESSOR = "regressor"

    def __init__(self, model_type):
        """
        Constructor of the class

        Args:
            model_type (str): type of ML model (classifier or regressor)
        """
        if model_type not in [ModelType.CLASSIFIER, ModelType.REGRESSOR]:
            raise ValueError("Invalid model type: choose either 'classifier' or 'regressor'")
        self.model_type = model_type

    def is_classifier(self):
        """
        Returns True if the model is a classifier
        """
        return self.model_type == ModelType.CLASSIFIER

    def is_regressor(self):
        """
        Returns True if the model is a regressor
        """
        return self.model_type == ModelType.REGRESSOR


def preprocess_input_data(
    df: pd.DataFrame,
    target: str,
    numerical_features: list = None,
    categorical_features: list = None,
    ml_type: ModelType = None,
) -> dict:
    """
    Process input data (df) and return a dictionary with the following keys:
    - df: pandas dataframe with the processed data
    - target: target column name
    - features: list of features (numerical and categorical)
    - numerical_features: list of numerical features
    - categorical_features: list of categorical features

    Args:
        df (pd.DataFrame): input dataframe
        target (str): target column name
        numerical_features (list, optional): list of numerical features. Defaults to None.
        categorical_features (list, optional): list of categorical features. Defaults to None.
        ml_type (ModelType, optional): type of ML model (classifier or regressor). Defaults to ModelType.REGRESSOR.

    Returns:
        dict: dictionary with the processed data (described above)
    """
    if ml_type is None:
        ml_type = ModelType(ModelType.REGRESSOR)

    # data = prepare_data(df, target, numerical_features, categorical_features)
    if isinstance(target, list):
        target = target[0]  # only first element is the target (no multi-targets for now)

    features = [col for col in df.columns if col != target]

    if numerical_features is None:
        numerical_features = list(df[features].select_dtypes(include=np.number))

    if categorical_features is None:
        categorical_features = [col for col in features if col not in numerical_features]

    numerical_features = [col for col in numerical_features if col not in categorical_features]
    # numerical_features = list(set(numerical_features) - set(categorical_features))
    features = numerical_features + categorical_features

    # Set dtypes
    df = df.copy()
    df[numerical_features] = df[numerical_features].astype("float32")
    df[categorical_features] = df[categorical_features].astype("category")
    if ml_type == "regression":
        df[target] = df[target].astype("float32")

    # Ensure target column exists
    if target not in df.columns:
        raise ValueError(f"Target column {target} not found in dataframe")

    features = numerical_features + categorical_features
    df = df[numerical_features + categorical_features + [target]]

    processed_dict = {
        "df": df,
        "target": target,
        "features": features,
        "numerical_features": numerical_features,
        "categorical_features": categorical_features,
    }

    return processed_dict


def build_pipeline(ml_model, numerical_features: list, categorical_features: list, preprocess: bool = True) -> Pipeline:
    """Return a production scikit-learn Pipeline (transformer + estimator)
    (usually already tuned and validated)

    Args:
        input_ml_model (sklearn-type estimator): input ML model to use in the pipeline
        numerical_features (list): list of numerical features
        categorical_features (list): list of categorical features
        preprocess (bool): whether to include the preprocessing steps in the pipeline
    """

    numerical_transformer = Pipeline(steps=[("imputer", SimpleImputer(strategy="median"))])

    categorical_transformer = Pipeline(
        steps=[
            ("encoder", OneHotEncoder(sparse_output=False, handle_unknown="ignore")),
            # ("scaler", OptimalScalingTransformer()), # Fisher's Optimal Scaling method
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numerical_transformer, numerical_features),
            ("cat", categorical_transformer, categorical_features),
        ],
        sparse_threshold=0,
    )

    pipeline = Pipeline(steps=[("preprocessor", preprocessor), ("ml_model", ml_model)])  # memory=cache_dir)

    if not preprocess:
        pipeline = Pipeline(steps=[("ml_model", ml_model)])  # memory=cache_dir) To Improve: add cache_dir

    info_model(pipeline)

    return pipeline


def split_data(
    df: pd.DataFrame,
    features: list,
    target: str,
    test_size: float = 0.2,
    chronological_split: bool = None,
    chronological_variable: str = "date",
    random_state: int = 0,
    stratify: pd.Series = None,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Split the data into train & test sets
    Args:
        df (pd.DataFrame): input dataframe
        features (list): list of features
        target (str): Target variable
        test_size (float): test size
        chronological_split (bool): whether to split chronologically
        chronological_variable (str): variable to use for chronological split
        random_state (int): random state
        stratify (pd.Series): stratify by a categorical variable
    Returns:
        tuple:  df_train, df_test, x_train, x_test, y_train, y_test
    Note: If chronological_split is True, and chronological_variable is None, the index will be used for
    chronological split.
    """

    df = df.copy()
    if chronological_split:
        if chronological_variable:
            df_sorted = df.sort_values(by=chronological_variable)
        else:
            df_sorted = df.sort_index()
        df_train, df_test = train_test_split(
            df_sorted,
            test_size=test_size,
            shuffle=False,
            random_state=random_state,
            stratify=stratify,
        )
        log.info("Chronological split applied")

    else:
        df_train, df_test = train_test_split(
            df, test_size=test_size, shuffle=True, random_state=random_state, stratify=stratify
        )

    x_train = df_train[features]
    y_train = df_train[target]
    x_test = df_test[features]
    y_test = df_test[target]

    df_train = pd.concat([x_train, y_train], axis=1)
    df_test = pd.concat([x_test, y_test], axis=1)

    return df_train, df_test, x_train, x_test, y_train, y_test


# def tune_pipeline(
#     pipeline: Pipeline,
#     x_train: pd.DataFrame,
#     y_train: pd.Series | pd.DataFrame,
#     param_grid: dict = None,
#     n_iter: int = 100,
#     verbose: int = 0,
#     cv: int = 3,
#     scoring: str = None,  # "r2"
#     # method: str = "Bayes",
# ) -> Pipeline:
#     """Perform a Bayesian Search and Return the best pipeline

#     Args:
#         pipeline (sklearn-type pipeline): input pipeline to tune
#         x_train (pd.DataFrame): input features
#         y_train (pd.Series | pd.DataFrame): input target
#         param_grid (dict): dictionary of parameters:values to tune. default values (If None):
#             {
#                 "ml_model__max_depth": [7, 9, 11, 13, 15, 17],
#                 "ml_model__n_estimators": [30, 50, 70, 100, 250, 400, 600],
#             }
#         n_iter (int): number of iterations for Bayesian search
#         verbose (int): verbosity of the search
#         cv (int): number of folds for cross-validation (minimum 2)
#         scoring (str): scoring metric

#     Returns:
#         The best estimator found during the search.
#     """
#     log.info(f"Training {n_iter} pipelines with {cv} Cross validations ({n_iter*cv} models) ...")

#     optimizer_search = BayesSearchCV(
#         pipeline, cv=cv, search_spaces=param_grid, n_jobs=-1, scoring=scoring, n_iter=n_iter, verbose=verbose
#     )

#     optimizer_search.fit(x_train, y_train.values.ravel())

#     best_pipeline = optimizer_search.best_estimator_

#     return best_pipeline


def info_ml_data(processed_dict: dict) -> None:
    """Print info about the data
    Args:
        processed_dict (dict): dictionary with the processed data
    """
    df = processed_dict["df"]
    target = processed_dict["target"]
    # features = processed_dict["features"]
    numerical_features = processed_dict["numerical_features"]
    categorical_features = processed_dict["categorical_features"]

    log.info(f"Total Samples: \t\t{df.shape[0]:,}")
    log.info(f"Target: \t\t\t{target}")
    log.info(f"{len(numerical_features)} Numerical Features: \t\t{numerical_features}")
    log.info(f"{len(categorical_features)} Categorical Features:\t{categorical_features}")


def load_pipeline(filepath: Path | str) -> Pipeline:
    """Load the pipeline & trained model
    Args:
        filepath (Path | str): path to the pipeline file
    Returns:
    """

    # if GOOGLE_CLOUD:
    #     google_cloud.load_from_bucket(filename)

    try:
        pipeline = joblib.load(filepath)
        log.info(f"Pipeline Loaded:\t{filepath}")
        return pipeline
    except FileNotFoundError as e:
        log.error(f"Failed to load pipeline: File not found: {e}")
        return None
    except EOFError as e:
        log.error(f"Failed to load pipeline: File is corrupted: {e}")
        return None


def save_pipeline(pipeline, filepath: Path | str) -> None:
    """Save the pipeline & trained model
    Args:
        pipeline (Pipeline): pipeline to save
        filepath (Path | str): path to the pipeline file
    """

    try:
        joblib.dump(pipeline, filepath, compress=True)
        log.info(f"\\ML Pipeline Saved:\t{filepath}")
    except FileNotFoundError as e:
        log.error(f"Failed to save pipeline: File not found: {e}")
    except PermissionError as e:
        log.error(f"Failed to save pipeline: Permission denied: {e}")
    except PicklingError as e:
        log.error(f"Failed to save pipeline: Pickling error: {e}")


def remove_null_params(ml_params: dict) -> dict:
    """Simplify the ML parameters to show them in a more readable way
    Args:
        ml_params (dict): ML Parameters
    Returns:
        dict: Simplified ML Parameters
    """
    ml_params = ml_params.copy()
    ml_params = {k: v for k, v in ml_params.items() if "__" not in k}
    ml_params = {k: v for k, v in ml_params.items() if v != 0}
    ml_params = {k: v for k, v in ml_params.items() if str(v).strip() not in ["None", "nan", ""]}

    return ml_params


def info_model(pipeline: Pipeline = None, ml_model=None):
    """Show info about the model and the pipeline
    Args:
        pipeline (Pipeline, optional): Pipeline. Defaults to None.
        ml_model ([type], optional): ML Model. Defaults to None.
    """
    if pipeline is None and ml_model is None:
        log.warning("No pipeline or model provided")
        return

    if pipeline is not None and ml_model is not None:
        log.warning("Both pipeline and model provided. Using pipeline")

    if pipeline is not None:
        ml_model = pipeline.steps[-1][1]
        display(pipeline)

    simplified_ml_params = remove_null_params(ml_model.get_params())
    log.info(f"ML Model: \t\t\t{ml_model.__class__.__name__}")
    log.info(f"ML Model Parameters: \t\t{simplified_ml_params}")


def get_ml_params(pipeline: Pipeline = None) -> dict:
    """Return the ML parameters of the pipeline
    Args:
        pipeline (Pipeline, optional): Pipeline. Defaults to None.
    Returns:
        dict: ML Parameters
    """
    if pipeline is None:
        log.warning("No pipeline provided")
        return None

    ml_model = pipeline.steps[-1][1]
    ml_params = ml_model.get_params()

    return ml_params


def format_scores(df_scores: pd.DataFrame, dict_metrics_type: dict) -> pd.DataFrame:
    """Format the scores dataframe
    Args:
        df_scores (pd.DataFrame): Scores dataframe
        dict_metrics_type (dict): Dictionary with the type of each metric ('max' or 'min')
    Returns:
        pd.DataFrame: Formatted scores dataframe
    """

    def _style_for_cell_value_in_table(value, value_range_and_color_list: list = None):
        """Style for the cell value in the table
        Args:
            value (float): Value of the cell
            value_range_and_color_list (list, optional): List with the value range and color for each value.
            Defaults to None.
        Returns:
            str: Style for the cell value in the table
        """

        if value_range_and_color_list is None:
            value_range_and_color_list = STYLE_NORMALIZED_MAX  # default

        color = next(
            (color for min_value, max_value, color in value_range_and_color_list if min_value <= value < max_value),
            "",
        )
        # return background-color: {color} and a format with only 3 decimals if the value is a float
        return f"background-color: {color}; "

    STYLE_NORMALIZED_MAX = [[-100.0, 0.4, "red"], [0.4, 0.6, "orange"], [0.6, 0.8, "yellow"], [0.8, 1.1, "green"]]
    STYLE_NORMALIZED_MIN = [[-100.0, 0.08, "green"], [0.08, 0.2, "yellow"], [0.2, 0.4, "orange"], [0.4, 1.1, "red"]]
    STYLE_SAMPLES = [[0, 20, "red"], [20, 50, "orange"], [50, 100, "yellow"], [100, 10000000, "green"]]

    df_formatted = df_scores.style.applymap(lambda x: "color: black").applymap(lambda x: "background-color: white")

    if "samples" in df_formatted.columns:
        df_formatted = df_formatted.applymap(
            lambda x: _style_for_cell_value_in_table(x, STYLE_SAMPLES), subset=["samples"]
        )

    for k, v in dict_metrics_type.items():
        if k in df_formatted.columns:
            if v == "min":
                df_formatted = df_formatted.applymap(
                    lambda x: _style_for_cell_value_in_table(x, STYLE_NORMALIZED_MIN), subset=[k]
                )
            elif v == "max":
                df_formatted = df_formatted.applymap(
                    lambda x: _style_for_cell_value_in_table(x, STYLE_NORMALIZED_MAX), subset=[k]
                )

    df_formatted = df_formatted.set_properties(**{"border": "1px solid grey !important"}, subset=pd.IndexSlice[:, :])

    for col in df_formatted.columns:
        if col in dict_metrics_type.keys():
            df_formatted = df_formatted.format("{:.3f}", subset=[col])
        elif col in dict_metrics_type.values():
            df_formatted = df_formatted.format("{:.3f}", subset=[col])

    return df_formatted


def get_scores_grouped(df: pd.DataFrame, col: str, target: str, dict_metrics: dict, dict_metrics_type) -> pd.DataFrame:
    """Get the scores for each category in a given column 'col'
    Args:
        df (pd.DataFrame): Dataframe with the scores
        col (str): Column to split the data to get the grouped scores
        dict_metrics (dict): Dictionary with the metrics to calculate
        dict_metrics_type (dict): Dictionary with the type of each metric ('max' or 'min')
    Returns:
        pd.DataFrame: sorted and formatted scores by categories of the given column
    """
    # if df is None:
    #     df = self.df_pred.copy()
    # if test_set_only:
    #     df = df[df["test_set"]].copy()

    assert df[col].dtype != np.number, "col must be a categorical variable"
    categories = list(df[col].unique())

    df_scores = pd.DataFrame()

    for cat in categories:
        df_sub = df[df[col] == cat].copy()
        y_test = df_sub[target].values
        y_pred = df_sub["predicted"].values
        # log.info(f"{df_sub.shape[0]} samples")
        # log.info(f"R2: {r2_score(y_test, y_pred):.3f}\n")

        df_scores.loc[cat, "samples"] = df_sub.shape[0]
        for k, v in dict_metrics.items():
            df_scores.loc[cat, k] = v(y_test, y_pred)

    df_scores["samples"] = df_scores["samples"].astype(int)

    for i in df_scores.columns:
        if i != "samples":
            df_scores[i] = df_scores[i].astype("float32").round(3)

    top_metric = list(dict_metrics.keys())[0]
    if dict_metrics_type[top_metric] == "min":
        df_scores = df_scores.sort_values(by=top_metric, ascending=True)
    else:
        df_scores = df_scores.sort_values(by=top_metric, ascending=False)

    df_scores_formatted = format_scores(df_scores, dict_metrics_type)

    return df_scores_formatted
