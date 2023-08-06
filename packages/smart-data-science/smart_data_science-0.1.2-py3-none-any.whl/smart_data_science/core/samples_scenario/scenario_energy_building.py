"""
- Title:            SCENARIO DEFINITION - Electric Motor
- Project/Topic:    Smart Data Science.
- Author/s:         Angel Martinez-Tenor
- Dev Date:         2023

- Status:           In progress.
"""

# To use the Scenario, use: scenario.Scenario(**scenario.params)


import calendar
from dataclasses import dataclass
from pathlib import Path

from smart_data_science import logger
from smart_data_science.core.scenario_base import ScenarioBase

log = logger.get_logger(__name__)


# from lightgbm import LGBMRegressor

DESCRIPTION = """
The Goal: Predict the Energy Consumption of a Building (in Wh). Target: "Energy_Appliances" (ML - regression)
Dataset Information: 10 min averaged samples for about 4.5 months
Variables:
date time year-month-day hour:minute:second
Energy_Appliances, energy use in Wh
Energy_Lights, energy use of light in Wh
T1, Temperature in kitchen area, in Celsius
RH_1, Humidity in kitchen area, in %
T2, Temperature in living room area, in Celsius
RH_2, Humidity in living room area, in %
T3, Temperature in laundry room area
RH_3, Humidity in laundry room area, in %
To, Temperature outside (from weather station), in Celsius
Pressure (from weather station), in mm Hg
RH_out, Humidity outside (from weather station), in %
Wind speed (from weather station), in m/s
Visibility (from weather station), in km
Tdewpoint (from weather station), in °C
rv1, Random variable 1, adimensional
rv2, Random variable 2, adimensional
"""

SCENARIO_TYPE = "regression"
LABEL = "Energy Building Scenario"
# https://archive.ics.uci.edu/ml/datasets/Appliances+energy+prediction


DATA_FILENAME = "Energy Building"  # todo change
TARGET = "Energy_Appliances"
TARGET_UNITS = "Kwh"
FEATURES = None
NUMERICAL_FEATURES = None
CATEGORICAL_FEATURES = ["is_holiday", "day_of_week", "month", "year"]
SORT_COL = None
GROUP_COL = None  # Column to group by for disaggregated ML results (optional)

# ML PARAMS
MODEL_FOLDER = Path("model")
INPUT_ML_PARAMS = None  # {"max_depth": 7, "n_estimators": 50, "n_jobs": -1}
INPUT_ML_MODEL = None  # LGBMRegressor(**ML_PARAMS)
CHRONOLOGICAL_SPLIT = False  # If True, the data is split chronologically

params = {
    "description": DESCRIPTION,
    "scenario_type": SCENARIO_TYPE,
    "label": LABEL,
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


@dataclass  # (init=False)
class Scenario(ScenarioBase):
    """Main Object for the Scenario"""

    def process_data(self, df):
        """Process data and Generate normalized tables and variables"""
        # log.info(f'{"-"*20} PROCESSING SOURCE DATA {"-"*50}')
        if self.sort_col is not None:
            df = df.sort_values(self.sort_col)

        df["day_of_week"] = df["day_of_week"].apply(lambda x: calendar.day_name[x])
        df["month"] = df["month"].apply(lambda x: calendar.month_name[x])
        if "lights" in df.columns:
            df = df.drop(columns=["lights"])
        # rename to Energy_Appliances
        df = df.rename(columns={"Appliances": "Energy_Appliances"})

        # remove temp and humidity variables different to 1, 2, 3 (1 = T1 and RH_1)
        df = df.drop(
            columns=[
                "T4",
                "RH_4",
                "T5",
                "RH_5",
                "T6",
                "RH_6",
                "T7",
                "RH_7",
                "T8",
                "RH_8",
                "T9",
                "RH_9",
            ]
        )
        return df
