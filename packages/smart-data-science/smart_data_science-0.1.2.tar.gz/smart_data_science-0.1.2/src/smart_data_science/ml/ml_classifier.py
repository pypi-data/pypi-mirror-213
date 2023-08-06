"""
- Title:            TEMPLATE ML PIPELINE. Smart Classifier for tabular data
- Project/Topic:    Smart Data Science. Practical functions for Data Science  (side project)
- Author/s:         Angel Martinez-Tenor
- Dev Date:         2020 - 2023

- Status:           Planned


"""

# import pickle
from copy import deepcopy
from dataclasses import dataclass

import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
from explainerdashboard import ClassifierExplainer, ExplainerDashboard
from lightgbm import LGBMClassifier
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score
from sklearn.pipeline import Pipeline

# from smart_data_science.analysis.info_advanced import find_similar_samples
from smart_data_science.core import logger
from smart_data_science.ml import ml_utils
from smart_data_science.ml.ml_base import SmartModel
from smart_data_science.ml.ml_utils import ModelType
from smart_data_science.ml.plot_intervals import plot_interval_predictions
from smart_data_science.process.transform import multi_to_single_index

# from pathlib import Path


# from mapie.metrics import regression_coverage_score
# from mapie.regression import MapieRegressor


log = logger.get_logger(__name__)

MODEL_TYPE = ModelType(ModelType.REGRESSOR)

DEFAULT_PATH_OBJECT = "model/smart_classifier.pkl"
CONFIDENCE_INTERVAL = 0.95  # used for Interval Prediction. 95% by default (alpha = 0.05)

DEFAULT_ML_PARAMS = {"max_depth": 7, "n_estimators": 250, "n_jobs": -1}
DEFAULT_ML_MODEL = LGBMClassifier(**DEFAULT_ML_PARAMS)

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

DEFAULT_METRICS = {"ROC_AUC": roc_auc_score, "F1_SCORE": f1_score, "ACCURACY": accuracy_score}
# type of metric (to be maximized or minimized)
DEFAULT_METRICS_TYPE = {"ROC_AUC": "max", "F1_SCORE": "max", "ACCURACY": "max"}
DEFAULT_METRICS_SCORING = {"ROC_AUC": "roc_auc", "F1_SCORE": "f1", "ACCURACY": "accuracy"}


@dataclass(repr=False)
class SmartClassifier(SmartModel):  # pylint: disable=too-many-instance-attributes
    """Smart Classifier for tabular data
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

    default_ml_model: LGBMClassifier = DEFAULT_ML_MODEL
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
        df_pred["predicted"] = self.pipeline.predict(df_pred)
        df_pred["predicted_proba"] = self.pipeline.predict_proba(df_pred)[:, 1].round(3)
        return df_pred

    def fit_intervals(self, confidence: float = CONFIDENCE_INTERVAL):  # TO TEST.  USEFUL FOR CLASSIFIER?
        """Generate prediction intervals model
        Args:
            alpha (float, optional): Confidence interval.
        """

        if isinstance(self.pipeline["ml_model"], LGBMClassifier):
            log.info("LIghtGBM detected: Using quantile objective to get the prediction intervals")

            pipeline_lower = deepcopy(self.pipeline)
            pipeline_upper = deepcopy(self.pipeline)

            ml_params_intervals = ml_utils.get_ml_params(self.pipeline).copy()
            ml_params_intervals["objective"] = "quantile"

            model_lower = LGBMClassifier(**ml_params_intervals, alpha=1 - confidence)
            pipeline_lower.steps[-1] = ("ml_model", model_lower)
            pipeline_lower.fit(self.x, self.y)

            model_upper = LGBMClassifier(**ml_params_intervals, alpha=confidence)
            pipeline_upper.steps[-1] = ("ml_model", model_upper)
            pipeline_upper.fit(self.x, self.y)

            self.pipeline_lower = pipeline_lower
            self.pipeline_upper = pipeline_upper

        else:
            log.warning("No prediction intervals model available for this ML model")

    def predict_intervals(self, x: pd.DataFrame) -> pd.DataFrame:
        """Predict intervals
        Args:
            x (pd.DataFrame): Input data.
        Returns:
            pd.DataFrame: Prediction intervals.
        """

        # mapie_y_pred, mapie_y_pis = self.mapie_reg.predict(x, alpha=alpha)
        # df = pd.DataFrame(mapie_y_pis.reshape(mapie_y_pis.shape[0], -1), index=x.index)
        # df.columns = [f"{alpha_item}_{bound}" for bound in ["lower", "upper"] for alpha_item in alpha]
        # # same as above but

        # df["predicted"] = mapie_y_pred
        # df["coverage"] = self.mapie_coverage_scores
        df = pd.DataFrame(index=x.index)

        # Optional: if the model is lightgbm, we can use the quantile objective to get the prediction intervals
        if isinstance(self.pipeline["ml_model"], LGBMClassifier):
            df["predicted_lower"] = self.pipeline_lower.predict_proba(x).astype("float32").round(3)
            df["predicted_upper"] = self.pipeline_upper.predict_proba(x).astype("float32").round(3)
            # add column with the difference between the upper and lower bound
            df["predicted_interval_diff"] = df["predicted_upper"] - df["predicted_lower"]
            return df

        log.warning("No prediction intervals model available for this ML model")
        return None

    def finalize(self, save: bool = True, save_path: str = None, units=None, title=None) -> None:
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
        # df_pred["deviation %"] = 100 * (df_pred["predicted"] - df_pred[self.target]) / df_pred[self.target]
        # df_pred["deviation %"] = df_pred["deviation %"].astype(float).round(2)

        log.info("Generate Classifier explainer for Dashboard ...")
        self.generate_classifier_explainer_for_dashboard(title=title)

        self.df_pred = df_pred
        self.df_contributions = df_contributions

        if save:
            self.save_object(save_path)

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
        df_pred["predicted"] = self.pipeline.predict(df_pred)
        df_pred["predicted_proba"] = self.pipeline.predict_proba(df_pred)[:, 1].round(3)

        # Generate prediction intervals
        if logs:
            log.info("Predicting intervals ...")
        if intervals:
            df_pred_intervals = self.predict_intervals(x)
            df_pred = df_pred.join(df_pred_intervals)

            # Correct Interval if the lower bound is higher than the prediction and / or the upper bound is lower than
            # the prediction and recalculate the difference between the upper and lower bound
            df_pred["predicted_lower"] = np.where(
                df_pred["predicted_lower"] > df_pred["predicted_proba"],
                df_pred["predicted_proba"],
                df_pred["predicted_lower"],
            )
            df_pred["predicted_upper"] = np.where(
                df_pred["predicted_upper"] < df_pred["predicted_proba"],
                df_pred["predicted_proba"],
                df_pred["predicted_upper"],
            )
            df_pred["predicted_interval_diff"] = df_pred["predicted_upper"] - df_pred["predicted_lower"]

            # df_pred["predicted_interval_%"] = 100 * df_pred["predicted_interval_diff"] / df_pred["predicted"]

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

    def generate_classifier_explainer_for_dashboard(  # Move to base class
        self, mode="dash", save_dashboard=True, title="Explainer Dashboard"
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
            reg_explainer = ClassifierExplainer(
                ml_model, df_x_test_transformer, self.y_test, cats=self.categorical_features
            )
        else:
            log.debug(df_x_test_transformer.columns)
            log.debug(df_x_test_transformer.shape)
            log.debug(self.y_test.shape)

            reg_explainer = ClassifierExplainer(ml_model, df_x_test_transformer, self.y_test)

        if save_dashboard:
            self.explainer_dashboard(reg_explainer, save=True, mode=mode, title=title)

        self.x_test_transformed = x_test_transformed
        self.reg_explainer = reg_explainer

    def explainer_dashboard(self, clf_explainer=None, save=False, mode="dash", title=None):
        """
        Generate the explainer dashboard from a regression explainer
        """

        if clf_explainer is None:
            clf_explainer = self.clf_explainer

        if clf_explainer is None:
            raise ValueError("There is no classifier explainer. Please generate one first.")

        if title is None:
            title = self.dashboard_title
        if title is None:
            title = "Explainer Dashboard"
        self.dashboard_title = title

        dashboard = ExplainerDashboard(
            clf_explainer,
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

    def plot_interval_predictions(self, df: pd.DataFrame):
        """
        Plot the interval Predictions along with the Predicted & True Target
        Args:
            df: dataframe with predictions. If None, the current 100 samples self.df_pred with sorted index is used
        """
        if df is None:
            df = self.df_pred.head(100).copy().sort_index()
        fig = plot_interval_predictions(df, self.target, self.target_units, regression=False)
        fig.show()


# Classifier Functions from old dev:

# # ## DEV Tune the model. Grid Search including Transformers
# def tune_pipeline(pipeline, x_train, y_train):
#     """Return the best pipeline"""
#     params = {
#         "classifier__max_depth": [7, 13, 17, 21],
#         "classifier__n_estimators": [30, 50, 70],
#         "classifier__min_samples_leaf": [1],
#         "classifier__min_samples_split": [2],
#         "preprocessor__num__imputer__strategy": ["mean", "median"],
#     }
#     grid_search = GridSearchCV(pipeline, cv=10, param_grid=params, n_jobs=-1)

#     grid_search.fit(x_train, y_train.values.ravel())

#     print("Best params:")
#     print(grid_search.best_params_)
#     print(f"Internal CV score: {grid_search.best_score_:.3f}")
#     print()

#     # ### Best Model / Pipeline
#     pipeline = grid_search.best_estimator_
#     return pipeline


# # --- SCENARIO-INDEPENDENT FUNCTIONS


# def load_pipeline(filename=PATH_ML_PIPELINE):
#     """Load the pipeline & trained model"""
#     if GOOGLE_CLOUD:
#         google_cloud.load_from_bucket(filename)
#     pipeline = joblib.load(filename)
#     print(f"Pipeline Loaded:\t{filename}")
#     return pipeline


# def save_pipeline(pipeline, filename=PATH_ML_PIPELINE):
#     """Save the pipeline & trained model"""
#     joblib.dump(pipeline, filename, compress=True)
#     print(f"\nML Pipeline Saved:\t{filename}")
#     if GOOGLE_CLOUD:
#         google_cloud.save_to_bucket(filename)


# def train_and_evaluate_pipeline(
#     pipeline, X, y, include_explainer=True, plot_explainer=True
# ):  # PIPELINE BROKEN IN NEW SKLEARN VERSIONS.
#     """Train & evaluate a ML pipeline"""
#     x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0, stratify=y)
#     print(f"Training shape:\t{x_train.shape}")
#     print(f"Test shape: \t{x_test.shape}")
#     # metrics available: sklearn.metrics.SCORERS.keys()
#     scoring = ["accuracy", "roc_auc"]
#     scores = cross_validate(pipeline, x_train, y_train.values.ravel(), cv=10, scoring=scoring, n_jobs=-1)
#     print("\nTraining set:")
#     show_cv_scores(scores)
#     # Fit/Train the pipeline with the training set
#     pipeline.fit(x_train, y_train.values.ravel())
#     # Evaluate using the test Set (Once Only)
#     print("\nTest set:")
#     evaluate_test_set(pipeline, x_test, y_test)
#     if include_explainer and plot_explainer:
#         ml_explainer.evaluate_explainer(pipeline, x_train, x_test)


# def show_cv_scores(scores, show_list=False):
#     """Show Mean and Std of CV Accuracy and ROC_AUC"""
#     acc = scores["test_accuracy"]
#     roc_auc = scores["test_roc_auc"]

#     print("CV Accuracy", end=" ")
#     print(f" mean: {acc.mean().round(2)}", end=" ")
#     print(f" std: {acc.std().round(2)}")

#     if show_list:
#         print(acc.round(2))

#     print("CV ROC_AUC ", end=" ")
#     print(f" mean: {roc_auc.mean().round(2)}", end=" ")
#     print(f" std: {roc_auc.std().round(2)}")

#     if show_list:
#         print(roc_auc.round(2))


# def evaluate_test_set(pipeline, x_test, y_test):
#     """Show the accuracy & ROC_AUC of the model given x & y"""
#     # y_pred = pipeline.predict(x_test)
#     y_pred_proba = pipeline.predict_proba(x_test)

#     print(f"Accuracy:\t{pipeline.score(x_test, y_test):.2f}")
#     roc_auc = roc_auc_score(y_test, y_pred_proba[:, 1])
#     print(f"ROC_AUC: \t{roc_auc:.2f}")


# def predict(pipeline, df):
#     """Predict data from a ML pipeline (scikit-learn)"""
#     df_pred = df[features].copy()
#     df_pred["True Prob %"] = pipeline.predict_proba(df_pred)[:, 1]
#     df_pred["True Prob %"] = (df_pred["True Prob %"] * 100).round(2)
#     df_pred = df_pred.sort_values(by="True Prob %", ascending=False)
#     return df_pred
