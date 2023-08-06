"""
- Title:            Utils load Data Samples
- Project/Topic:    Smart Data Science. Practical functions for Data Science
- Author/s:         Angel Martinez-Tenor
- Dev Date:         2017 - 2023

- Status:           Planning

- Acknowledgements. Partially Based on:
    - Personal Repo: https://github.com/angelmtenor/data-science-keras/blob/master/helper_ds.py
"""
from __future__ import annotations

from importlib import resources
from pathlib import Path

import pandas as pd

from smart_data_science.core import io, logger

log = logger.get_logger(__name__)

# PUBLIC_DATASETS = {
#     "Churn Banking": "churn_bank.csv",
#     "Sales Supermarkets": "sales_supermarkets.parquet",
#     "Supply Chain": "shipping_logs.csv",
#     "Energy Building": "energy_building.parquet",
#     "Electric Motor": "electric_motor.parquet",
# }

# public_data_names = list(PUBLIC_DATASETS.keys())
# public_datafiles = [Path(f) for f in PUBLIC_DATASETS.values()]


def get_available_datasets(prefix="") -> dict:
    """Get a dict with the name of available datasets and the paths
    returns:
        dict: Dict with the name of available datasets and the paths
    """
    data_files_format_accepted = [".csv", ".parquet"]

    data_files = [
        f
        for f in resources.contents("smart_data_science.core.samples_data")
        if f.startswith(prefix) and Path(f).suffix in data_files_format_accepted
    ]

    data_dict = {io.format_prefixed_name(i, prefix=prefix): i for i in data_files}

    # with resources.path("smart_data_science.core.data_samples", f"{scenario_module}.py") as f:
    #     scenarios[scenario_name] = f
    return data_dict


def load_sample(dataset_name: str = "Supply Chain") -> pd.DataFrame:
    """Load a Sample Dataset
    args:
        sample_data (str): Name of the sample data to load. Extension can be omitted.
    returns:
        pd.DataFrame: Sample Log Dataset Selected
    """
    df = None
    data_dict = get_available_datasets()
    datafile = data_dict.get(dataset_name)
    if datafile is None:
        log.error(f"Sample data {dataset_name} not available. Available: {data_dict.keys()}")
        return None
    datafile = Path(datafile)

    # if datafile.suffix:
    #     assert datafile.suffix in [".csv", ".parquet"], "Only .csv and .parquet files are supported"
    #     assert datafile in data_dict, f"Sample datafile {datafile} not available. Available: {data_dict.keys()}"
    # else:
    #     for suffix in [".parquet", ".csv"]:
    #         if datafile.with_suffix(suffix) in data_dict:
    #             datafile = datafile.with_suffix(suffix)
    #             break
    #     assert datafile.suffix, f"Sample datafile {datafile} not available. Available: {data_dict.keys()}"

    with resources.path("smart_data_science.core.samples_data", f"{datafile}") as f:
        data_file_path = Path(f)
        if datafile.suffix == ".parquet":
            df = pd.read_parquet(data_file_path)
        elif datafile.suffix == ".csv":
            df = pd.read_csv(data_file_path)
        log.debug(f"Data loaded from {data_file_path} with shape {df.shape} samples")
        return df
