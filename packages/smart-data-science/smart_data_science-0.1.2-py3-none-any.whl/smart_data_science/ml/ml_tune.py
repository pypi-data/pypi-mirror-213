"""
- Title:            ML TUNE. Smart Model for tabular data
- Project/Topic:    Smart Data Science. Practical functions for Data Science  (side project)
- Author/s:         Angel Martinez-Tenor
- Dev Date:         2018-2023

- Status:           In progress.
"""

from __future__ import annotations

import pandas as pd
from sklearn.pipeline import Pipeline
from skopt import BayesSearchCV

from smart_data_science.core import logger

log = logger.get_logger(__name__)


def tune_pipeline(
    pipeline: Pipeline,
    x_train: pd.DataFrame,
    y_train: pd.Series | pd.DataFrame,
    param_grid: dict = None,
    n_iter: int = 100,
    verbose: int = 0,
    cv: int = 3,
    scoring: str = None,  # "r2"
    method: str = "Bayes",
) -> Pipeline:
    """Perform a Bayesian Search and Return the best pipeline

    Args:
        pipeline (sklearn-type pipeline): input pipeline to tune
        x_train (pd.DataFrame): input features
        y_train (pd.Series | pd.DataFrame): input target
        param_grid (dict): dictionary of parameters:values to tune. default values (If None):
            {
                "ml_model__max_depth": [7, 9, 11, 13, 15, 17],
                "ml_model__n_estimators": [30, 50, 70, 100, 250, 400, 600],
            }
        n_iter (int): number of iterations for Bayesian search
        verbose (int): verbosity of the search
        cv (int): number of folds for cross-validation (minimum 2)
        scoring (str): scoring metric

    Returns:
        The best estimator found during the search.
    """
    log.info(f"Training {n_iter} pipelines with {cv} Cross validations ({n_iter*cv} models) ...")

    if method == "Bayes":
        optimizer_search = BayesSearchCV(
            pipeline, cv=cv, search_spaces=param_grid, n_jobs=-1, scoring=scoring, n_iter=n_iter, verbose=verbose
        )
    else:
        raise ValueError(f"Method {method} not implemented")

    optimizer_search.fit(x_train, y_train.values.ravel())

    best_pipeline = optimizer_search.best_estimator_

    return best_pipeline
