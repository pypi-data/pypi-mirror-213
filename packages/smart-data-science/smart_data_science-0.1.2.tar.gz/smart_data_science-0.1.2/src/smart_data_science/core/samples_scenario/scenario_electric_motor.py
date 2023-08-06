"""
- Title:            SCENARIO DEFINITION - Electric Motor
- Project/Topic:    Smart Data Science.
- Author/s:         Angel Martinez-Tenor
- Dev Date:         2023

- Status:           In progress.
"""

# To use the Scenario, use: scenario.Scenario(**scenario.params)

from dataclasses import dataclass
from pathlib import Path

from smart_data_science.core.scenario_base import ScenarioBase

SCENARIO_TYPE = "regression"
LABEL = "Electric Motor Scenario"
# https://www.kaggle.com/datasets/wkirgsn/electric-motor-temperature?datasetId=236410&sortBy=voteCount
DESCRIPTION = """
The Goal: Predict the "motor_speed" (in rpm) of electric motors given the rest of the variables (ML - regression)

The data set comprises several sensor data collected from a permanent magnet synchronous motor (PMSM) on a test bench.

Content
All recordings are sampled at 2 Hz. The data set consists of multiple measurement sessions,
which can be distinguished from each other by column "profile_id".
A measurement session can be between one and six hours long.

The motor is excited by hand-designed driving cycles denoting a reference motor speed and a reference torque.
Currents in d/q-coordinates (d=direct or active, q=quadrature or reactive) (columns "i_d" and i_q") and voltages in \
d/q-coordinates (columns "u_d" and "u_q") are a result of a standard control strategy trying to follow the reference \
speed and torque. Columns "motor_speed" and "torque" are the resulting quantities achieved by that strategy, derived \
from set currents and voltages.
"""

DATA_FILENAME = "Electric Motor 50k"
TARGET = "motor_speed"
TARGET_UNITS = "rpm"
FEATURES = None
NUMERICAL_FEATURES = None
CATEGORICAL_FEATURES = ["profile_id"]
SORT_COL = None
GROUP_COL = "profile_id"  # COlumn to group by for disaggregated ML results (optional)

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
