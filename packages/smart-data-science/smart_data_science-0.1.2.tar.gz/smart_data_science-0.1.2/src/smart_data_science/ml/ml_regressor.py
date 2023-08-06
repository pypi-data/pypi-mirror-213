"""
- Title:            TEMPLATE ML PIPELINE. Smart Regressor for tabular data
- Project/Topic:    Smart Data Science. Practical functions for Data Science  (side project)
- Author/s:         Angel Martinez-Tenor
- Dev Date:         2020 - 2023

- Status:           In progress.

Description (from ChatGPT):

This is a Python class definition for a smart regressor that is capable of building a production-ready scikit-learn
pipeline for regression tasks. The pipeline includes transformers for handling missing values and categorical variables,
and an estimator that is an XGBoost regressor by default, but can be replaced with another scikit-learn compatible
estimator. The class provides several methods for data preparation, model training, and prediction, as well as for
producing explanations and insights about the model's behavior.

The class is defined using the dataclass decorator, which allows you to define a class with default values for its
attributes and automatically generate an __init__() method and other methods based on them. The attributes of the class
include the input dataset, target feature, numerical and categorical features, the scikit-learn pipeline, the
scikit-learn estimator, the path to save the pipeline, and various other parameters related to the pipeline, such as its
 name, version, author, date, status, and notes.

The __post_init__() method is a special method that is called automatically after the class instance is initialized.
It sets some default values for the numerical and categorical features if they are not provided, converts them to the
appropriate data types, and initializes some other attributes to None.

The build_pipeline() method is the main method of the class that builds the scikit-learn pipeline. It uses scikit-learn
transformers to preprocess the data, including handling missing values and categorical variables, and an XGBoost
regressor as the default estimator. The parameters of the estimator can be provided as a dictionary to the method or set
 as the default values inside the method. The method returns the final pipeline.

Other methods provided by the class include prepare_data(), which splits the input dataset into training and testing
datasets, train_model(), which trains the pipeline on the training dataset, predict(), which makes predictions on new
data using the trained pipeline, get_explanation(), which generates SHAP values to explain the model's predictions,
get_insights(), which produces various insights about the model's behavior, such as feature importances, partial
dependence plots, and permutation importance, and save_pipeline(), which saves the pipeline to a file.
"""

# import pickle
from dataclasses import dataclass

import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
from explainerdashboard import ExplainerDashboard, RegressionExplainer
from lightgbm import LGBMRegressor
from sklearn.metrics import mean_absolute_percentage_error, r2_score
from sklearn.pipeline import Pipeline

from smart_data_science.analysis.info_advanced import find_similar_samples
from smart_data_science.core import logger
from smart_data_science.ml.ml_base import SmartModel
from smart_data_science.ml.ml_utils import ModelType
from smart_data_science.ml.plot_intervals import plot_interval_predictions
from smart_data_science.ml.plot_regressor import plot_predictions_vs_target
from smart_data_science.process.transform import multi_to_single_index

# from pathlib import Path


# from mapie.metrics import regression_coverage_score
# from mapie.regression import MapieRegressor


log = logger.get_logger(__name__)

MODEL_TYPE = ModelType(ModelType.REGRESSOR)

DEFAULT_PATH_OBJECT = "model/smart_regressor.pkl"
CONFIDENCE_INTERVAL = 0.95  # used for Interval Prediction. 95% by default (alpha = 0.05)

DEFAULT_ML_PARAMS = {"max_depth": 7, "n_estimators": 150, "n_jobs": -1}  # down from 250 to 150 (faster demos)
DEFAULT_ML_MODEL = LGBMRegressor(**DEFAULT_ML_PARAMS)

DEFAULT_PARAM_GRID = {  # used for Bayesian optimization/tunning (BayesSearchCV)
    "ml_model__colsample_bytree": [None],
    "ml_model__max_depth": [7, 9, 11, 13, 15, 17],
    "ml_model__n_estimators": [30, 50, 70, 100, 250, 400, 600],
    "ml_model__learning_rate": [0.01, 0.05, 0.1, 0.2, 0.3, 0.5],
    # "ml_model__num_leaves": [7, 15, 31, 63, 127, 255],
    "ml_model__feature_fraction": [0.1, 0.3, 0.5, 0.7, 0.9, 1.0],
    "ml_model__subsample": [0.1, 0.3, 0.5, 0.7, 0.9, 1.0],
    # "ml_model__min_child_samples": [5, 10, 20, 30, 50, 100],
}

DEFAULT_METRICS = {"R2": r2_score, "MAPE": mean_absolute_percentage_error}
DEFAULT_METRICS_TYPE = {"R2": "max", "MAPE": "min"}  # type of metric (to be maximized or minimized)
DEFAULT_METRICS_SCORING = {"R2": "r2", "MAPE": "neg_mean_absolute_percentage_error"}


@dataclass(repr=False)
class SmartRegressor(SmartModel):  # pylint: disable=too-many-instance-attributes
    """Smart Regressor for tabular data
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
    """

    default_ml_model: LGBMRegressor = DEFAULT_ML_MODEL
    # default_param_grid: dict = DEFAULT_PARAM_GRID

    def __post_init__(self) -> None:
        """Post init method"""
        self.model_type = MODEL_TYPE

        super().__post_init__()

        self.default_param_grid = DEFAULT_PARAM_GRID
        # self.default_ml_model = DEFAULT_ML_MODEL

        if self.dict_metrics is None:
            self.dict_metrics = DEFAULT_METRICS
        if self.dict_metrics_type is None:
            self.dict_metrics_type = DEFAULT_METRICS_TYPE
        if self.dict_metrics_scoring is None:
            self.dict_metrics_scoring = DEFAULT_METRICS_SCORING

        self.pipeline_lower: Pipeline = None
        self.pipeline_upper: Pipeline = None

    def predict(self, df: pd.DataFrame | pd.Series) -> pd.DataFrame:
        """Predict data from a ML pipeline - Regression (scikit-learn)
        Args:
            df (pd.DataFrame): Data to predict
        Returns:
            pd.DataFrame: input data + 'predicted' column
        """
        if isinstance(df, pd.Series):
            df = df.to_frame().T
        df_pred = df[self.features].copy()
        df_pred["predicted"] = self.pipeline.predict(df_pred).astype(float).round(2)
        return df_pred

    def predict_complete(
        self, x: pd.DataFrame | pd.Series | dict, contributions=True, intervals=True, logs=False, save=False
    ) -> tuple[pd.DataFrame, pd.DataFrame]:
        """
        Return the prediction of the model for a given input (individual or batch). Return also the prediction
        intervals and the contributions of each feature.
        Args:
            x (pd.DataFrame | pd.Series | dict): Input data
            contributions (bool, optional): Return the contributions of each feature. Defaults to True.
            intervals (bool, optional): Return the prediction intervals. Defaults to True.
            logs (bool, optional): Show logs. Defaults to False.
            save (bool, optional): Save the prediction. Defaults to False.
        Returns:
            tuple(pd.DataFrame, pd.DataFrame): Predictions and contributions.

        """
        # if input data is dict, convert to dataframe
        if isinstance(x, dict):
            x = pd.DataFrame(x, index=[0])
        # if input data is series, convert to dataframe
        elif isinstance(x, pd.Series):
            x = x.to_frame().T

        # check if the input data has the same columns as the training data. In that case show a message with the
        # missing columns and return None

        missing_cols = [col for col in self.features if col not in x.columns]
        if len(missing_cols) > 0:
            log.warning(f"No Prediction. Missing columns: {missing_cols}")
            return None

        # Generate predictions
        df_pred = x[self.features].copy()

        if logs:
            log.info("Predicting ...")
        df_pred["predicted"] = self.pipeline.predict(df_pred).astype("float32").round(2)

        # Generate prediction intervals
        if logs:
            log.info("Predicting intervals ...")
        if intervals:
            df_pred_intervals = self.predict_intervals(x)
            df_pred = df_pred.join(df_pred_intervals)

            # Correct Interval if the lower bound is higher than the prediction and / or the upper bound is lower than
            # the prediction and recalculate the difference between the upper and lower bound
            df_pred["predicted_lower"] = np.where(
                df_pred["predicted_lower"] > df_pred["predicted"], df_pred["predicted"], df_pred["predicted_lower"]
            )
            df_pred["predicted_upper"] = np.where(
                df_pred["predicted_upper"] < df_pred["predicted"], df_pred["predicted"], df_pred["predicted_upper"]
            )
            df_pred["predicted_interval_diff"] = df_pred["predicted_upper"] - df_pred["predicted_lower"]

            df_pred["predicted_interval_%"] = 100 * df_pred["predicted_interval_diff"] / df_pred["predicted"]

        # Generate contributions
        if contributions:
            if logs:
                log.info("Getting contributions ...")
            df_contributions = self.get_contributions(x, save=save)
        else:
            df_contributions = None

        self.df_last_predictions = df_pred.copy()
        self.df_last_contributions = df_contributions.copy()

        # numeric_cols = [col for col in df_pred.columns if df_pred[col].dtype not in ["object", "category"]]
        df_pred = df_pred.applymap(lambda x: round(x, 2) if isinstance(x, (int, float)) else x)
        df_contributions = df_contributions.applymap(lambda x: round(x, 2) if isinstance(x, (int, float)) else x)

        return df_pred, df_contributions

    def finalize(
        self, save: bool = True, save_path: str = None, units=None, title=None, generate_explainer_dashboard=True
    ) -> None:
        """Train the current pipeline with all the data and save the whole object
        Args:
            save (bool, optional): Save the pipeline.
            save_path (str, optional): Path to save the pipeline.
            units (str, optional): Units of the target variable.
            title (str, optional): Title of the dashboard.
        """

        x = self.x.copy()
        y = self.y.copy()

        log.info("Training with all data ...")
        self.pipeline.fit(x, y.values.ravel())

        self.generate_shap_explainer()

        log.info("Generate prediction intervals model ...")
        self.fit_intervals()

        log.info("Predict complete with all the reference data ...")
        df_pred, df_contributions = self.predict_complete(x, logs=True, save=True)

        df_pred = df_pred.join(y)  # add target
        df_pred["deviation %"] = 100 * (df_pred["predicted"] - df_pred[self.target]) / df_pred[self.target]
        df_pred["deviation %"] = df_pred["deviation %"].astype(float).round(2)

        log.info("Generate Regression explainer for Dashboard ...")

        if generate_explainer_dashboard:
            self.generate_regression_explainer_for_dashboard(units=units, title=title)

        # log.info("Predict intervals with all data ...")
        # df_pred_intervals = self.predict_intervals(x)
        # df_pred = df_pred.join(df_pred_intervals)
        # df_pred["predicted_interval_%"] = 100 * df_pred["predicted_interval_diff"] / df_pred["predicted"]
        # log.info("Get all contributions ...")
        # df_contributions = self.get_contributions(x, plot=False, save=True)

        self.df_pred = df_pred
        self.df_contributions = df_contributions

        if save:
            self.save_object(save_path)

    def generate_regression_explainer_for_dashboard(
        self, units: str = None, mode="dash", save_dashboard=True, title="Explainer Dashboard"
    ):
        """Generate the explainer dashboard (test set only)"""
        self.dashboard_title = title

        assert self.pipeline is not None, "Pipeline is not fitted yet. Please fit the pipeline first"

        if "preprocessor" in self.pipeline.named_steps:
            preprocessor = self.pipeline["preprocessor"]
            feature_names_transformed = list(preprocessor.get_feature_names_out())
            x_test_transformed = preprocessor.transform(self.x_test)

        else:  # no preprocessor: e.g. fast lightgbm xgboost with Fisher's Optimal Scaling for categorical features
            x_test_transformed = self.x_test
            feature_names_transformed = self.x_test.columns

        ml_model = self.pipeline["ml_model"]

        if not isinstance(x_test_transformed, (np.ndarray, pd.DataFrame)):
            log.warning(
                "Transformed data is not a numpy array. A sparse matrix converted into dense array will give you  \
            incorrect predictions if the model was trained with sparse data using explainer dashboard "
            )
            x_test_transformed = x_test_transformed.toarray()

        if "preprocessor" in self.pipeline.named_steps:
            feature_names = [f.split("__")[1] for f in feature_names_transformed]
        else:
            feature_names = feature_names_transformed

        x_test_index = self.x_test.index

        if x_test_index.nlevels > 1:
            x_test_index = multi_to_single_index(x_test_index)

        df_x_test_transformer = pd.DataFrame(
            columns=feature_names_transformed, data=x_test_transformed, index=x_test_index
        )
        df_x_test_transformer.columns = feature_names

        if "preprocessor" in self.pipeline.named_steps:
            reg_explainer = RegressionExplainer(
                ml_model, df_x_test_transformer, self.y_test, units=units, cats=self.categorical_features
            )
        else:
            log.debug(df_x_test_transformer.columns)
            log.debug(df_x_test_transformer.shape)
            log.debug(self.y_test.shape)

            reg_explainer = RegressionExplainer(ml_model, df_x_test_transformer, self.y_test, units=units)

        if save_dashboard:
            self.explainer_dashboard(reg_explainer, save=True, mode=mode, title=title)

        self.x_test_transformed = x_test_transformed
        self.reg_explainer = reg_explainer

    def explainer_dashboard(self, reg_explainer=None, save=False, mode="dash", title=None):
        """
        Generate the explainer dashboard from a regression explainer
        """

        if reg_explainer is None:
            reg_explainer = self.reg_explainer

        if reg_explainer is None:
            raise ValueError("There is no regression explainer. Please generate one first.")

        if title is None:
            title = self.dashboard_title
        if title is None:
            title = "Explainer Dashboard"
        self.dashboard_title = title

        dashboard = ExplainerDashboard(
            reg_explainer,
            title=title,  # defaults to "Model Explainer"
            shap_interaction=False,  # you can switch off tabs with booleans
            check_additivity=False,
            hide_header=True,
            header_hide_title=True,
            decision_trees=False,
            mode=mode,
            show_metrics=list(DEFAULT_METRICS.values()),
            bootstrap=dbc.themes.BOOTSTRAP,  # ZEPHYR,
            importances=False,
        )
        if save:
            dashboard.to_yaml("dashboard.yaml", explainerfile="explainer.joblib", dump_explainer=True)

        return dashboard

    def anomaly_insight(self, ds: pd.DataFrame | pd.Series = None, filter_cols: list = None, anomaly_rank: int = 1):
        """
        Return the anomaly defined by anomaly order (1 = most anomalous), and the most similar samples found to
        analyze the anomaly
        Args:
            ds: anomaly to analyze. If None, the most anomalous sample is selected
            filter_cols: columns to filter the most similar samples
            anomaly_rank: rank of the anomaly to analyze (1 = most anomalous)
        """

        if anomaly_rank <= 0:
            log.error("anomaly_rank must be greater than 0")
            return None

        if ds is None:
            ds = self.df_pred.reindex(self.df_pred["deviation %"].abs().sort_values(ascending=False).index).iloc[
                anomaly_rank - 1
            ]

        elif isinstance(ds, pd.DataFrame):
            ds = ds.iloc[0]

        log.info(
            f"Anomaly selected: id: {ds.name}. {self.target}: {ds[self.target]} {self.target_units}. "
            f"Predicted: {ds['predicted']} {self.target_units}.  Deviation: {ds['deviation %']} %"
        )

        if filter_cols is None:
            filter_cols = self.categorical_features

        df_similar_samples = find_similar_samples(
            self.df_pred,
            ds,
            filter_cols=filter_cols,
            numerical_cols=self.numerical_features,
        )
        return df_similar_samples

    def plot_predictions_vs_target(self, df: pd.DataFrame = None):
        """
        Plot the Predicted vs True Target
        Args:
            df: dataframe with predictions. If None, the current self.df_pred is used
        """

        if df is None:
            df = self.df_pred
        fig = plot_predictions_vs_target(df, self.target, group_col=self.group_col)
        return fig

    def plot_interval_predictions(self, df: pd.DataFrame):
        """
        Plot the interval Predictions along with the Predicted & True Target
        Args:
            df: dataframe with predictions. If None, the current 100 samples self.df_pred with sorted index is used
        """
        if df is None:
            df = self.df_pred.head(100).copy().sort_index()
        fig = plot_interval_predictions(df, self.target, self.target_units)
        return fig
