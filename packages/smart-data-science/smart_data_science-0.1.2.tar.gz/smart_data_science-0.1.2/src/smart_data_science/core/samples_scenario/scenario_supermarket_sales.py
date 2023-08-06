"""
- Title:            SCENARIO DEFINITION - SUPERMARKET SALES
- Project/Topic:    Smart Data Science.
- Author/s:         Angel Martinez-Tenor
- Dev Date:         2023

- Status:           In progress.
"""


from dataclasses import dataclass
from pathlib import Path

from smart_data_science.core.scenario_base import ScenarioBase

SCENARIO_TYPE = "regression"
LABEL = "Supermarket Sales Scenario"
SCENARIO_DATA_LABEL = "Supermarket Sales Data"
# Source: https://www.kaggle.com/datasets/yasserh/walmart-dataset
DESCRIPTION = """Retail Sector. The goal is to predict the weekly sales of a supermarket.
The synthetic dataset contains weekly sales data for 45 stores of Walmart. It has ~400000 rows, and the variables are:
store - the store number (categorical)
weekly_sales - sales for the given store
temperature - Temperature on the day of sale
fuel_price - Cost of fuel in the region
cpi – Prevailing consumer price index
unemployment - Prevailing unemployment rate
size - Size of the store (in sq ft)
month - Month of sales
"""
# Date - the week of sales

DATA_FILENAME = "Supermarket Sales"
TARGET = "weekly_sales"
TARGET_UNITS = "$"
FEATURES = ["size", "cpi", "unemployment", "temperature", "fuel_price", "dept", "store", "type", "month"]
NUMERICAL_FEATURES = [
    "size",
    "cpi",
    "unemployment",
    "temperature",
    "fuel_price",
]
CATEGORICAL_FEATURES = ["dept", "store", "type", "month"]
SORT_COL = None  # "OrderDate"
GROUP_COL = "type"  # Column to group by for disaggregated ML results (optional)

# ML PARAMS
MODEL_FOLDER = Path("model")
INPUT_ML_PARAMS = None  # {"max_depth": 17, "n_estimators": 50, "n_jobs": -1}
INPUT_ML_MODEL = None  # LGBMRegressor(**INPUT_ML_PARAMS)
CHRONOLOGICAL_SPLIT = False  # If True, the data is split chronologically


params = {
    "scenario_type": SCENARIO_TYPE,
    "label": LABEL,
    "description": DESCRIPTION,
    "data_filename": DATA_FILENAME,
    "target": TARGET,
    "target_units": TARGET_UNITS,
    "features": FEATURES,
    "numerical_features": NUMERICAL_FEATURES,
    "categorical_features": CATEGORICAL_FEATURES,
    "sort_col": SORT_COL,
    "group_col": GROUP_COL,
    "model_folder": MODEL_FOLDER,
    "input_ml_params": INPUT_ML_PARAMS,
    "input_ml_model": INPUT_ML_MODEL,
    "chronological_split": CHRONOLOGICAL_SPLIT,
}


@dataclass
class Scenario(ScenarioBase):
    """Main Object for the Scenario"""

    def process_data(self, df):
        """Process data and Generate normalized tables and variables"""
        df = df[df[TARGET] >= 50000].copy()  # only sales above 50K will be considered
        df = df[df[TARGET] <= 200000].copy()  # only sales above 50K will be considered
        return df
