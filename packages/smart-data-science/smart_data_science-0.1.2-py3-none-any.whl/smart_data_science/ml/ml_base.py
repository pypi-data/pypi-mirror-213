"""
- Title:            Smart Model Base Class. Smart Regressor for tabular data
- Project/Topic:    Smart Data Science. Practical functions for Data Science  (side project)
- Author/s:         Angel Martinez-Tenor
- Dev Date:         2018 - 2023
"""

import pickle
import time
from abc import ABC, abstractmethod
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path

# import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import shap
from explainerdashboard import RegressionExplainer  # ExplainerDashboard
from IPython.display import display  # import display (for notebooks)
from sklearn.model_selection import cross_validate
from sklearn.pipeline import Pipeline

from smart_data_science.core import logger
from smart_data_science.core.scenario_base import ScenarioBase
from smart_data_science.ml import ml_contributions, ml_intervals, ml_tune, ml_utils  # ml_counterfactual
from smart_data_science.ml.plot_contributions import plot_contributions_summary  # plot_interval_predictions

# from .info_advanced import find_similar_samples

# from .transform import multi_to_single_index

# from mapie.metrics import regression_coverage_score
# from mapie.regression import MapieRegressor

log = logger.get_logger(__name__)


DEFAULT_PATH_OBJECT = "model/complete_regressor.pkl"
DEFAULT_PATH_ML_PIPELINE = "model/ml_pipeline.joblib"

# DEFAULT_ML_PARAMS = {"max_depth": 7, "n_estimators": 250, "n_jobs": -1}
# DEFAULT_ML_MODEL_REGRESSOR = LGBMRegressor(**DEFAULT_ML_PARAMS)
# DEFAULT_ML_MODEL_CLASSIFIER = LGBMClassifier(**DEFAULT_ML_PARAMS)


# DEFAULT_PARAM_GRID = {  # used for Bayesian optimization/tunning (BayesSearchCV)
#     "ml_model__colsample_bytree": [None],
#     "ml_model__max_depth": [7, 9, 11, 13, 15, 17],
#     "ml_model__n_estimators": [30, 50, 70, 100, 250, 400, 600],
#     "ml_model__learning_rate": [0.01, 0.05, 0.1, 0.2, 0.3, 0.5],
#     # "ml_model__num_leaves": [7, 15, 31, 63, 127, 255],
#     "ml_model__feature_fraction": [0.1, 0.3, 0.5, 0.7, 0.9, 1.0],
#     "ml_model__subsample": [0.1, 0.3, 0.5, 0.7, 0.9, 1.0],
#     # "ml_model__min_child_samples": [5, 10, 20, 30, 50, 100],
# }

# if GOOGLE_CLOUD:
#     from utils import google_cloud  # used for loading/saving the pipeline in GCS only


@dataclass(repr=False)
class SmartModel(ABC):  # pylint: disable=too-many-instance-attributes
    """Smart Extended ML for tabular data
    Args:
        df (pd.DataFrame): input dataset
        target (list(str) | str): target feature (if list, only the first element is the target)
        numerical_features (list(str)): numerical features
        categorical_features (list(str)): categorical features
        pipeline (sklearn Pipeline): Pipeline
        input_ml_model (sklearn-type estimator): ML model (the trained one will be saved in the pipeline)
        path_ml_pipeline (str): path to save/load the ML pipeline
        description (str): description of the Object / ML pipeline
        chronological_split (bool): if True, the split between train and test is done chronologically
        group_col (str): auxiliary column to plot the result grouped by this column
        target_units (str): units of the target variable
        dashboard_title (str): title of the dashboard
        model_folder (str): folder where the model is saved
        dict_metrics (dict): dictionary with the metrics to be used
        dict_metrics_type (dict): dictionary with the type of metrics (minimize or maximize)
        dict_metrics_scoring (dict): dictionary with the scoring to be used
        model_type (ModelType): type of model (classifier or regressor)  # leave blank to be inferred
    """

    df: pd.DataFrame = None
    target: str = None
    numerical_features: list[str] = None
    categorical_features: list[str] = None

    pipeline: Pipeline = None
    input_ml_model: object = None
    input_ml_params = None
    model_folder: str | Path = None  # folder where the model is saved

    path_ml_pipeline: str = DEFAULT_PATH_ML_PIPELINE
    description: str = None
    chronological_split: bool = False
    group_col: str = None  # auxiliary column to plot the result grouped by this column
    target_units: str = None  # units of the target variable
    dashboard_title: str = None  # title of the dashboard
    dict_metrics: dict = None
    dict_metrics_type: dict = None
    dict_metrics_scoring: dict = None
    model_type: ml_utils.ModelType = None
    default_ml_model = None
    scenario: ScenarioBase = None

    def __post_init__(self) -> None:  # noqa: R0915 # pylint: disable=too-many-statements
        """Post initialization"""

        self.features: list[str] = None

        if self.scenario is not None:
            log.info(f"Loading Parameters from Scenario {self.scenario.label}")
            self.df = self.scenario.df
            self.target = self.scenario.target
            self.features = self.scenario.features
            self.numerical_features = self.scenario.numerical_features
            self.categorical_features = self.scenario.categorical_features
            self.group_col = self.scenario.group_col

            self.input_ml_model = self.scenario.input_ml_model
            self.input_ml_params = self.scenario.input_ml_params
            self.model_folder = self.scenario.model_folder
            self.chronological_split = self.scenario.chronological_split

            self.dashboard_title = self.scenario.label  # TODO remove dashboard_title
            self.target_units = self.scenario.target_units

        else:
            processed_dict = ml_utils.preprocess_input_data(
                self.df, self.target, self.numerical_features, self.categorical_features, self.model_type
            )

            ml_utils.info_ml_data(processed_dict)

            self.df = processed_dict["df"]
            self.target = processed_dict["target"]
            self.features = processed_dict["features"]
            self.numerical_features = processed_dict["numerical_features"]
            self.categorical_features = processed_dict["categorical_features"]

        self.x = self.df[self.features].copy()
        self.y = self.df[self.target].copy()

        # Initialize empty variables

        self.scores: dict = {}
        self.df_train: pd.DataFrame = None
        self.df_test: pd.DataFrame = None
        self.df_pred: pd.DataFrame = None
        self.x_train: pd.DataFrame = None
        self.y_train: pd.DataFrame = None
        self.x_test: pd.DataFrame = None
        self.y_test: pd.DataFrame = None
        self.explainer: shap.Explainer = None
        self.shap_values: np.ndarray = None
        self.df_pred_test: pd.DataFrame = None
        # self.dashboard : ExplainerDashboard = None
        self.x_transformed: np.ndarray = None
        self.x_test_transformed: np.ndarray = None
        self.feature_names_transformed: list[str] = None
        self.reg_explainer: RegressionExplainer = None
        self.last_results: dict = None
        self.dashboard_title: str = None
        self.df_predictions: pd.DataFrame = None
        self.df_contributions: pd.DataFrame = None
        self.df_last_predictions: pd.DataFrame = None
        self.df_last_contributions: pd.DataFrame = None
        self.test_size: float = None
        self.random_state: int = None
        self.default_param_grid: dict = None
        self.df_contributions_summary: pd.DataFrame = None
        self.pipeline_lower: Pipeline = None
        self.pipeline_upper: Pipeline = None

        self.build_pipeline(input_ml_model=self.input_ml_model)

    def build_pipeline(self, input_ml_model=None, preprocess: bool = True) -> Pipeline:
        """Return a production scikit-learn Pipeline (transformer + estimator)
        (usually already tuned and validated)

        Args:
            input_ml_model (sklearn-type estimator): input ML model to use in the pipeline
            preprocess (bool): whether to include the preprocessing steps in the pipeline
        """

        if input_ml_model is None:
            ml_model = self.default_ml_model
        else:
            ml_model = deepcopy(input_ml_model)

        self.pipeline = ml_utils.build_pipeline(
            ml_model,
            self.numerical_features,
            self.categorical_features,
            preprocess,
        )
        ml_utils.get_ml_params(self.pipeline)
        return self.pipeline

    def tune_pipeline(
        self,
        param_grid: dict = None,
        n_iter: int = 100,
        scoring: str = "r2",
        verbose: int = 0,
        cv: int = 3,
        update_pipeline: bool = True,
    ) -> Pipeline:
        """Perform a Bayesian Search and Return the best pipeline

        Args:
            param_grid (dict): dictionary of parameters:values to tune. default values (If None):
                {
                    "ml_model__max_depth": [7, 9, 11, 13, 15, 17],
                    "ml_model__n_estimators": [30, 50, 70, 100, 250, 400, 600],
                }
            n_iter (int): number of iterations for Bayesian search
            scoring (str): scoring metric
            verbose (int): verbosity of the search
            cv (int): number of folds for cross-validation (minimum 2)
            update_pipeline (bool): whether to update the pipeline with the best estimator

        Returns:
            The best estimator found during the search.
        """
        if param_grid is None:
            param_grid = self.default_param_grid
            display(param_grid)

        best_pipeline = ml_tune.tune_pipeline(self.pipeline, self.x, self.y, param_grid, n_iter, verbose, cv, scoring)

        if update_pipeline:
            self.pipeline = best_pipeline  # deepcopy(best_pipeline)
            self.fit()

        return best_pipeline

    def split_data(
        self,
        test_size: float = 0.2,
        chronological_split: bool = None,
        chronological_variable: str = "date",
        random_state: int = 0,
    ) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Split the data into train & test sets
        Args:
            test_size (float, optional): Test size.
            chronological_split (bool, optional): Split the data chronologically.
            chronological_variable (str, optional): Variable to split the data chronologically.
            random_state (int, optional): Random state for the split.
        Returns:
            x_train, x_test, y_train, y_test: Train & Test sets

        Note: If chronological_split is True, and chronological_variable is None, the index will be used for
        chronological split.
        """

        stratify = None
        if self.model_type.is_classifier():
            stratify = self.df[self.target]

        if chronological_split is None:
            chronological_split = self.chronological_split

        df_train, df_test, x_train, x_test, y_train, y_test = ml_utils.split_data(
            self.df,
            self.features,
            self.target,
            test_size,
            chronological_split,
            chronological_variable,
            random_state,
            stratify,
        )

        self.df_train = df_train
        self.df_test = df_test
        self.x_train = x_train
        self.x_test = x_test
        self.y_train = y_train
        self.y_test = y_test
        self.test_size = test_size
        self.random_state = random_state

        return x_train, x_test, y_train, y_test

    def fit(self, cv: int = 10) -> None:  # TO IMPROVE: Move to ML utils?
        """Train & evaluate a ML pipeline
        Args:
            cv (int, optional): Number of folds for cross validation.
        """

        start_time = time.time()

        if self.x_train is None:
            x_train, x_test, y_train, y_test = self.split_data(chronological_split=self.chronological_split)
        else:
            x_train, x_test, y_train, y_test = self.x_train, self.x_test, self.y_train, self.y_test

        log.info(f"Training with {x_train.shape[0]} samples ...")
        # metrics available: sklearn.metrics.SCORERS.keys()
        cv_scores = cross_validate(
            self.pipeline,
            x_train,
            y_train.values.ravel(),
            cv=cv,
            scoring=self.dict_metrics_scoring,
            n_jobs=-1,
            error_score="raise",
        )

        for i in self.dict_metrics.keys():
            if self.dict_metrics_type[i] == "max":
                self.scores[f"CV {i} (mean)"] = cv_scores[f"test_{i}"].mean().round(3)
                self.scores[f"CV {i} (std)"] = cv_scores[f"test_{i}"].std().round(3)
            else:
                self.scores[f"CV {i} (mean)"] = abs(cv_scores[f"test_{i}"].mean()).round(3)
                self.scores[f"CV {i} (std)"] = abs(cv_scores[f"test_{i}"].std()).round(3)

            log.info(f"CV {i}: {self.scores[f'CV {i} (mean)']} (std: {self.scores[f'CV {i} (std)']})")

        # Fit/Train the pipeline with the training set
        self.pipeline.fit(x_train, y_train.values.ravel())

        # Evaluate using the test Set (Once Only)
        log.info(f"Evaluating Test with {x_test.shape[0]} samples ...")
        self.evaluate(x_test, y_test)

        df_pred = self.predict(x_test)
        self.df_pred = df_pred.join(y_test)

        end_time = time.time()
        log.info(f"Total Training (CV) and evaluation time: {end_time - start_time:.0f} seconds")

        log.info(self.get_summary())
        display(self.display_scores())
        if self.group_col:
            display(self.get_scores_grouped(self.df_pred, self.group_col))

        # TO IMPROVE: Retrain removing features with very low global contribution (via LLM with feature engineering or
        #  Rule based)

    def evaluate(self, x_test: pd.DataFrame, y_test: pd.DataFrame | pd.Series):
        """Show the R2 score and MAD
        Args:
            x_test (pd.DataFrame): Test features
            y_test (pd.DataFrame | pd.Series): Test target
        """

        y_pred = self.pipeline.predict(x_test)

        for k, v in self.dict_metrics.items():
            if self.dict_metrics_type[k] == "max":
                self.scores[f"Test {k}"] = v(y_test, y_pred).round(3)
            else:
                self.scores[f"Test {k}"] = abs(v(y_test, y_pred)).round(3)

            log.info(f"Test {k}: {self.scores[f'Test {k}']}")

    def display_scores(self, dict_scores: dict = None) -> pd.DataFrame:
        """Return a colored dataframe with scores"""

        # Use default dictionary if None is provided
        if dict_scores is None:
            dict_scores = self.scores.copy()

        df_results = pd.DataFrame(index=["CV", "Test"])
        df_results["samples"] = [self.x_train.shape[0], self.x_test.shape[0]]

        # split dict scores into 2 dictionaries: starting with CV and Test. the prefixes CV and Test will be removed.
        # the scores containing (std) will be removed
        cv_scores = {
            k.split("CV ")[-1].split(" (mean)")[0]: v
            for k, v in dict_scores.items()
            if k.startswith("CV") and "(std)" not in k
        }
        test_scores = {k.split("Test ")[-1]: v for k, v in dict_scores.items() if k.startswith("Test")}

        # cv scores will be at the row with index CV
        for k, v in cv_scores.items():
            df_results.loc["CV", k] = v

        # test scores will be at the row with index Test
        for k, v in test_scores.items():
            df_results.loc["Test", k] = v

        return self.format_scores(df_results)

    def save_object(self, save_path: Path | str = None) -> None:
        """Save the whole object
        Args:
            save_path (str, optional): Path to save the pipeline.
        """

        if save_path is None:
            save_path = DEFAULT_PATH_OBJECT
        save_path = Path(save_path)
        log.info(f"Saving the whole trained object to {save_path}")
        save_path.parent.mkdir(parents=True, exist_ok=True)
        with open(save_path, "wb") as f:
            pickle.dump(self, f)
        log.info("FINISHED")

    def plot_contributions_summary(self, df: pd.DataFrame = None, title: str = "Feature contributions"):
        """
        Plot the contributions of the features to the prediction
        """
        if df is None:
            df = self.df_contributions_summary.copy()

        fig = plot_contributions_summary(df, title=title)

        return fig

    def get_summary(self) -> dict:  # TODO: improve this
        """Return a summary dict of the model"""

        summary_dict = {}
        if self.scenario is not None:
            summary_dict = self.scenario.summary_dict

        summary_dict.update(
            {
                "target": self.target,
                "numerical_features": self.numerical_features,
                "categorical_features": self.categorical_features,
                "model": self.pipeline["ml_model"].__class__.__name__,
                "ml_params": ml_utils.remove_null_params(ml_utils.get_ml_params(self.pipeline)),
                "training_samples": self.df_train.shape[0],
                "test_samples": self.df_test.shape[0],
                "test_size": self.test_size,
                "random_state": self.random_state,
                "results": self.scores,
            }
        )
        if self.df_contributions_summary is not None:
            dict_contributions = self.df_contributions_summary.to_dict()
            # force all the values to 3 decimals
            dict_contributions = {k: round(v, 3) for k, v in dict_contributions.items()}

            summary_dict.update({"global_contributions_to_predictions": dict_contributions})

        summary_dict = {
            k: v for k, v in summary_dict.items() if v is not None and v is not False  # and k != "description"
        }

        # summary_str = "SUMMARY:\n\n"
        # for key, value in summary_dict.items():
        #     if isinstance(value, list):
        #         value = ", ".join(value)
        #     elif isinstance(value, dict):
        #         plain_str = ""
        #         for k, v in value.items():
        #             # if isinstance(v, str):
        #             plain_str += f"\n- {k:<22} {v}"
        #             # else:
        #             #     plain_str += f"{k}: {v}, "
        #         value = plain_str
        #     key = f"{key}:"
        #     summary_str += f"{key:<22} {value}\n"
        return summary_dict  # summary_str

    def generate_shap_explainer(self):
        """Generate the SHAP explainer"""
        assert self.pipeline is not None, "Pipeline is not fitted yet. Please fit the pipeline first"
        self.explainer = ml_contributions.generate_shap_explainer(self.pipeline)

    def get_contributions(self, df: pd.DataFrame = None, save=False) -> pd.DataFrame:
        """Get the contributions of each feature to the prediction (SHAP)
        Args:
            df (pd.DataFrame): Data to predict
            save_explainer (bool, optional): Save the explainer and contributions to the object. Defaults to False.

        Returns:
            pd.DataFrame: contributions to the prediction (SHAP)

        To plot: fig = self.plot_contributions_summary(self.df_contributions_summary)

        """
        # shap.initjs()
        if self.explainer is None:
            self.generate_shap_explainer()

        if df is None:
            df = self.df_pred.copy()
            # save_explainer_and_contributions = True

        x_transformed, feature_names_transformed = ml_contributions.get_x_transformed(self.pipeline, df, self.features)

        shap_values = ml_contributions.get_shap_values(self.explainer, x_transformed)

        df_contributions, df_contributions_summary = ml_contributions.get_grouped_contributions_from_shap_values(
            shap_values, feature_names_transformed, self.categorical_features, df
        )
        # explainer = shap.TreeExplainer(ml_model, feature_perturbation="tree_path_dependent")

        # df_contributions_summary = (
        #     df_contributions.apply(abs).mean().sort_values(ascending=False).astype("float32").round(3)
        # )

        if save:
            self.df_contributions = df_contributions
            self.x_transformed = x_transformed
            self.feature_names_transformed = feature_names_transformed
            self.df_contributions_summary = df_contributions_summary
            self.shap_values = shap_values

        return df_contributions

    def fit_intervals(self, confidence: float = None):
        """Generate prediction intervals model
        Args:
            confidence (float, optional): Confidence interval.
        """

        self.pipeline_lower, self.pipeline_upper = ml_intervals.fit_intervals(
            self.pipeline,
            x=self.x,
            y=self.y,
            confidence=confidence,
        )

    def predict_intervals(self, x: pd.DataFrame) -> pd.DataFrame:
        """Predict intervals
        Args:
            x (pd.DataFrame): Input data.
        Returns:
            pd.DataFrame: Prediction intervals.
        """

        df = ml_intervals.predict_intervals(self.pipeline_lower, self.pipeline_upper, x)
        return df

    def get_scores_grouped(self, df: pd.DataFrame, col: str) -> pd.DataFrame:
        """Get the scores disaggregated for each value in the given categorical column
        Args:
            col (str): Column to split the data to get the R2 scores
            test_set_only (bool, optional): Only use test set. Defaults to True.
        Returns:
            pd.DataFrame: sorted R2 score for each category
        """

        # assert self.pipeline is not None, "The pipeline must be fitted first"
        try:
            assert col in df.columns
        except AssertionError:
            log.warning("The pipeline must be fitted first")

        return ml_utils.get_scores_grouped(df, col, self.target, self.dict_metrics, self.dict_metrics_type)

    def format_scores(self, df_scores: pd.DataFrame) -> pd.DataFrame:
        """Format the scores dataframe
        Args:
            df_scores (pd.DataFrame): Scores dataframe
        Returns:
            pd.DataFrame: Formatted scores dataframe
        """

        return ml_utils.format_scores(df_scores, self.dict_metrics_type)

    @abstractmethod
    def predict(self, df: pd.DataFrame | pd.Series) -> pd.DataFrame:
        """Predict data from a ML pipeline
        Args:
            df (pd.DataFrame): Data to predict
        Returns:
            pd.DataFrame: input data + 'predicted' column
        """

    @abstractmethod
    def predict_complete(self, x: pd.DataFrame | pd.Series | dict, contributions=True, intervals=True) -> pd.DataFrame:
        """
        Return the prediction of the model for a given input (individual or batch). Return also the prediction
        intervals and the contributions of each feature.
        Args:
            x (pd.DataFrame | pd.Series | dict): Input data
            contributions (bool, optional): Return the contributions of each feature. Defaults to True.

        """

    @abstractmethod
    def plot_predictions_vs_target(self, df: pd.DataFrame = None):
        """
        Plot the Predicted vs True Target
        Args:
            df: dataframe with predictions. If None, the current self.df_pred is used
        """

    # @abstractmethod
    # def fit_intervals(self, confidence: float = CONFIDENCE_INTERVAL):
    #     """Generate prediction intervals model
    #     Args:
    #         alpha (float, optional): Confidence interval.
    #     """

    # @abstractmethod
    # def predict_intervals(self, x: pd.DataFrame) -> pd.DataFrame:
    #     """Predict intervals
    #     Args:
    #         x (pd.DataFrame): Input data.
    #     Returns:
    #         pd.DataFrame: Prediction intervals.
    #     """

    @abstractmethod
    def finalize(self, save: bool = True, save_path: str = None, units=None, title=None) -> None:
        """Train the current pipeline with all the data and save the whole object
        Args:
            save (bool, optional): Save the pipeline.
            save_path (str, optional): Path to save the pipeline.
            units (str, optional): Units of the target variable.
            title (str, optional): Title of the dashboard.
        """
