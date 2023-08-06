"""
- Title:            Utils Scenario Samples
- Project/Topic:    Smart Data Science. Practical functions for Data Science
- Author/s:         Angel Martinez-Tenor
- Dev Date:         2017 - 2023

- Status:           Planning

- Acknowledgements. Partially Based on:
    - Personal Repo: https://github.com/angelmtenor/data-science-keras/blob/master/helper_ds.py
"""
from __future__ import annotations

from importlib import resources
from types import ModuleType

from smart_data_science.core import io, logger

# from pathlib import Path

# import pandas as pd


log = logger.get_logger(__name__)


# return a dict with the name of available scenarios and the path of the module
def get_internal_scenarios(prefix="scenario_") -> dict:
    """Get a dict with the name of available scenarios and the path of the module
    returns:
        dict: Dict with the name of available scenarios and the path of the module
    """
    # scenarios = {}
    # package_name = "smart_data_science"
    # folder_path = "core.data_samples"
    scenario_files = [
        f
        for f in resources.contents("smart_data_science.core.samples_scenario")
        if f.startswith(prefix) and f.endswith(".py")
    ]

    scenario_dict = {io.format_prefixed_name(i, prefix=prefix): i for i in scenario_files}

    # with resources.path("smart_data_science.core.data_samples", f"{scenario_module}.py") as f:
    #     scenarios[scenario_name] = f
    return scenario_dict


def load_internal_scenario(scenario_name: str) -> ModuleType:  # TODO IN PROGRESS
    """Load a Scenario module
    args:
        scenario_name (str): Name of the scenario to load. Extension can be omitted.
    returns:
        pd.DataFrame: Sample Log Dataset Selected
    """
    scenario_dict = get_internal_scenarios()
    scenario_module = scenario_dict.get(scenario_name)
    if scenario_module is None:
        log.error(f"Scenario {scenario_name} not available. Available: {scenario_dict.keys()}")
        return None

    log.info(scenario_module)

    with resources.path("smart_data_science.core.samples_scenario", f"{scenario_module}") as f:
        module = io.import_custom_module(f)
        return module
