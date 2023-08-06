"""
- Title:            ML INTERVALS. Smart Model for tabular data
- Project/Topic:    Smart Data Science. Practical functions for Data Science (side project)
- Author/s:         Angel Martinez-Tenor
- Dev Date:         2018-2023

- Status:           In progress.
"""

from __future__ import annotations

from copy import deepcopy

import pandas as pd
from lightgbm import LGBMClassifier, LGBMRegressor
from sklearn.pipeline import Pipeline

from smart_data_science.core import logger
from smart_data_science.ml.ml_utils import get_ml_params

log = logger.get_logger(__name__)

DEFAULT_CONFIDENCE_INTERVAL = 0.95  # used for Interval Prediction. 95% by default (alpha = 0.05)

LGBM_MODELS = (LGBMRegressor, LGBMClassifier)


def fit_intervals(
    pipeline: Pipeline = None,
    ml_model=None,
    x: pd.DataFrame = None,
    y: pd.Series = None,
    confidence: float = None,
):
    """Generate prediction intervals model
    Args:
        alpha (float, optional): Confidence interval.
    """
    if confidence is None:
        confidence = DEFAULT_CONFIDENCE_INTERVAL

    if pipeline is None and ml_model is None:
        log.critical("No pipeline or model provided")
        raise ValueError("No pipeline or model provided")

    if pipeline is not None and ml_model is not None:
        log.warning("Both pipeline and model provided. Using pipeline")

    if pipeline is not None:
        ml_model = pipeline.steps[-1][1]

    pipeline_lower, pipeline_upper = None, None

    lgbm_model = None
    if isinstance(pipeline["ml_model"], LGBMRegressor):
        log.info("LGBMRegressor detected: Using quantile objective to get the prediction intervals")
        lgbm_model = LGBMRegressor
    elif isinstance(pipeline["ml_model"], LGBMClassifier):
        log.info("LGBMClassifier detected: Using quantile objective to get the prediction intervals")
        lgbm_model = LGBMClassifier
    else:
        log.warning("No prediction intervals model available for this ML model")

    if lgbm_model is not None:
        pipeline_lower = deepcopy(pipeline)
        pipeline_upper = deepcopy(pipeline)

        ml_params_intervals = get_ml_params(pipeline).copy()
        ml_params_intervals["objective"] = "quantile"

        model_lower = lgbm_model(**ml_params_intervals, alpha=1 - confidence)
        pipeline_lower.steps[-1] = ("ml_model", model_lower)
        pipeline_lower.fit(x, y)

        model_upper = lgbm_model(**ml_params_intervals, alpha=confidence)
        pipeline_upper.steps[-1] = ("ml_model", model_upper)
        pipeline_upper.fit(x, y)

        # TO IMPROVE: use MAPIE
        # mapie_reg = MapieRegressor(
        #     pipeline, cv="prefit", method="plus"
        # )  # Change method to cdr (ml objective: quantile)
        # mapie_reg.fit(self.x, self.y)
        # mapie_y_pred, mapie_y_pis = mapie_reg.predict(self.x, alpha=alpha)

        # self.mapie_reg = mapie_reg
        # self.mapie_y_pred = mapie_y_pred
        # self.mapie_y_pis = mapie_y_pis
        # self.mapie_alpha = alpha

        # self.mapie_coverage_scores = [
        #     regression_coverage_score(self.y, mapie_y_pis[:, 0, i], mapie_y_pis[:, 1, i]) for i, _ in enumerate(alpha)
        # ]

        # Optional: if the model is lightgbm, we can use the quantile objective to get the prediction intervals

    return pipeline_lower, pipeline_upper


def predict_intervals(
    pipeline_lower,
    pipeline_upper,
    x: pd.DataFrame,
    # ml_type: str = ModelType.REGRESSOR,
) -> pd.DataFrame:
    """Predict intervals
    Args:
        x (pd.DataFrame): Input data.
    Returns:
        pd.DataFrame: Prediction intervals.
    """

    df = pd.DataFrame(index=x.index)

    # if isinstance(pipeline["ml_model"], LGBM_MODELS):
    #     lgbm_model = LGBMRegressor
    # if ml_type == ModelType.CLASSIFICATION:
    #     lgbm_model = LGBMClassifier

    # Optional: if the model is lightgbm, we can use the quantile objective to get the prediction intervals
    if isinstance(pipeline_lower["ml_model"], LGBMRegressor):
        df["predicted_lower"] = pipeline_lower.predict(x).astype("float32").round(2)
        df["predicted_upper"] = pipeline_upper.predict(x).astype("float32").round(2)
    elif isinstance(pipeline_lower["ml_model"], LGBMClassifier):
        df["predicted_lower"] = pipeline_lower.predict_proba(x)[:, 1].astype("float32").round(3)
        df["predicted_upper"] = pipeline_upper.predict_proba(x)[:, 1].astype("float32").round(3)
    else:
        log.warning(
            "No prediction intervals model available for this ML model"
        )  # To Improve: use MAPIE with other models

        # if ml_type == ModelType.REGRESSOR:
        #     pass  # To improve: add other models

        return None

    # TO IMPROVE: use MAPIE
    # mapie_y_pred, mapie_y_pis = self.mapie_reg.predict(x, alpha=alpha)
    # df = pd.DataFrame(mapie_y_pis.reshape(mapie_y_pis.shape[0], -1), index=x.index)
    # df.columns = [f"{alpha_item}_{bound}" for bound in ["lower", "upper"] for alpha_item in alpha]
    # # same as above but

    # df["predicted"] = mapie_y_pred
    # df["coverage"] = self.mapie_coverage_scores

    # add column with the difference between the upper and lower bound
    df["predicted_interval_diff"] = df["predicted_upper"] - df["predicted_lower"]
    return df
