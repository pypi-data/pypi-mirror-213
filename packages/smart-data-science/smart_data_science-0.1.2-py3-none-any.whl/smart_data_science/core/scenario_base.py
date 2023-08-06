"""
- Title:            Scenario Definition Class.
- Project/Topic:    Smart Data Science. Practical functions for Data Science (side project)
- Author/s:         Angel Martinez-Tenor
- Dev Date:         2023

- Status:           In progress.

"""

from abc import ABC
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd

from smart_data_science import info_data, load_sample, logger, optimize_schema
from smart_data_science.ml import ml_utils
from smart_data_science.ui import ui_table_definition  # used for UI only

log = logger.get_logger(__name__)


SCENARIO_TYPE = None
LABEL = None
DESCRIPTION = None

DATA_FILENAME = None
TARGET = None
TARGET_UNITS = None
FEATURES = None
NUMERICAL_FEATURES = None
CATEGORICAL_FEATURES = None
SORT_COL = None
GROUP_COL = None

INPUT_ML_PARAMS = None
INPUT_ML_MODEL = None
MODEL_FOLDER = Path("model")  # TODO set default in post init
CHRONOLOGICAL_SPLIT = False  # TODO set default to False in post init


@dataclass(repr=False)
class ScenarioBase(ABC):  # pylint: disable=R0902  # Too many instance attribute
    """Scenario Base. Abstract Parent Class with common variables & methods for all the Types of Scenarios"""

    scenario_type: str = SCENARIO_TYPE  # "regression"  pending: "classification", "analytics" (partial/derived)
    label: str = LABEL
    description: str = DESCRIPTION

    data_filename: str = DATA_FILENAME
    target: str = TARGET
    target_units: str = TARGET_UNITS
    features: list = FEATURES
    numerical_features: list = NUMERICAL_FEATURES
    categorical_features: list = CATEGORICAL_FEATURES
    sort_col: str = SORT_COL
    group_col: str = GROUP_COL

    input_ml_model: Any = INPUT_ML_MODEL
    input_ml_params: dict = INPUT_ML_PARAMS
    model_folder: Path | str = MODEL_FOLDER
    chronological_split: bool = CHRONOLOGICAL_SPLIT

    def __post_init__(self) -> None:
        """Post initialization"""

        log.info(f"Categories: {self.categorical_features}")
        log.info(f"Target: {self.target}")

        self.df_source: pd.DataFrame = None
        self.df: pd.DataFrame = None  # processed and prepared for ML
        self.summary_dict: dict = None
        self.summary_text: str = None
        self.etl()
        self.generate_table_objects()

    def load_data(self):
        """Load source data)"""
        log.debug(f"Loading data {self.data_filename}")
        df = load_sample(self.data_filename)
        self.df_source = df.copy()
        return df

    def process_data(self, df):
        """Process data and Generate normalized tables and variables"""
        # log.info(f'{"-"*20} PROCESSING SOURCE DATA {"-"*50}')
        if self.sort_col is not None:
            df = df.sort_values(self.sort_col)
        return df

    def prepare_data_for_ml(self, df):
        """Prepare data for ML"""

        df = optimize_schema(df)

        if self.sort_col is not None:
            df = df.sort_values(self.sort_col)

        if self.features:
            df = df[self.features + [self.target]].copy()

        processed_dict = ml_utils.preprocess_input_data(
            df, self.target, self.numerical_features, self.categorical_features
        )

        self.features = processed_dict["features"]
        self.numerical_features = processed_dict["numerical_features"]
        self.categorical_features = processed_dict["categorical_features"]
        self.target = processed_dict["target"]

        df = processed_dict["df"].copy()
        df = optimize_schema(df)
        self.df = df.copy()
        return df

    def etl(self):
        """load, process and prepare data for ML. ALso generates a summary of the parameters of the scenario"""
        df = self.load_data()
        df = self.process_data(df)
        df = self.prepare_data_for_ml(df)
        self.generate_summary()
        return df

    def info_data_log(self):  # log only
        """Log info of processed data for ml"""
        info_data(
            self.df,
            unique=True,
            plot=True,
            types=True,
            corr_matrix=True,
            corr_matrix_sort_col=self.target,
        )

    def generate_table_objects(self):
        """Generate table objects"""
        df = self.df.copy()
        self.table_data_for_ml = ui_table_definition.DataForML(df)

    def generate_summary(self):
        """Generate summary of the main attributes in dict and text format"""

        # generate json from attributes:
        summary_dict = {
            "description": self.description,
            "scenario_type": self.scenario_type,
            "label": self.label,
            "target": self.target,
            "target_units": self.target_units,
            "numerical_features": self.numerical_features,
            "categorical_features": self.categorical_features,
            "sort_col": self.sort_col,
            "group_col": self.group_col,
            "input_ml_params": self.input_ml_params,
            "input_ml_model": self.input_ml_model,
            "chronological_split": self.chronological_split,
        }

        # remove None anf False values:
        summary_dict = {k: v for k, v in summary_dict.items() if v is not None and v is not False}

        self.summary_dict = summary_dict
        self.summary_text = ". ".join([f"{k}: {v}" for k, v in summary_dict.items()])
