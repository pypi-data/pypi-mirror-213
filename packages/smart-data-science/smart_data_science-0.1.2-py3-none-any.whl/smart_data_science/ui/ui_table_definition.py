"""
- Title:            UI Table Definitions. Definition of tables for UI I/O
- Project/Topic:    Smart Data Science. Practical functions for Data Science  (side project)
- Author/s:         Angel Martinez-Tenor
- Dev Date:         2020 - 2023

- Status:           In progress.

"""

from abc import ABC
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from smart_data_science import logger
from smart_data_science.core import io
from smart_data_science.ui import ui_io

# # Data & Output paths
# DATA_PATH = "../data/"
# OUTPUT_PATH = "../output/"

PATH_NORMALIZED = Path("data/normalized")
FILEPATH_DATA_FOR_ML = PATH_NORMALIZED / "data.parquet"

log = logger.get_logger(__name__)

# UPDATE TO  @dataclass


@dataclass(repr=False)
class DataTable(ABC):  # pylint: disable=too-many-instance-attributes

    """Data Table Definition. Abstract Parent Class with common variables & methods for all the Tables
    Args:
        df (pd.DataFrame): Dataframe with the data
        table_name (str): Name of the table
        filepath (Path): Path to the parquet file with the data processed
        filepath_source (Path): Path to the source file
        variables (list): List of variables to be used in the table
        index_col (str): Name of the index column
        reference_date_col (str): Name of the reference date column
        link_zip (str): Link to the zip file with the source data
    """

    df: pd.DataFrame
    table_name: str
    filepath: str | Path  # parquet file
    filepath_source: str | Path
    variables: list = None
    index_col: str = None
    reference_date_col: str = None
    link_zip: str = None  # link to zip of last uploaded excel file (Streamlit download solution)

    def __post_init__(self) -> None:
        """post Initialization"""
        self.filepath = Path(self.filepath)
        self.filepath_source = Path(self.filepath_source)

    def process(self, df: pd.DataFrame, check: bool = False, drop_duplicates: bool = True) -> pd.DataFrame:
        """
        Parse & Process the input dataframe
        Args:
            df (pd.DataFrame): Input dataframe
            check (bool): Check if the variables are in the dataframe
            matrix_type (bool): If the table is a matrix type (no index)
        Returns:
            pd.DataFrame: Processed dataframe

        """
        df = df.copy()
        # if df.index.name == self.index:
        #     df = df.reset_index()
        if check and self.variables is not None:
            check_variables(df.reset_index(), self.variables)
            df = df[self.variables]
        df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)  # Remove Tailing spaces found excel files

        if drop_duplicates:
            df = df.drop_duplicates()
        # to improve: check for unique indexes when dropping duplicates
        # df = df.dropna(subset=[self.index])  # Reject samples with null index
        # df.set_index(self.index, inplace=True)
        return df

    def etl(self, filepath=None) -> None:
        """
        Load the source File, parse, process & save the normalized data to parquet
        Args:
            filepath (Path): Path to the source file
        """
        if not filepath:
            filepath = self.filepath_source
        df = self.load_source(filepath)
        df = self.process(df)
        self.df = df
        df.to_parquet(self.filepath)

    def load(self) -> pd.DataFrame:
        """
        Load the normalized parquet file
        """
        df = pd.read_parquet(self.filepath)

        check_variables(df.reset_index(), self.variables)
        self.df = df.copy()
        return df

    def check_datafile(self) -> None:
        """
        Generate  a normalized parquet datafile if it nor exists.
        Future Improvement: To be used for a Recovery
        """
        if not Path(self.filepath).exists():
            self.etl()

    def load_source(self, filepath=None) -> pd.DataFrame:
        """
        Abstract method: Load the  source file into a dataframe
        Args:
            filepath (Path): Path to the source file
        """
        if not filepath:
            filepath = self.filepath_source
        df = io.load_datafile(filepath)
        return df

    def update_excel_and_zip(self, file_uploaded) -> None:
        """
        Save uploaded excel & zip files.
        """
        ui_io.save_file_and_zip(file_uploaded, self.filepath_source)

    def generate_download_link(self, filepath: str | Path = None) -> None:  # type: ignore
        """
        Generate a downloadable link of a zipped file with the last file uploaded
        """
        if filepath is None:
            filepath = self.filepath_source

        filepath = Path(filepath)

        self.link_zip = ui_io.generate_download_link(filepath, caption="**Download**")

    def save_and_generate_download_link(self, filepath: str | Path):  # New - fast demo
        """
        Generate a downloadable link of a zipped file with the last file uploaded
        """
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        self.df.to_parquet(filepath)
        self.generate_download_link(filepath)


@dataclass(repr=False)
class DataForML(DataTable):
    """Table Products Definition"""

    df: pd.DataFrame
    table_name: str = "DATA FOR ML"
    filepath: str | Path = FILEPATH_DATA_FOR_ML
    filepath_source: str | Path = FILEPATH_DATA_FOR_ML

    def __post_init__(self) -> None:
        super().__post_init__()
        self.save_and_generate_download_link(self.filepath)
        # TO IMPROVE check rest of variables, Add numerical_features, etc.. .


def check_variables(df, needed_variables):
    """
    Check if all the variables from the list or set 'needed_variables' are columns of the input dataframe 'df.
    Generate an assertion error showing the missing the variables if any
    """
    missing_variables = set(needed_variables).difference(set(df))

    try:
        assert not missing_variables
    except AssertionError as exc:
        error_message = f"ERROR: MISSING VARIABLES: {missing_variables}"
        log.critical(error_message)
        raise AssertionError(error_message) from exc
