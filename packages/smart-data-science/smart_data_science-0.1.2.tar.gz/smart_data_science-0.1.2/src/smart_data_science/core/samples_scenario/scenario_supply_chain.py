"""
- Title:            SCENARIO DEFINITION - SUPPLY CHAIN
- Project/Topic:    Smart Data Science.
- Author/s:         Angel Martinez-Tenor
- Dev Date:         2023

- Status:           In progress.
"""


from dataclasses import dataclass
from pathlib import Path

from smart_data_science.core.scenario_base import ScenarioBase

SCENARIO_TYPE = "regression"
LABEL = "Supply Chain Scenario"
# source: https://catalog.us-east-1.prod.workshops.aws/workshops/80ba0ea5-7cf9-4b8c-9d3f-1cd988b6c071/en-US/1-use-cases/7-supply-chain # noqa # pylint: disable=line-too-long
DESCRIPTION = """Logistic Sector. The  goal is to predict the estimated time of arrival of the shipment in \
    number of days. The synthetic dataset contains complete shipping data for all products delivered including \
    estimated time, shipping priority, carrier and origin. It has ~10000 rows, 12 feature columns, and the data schema \
is the following:

Feature Name:	Description
ActualShippingDays:	Number of days it took to deliver the shipment
Carrier:	Carrier used for shipment
YShippingDistance:	Distance of shipment on the Y-axis
XShippingDistance:	Distance of shipment on the X-axis
InBulkOrder:	Is it a bulk order
ShippingOrigin:	Origin of shipment
ShippingPriority:	Priority of Shipping
"""

DATA_FILENAME = "Supply Chain"
TARGET = "ActualShippingDays"
TARGET_UNITS = "days"
FEATURES = ["Carrier", "YShippingDistance", "XShippingDistance", "InBulkOrder", "ShippingOrigin", "ShippingPriority"]
NUMERICAL_FEATURES = None
CATEGORICAL_FEATURES = None
SORT_COL = "OrderDate"
GROUP_COL = "ShippingPriority"  # Column to group by for disaggregated ML results (optional)

# ML PARAMS
MODEL_FOLDER = Path("model")
INPUT_ML_PARAMS = None
INPUT_ML_MODEL = None
CHRONOLOGICAL_SPLIT = False  # If True, the data is split chronologically
# ML_PARAMS = {"max_depth": 17, "n_estimators": 50, "n_jobs": -1}
# ML_MODEL = LGBMRegressor(**INPUT_ML_PARAMS)


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
        df["ActualShippingDays"] = df["ActualShippingDays"].clip(lower=1, upper=25)  # clip anomalies/outliers
        return df
