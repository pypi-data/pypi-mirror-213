"""
- Title:            Utils System. Wrapper on top of Pandas for common OS/environment calls
- Project/Topic:    Utils Tabular Data. Practical functions for Data Science
- Author/s:         Angel Martinez-Tenor
- Dev Date:         2017 - 2022

- Status:           Planning

- Acknowledgements. Partially Based on:
    - Personal Repo: https://github.com/angelmtenor/data-science-keras/blob/master/helper_ds.py
"""

from __future__ import annotations

import os
import pickle
import platform
import sys
import time
from pathlib import Path

import cpuinfo  # pip py-cpuinfo
import pkg_resources
import psutil

from smart_data_science.core import logger

log = logger.get_logger(__name__)

INSTALLED_PACKAGES = pkg_resources.working_set
installed_packages_dict = {i.key: i.version for i in INSTALLED_PACKAGES}  # pylint: disable=not-an-iterable

DEFAULT_MODULES = [
    "pandas",
    "scikit-learn",
    "lightgbm",
    "shap",
    "streamlit",
    # "tensorflow",
]


def get_root(target_path, cwd: Path | str = Path.cwd(), depth: int = 0, max_depth: int = 5) -> Path:
    """Get the root path of the project, defined by the closest parent folder that contains the target_path

    Args:
        target_path (Path or str): Target path. e.g.: 'my-cloned-repo'
        cwd (Path | str, optional): Current Working Directory of the execution environment. Defaults to Path.cwd().
        depth (int, optional): Current call's recursion depth. Defaults to 0.
        max_depth (int, optional): Maximum recursion depth to stop search. Defaults to 5.

    Raises:
        ValueError: If the root path is not found within `max_depth` recursive calls (calls to path.parent each time).

    Returns:
        Path: Root path of the project.
    """
    cwd = Path(cwd)
    if depth > max_depth:
        error_msg = f"get_root() could not find {target_path} within {depth} parent directories"
        log.critical(error_msg)
        raise ValueError(error_msg)
    path_file_anchor = cwd / target_path
    return cwd if path_file_anchor.exists() else get_root(target_path, cwd.parent, depth=depth + 1, max_depth=max_depth)


def change_dir(target_path: Path | str, show_info=False) -> None:
    """Change the current working directory.
    Args:
        target_path (Path or str): Target execution path. e.g.: 'my-cloned-repo'
        show_info (bool, optional): Show info about the change of execution path. Defaults to False.
    """
    target_path = Path(target_path)
    current_path = Path.cwd()
    if current_path != target_path:
        os.chdir(target_path)
        if show_info:
            log.info(f"Working Path changed to {Path().absolute()}")


def change_dir_to_parent(target_path: Path | str = None, show_info=False) -> None:
    """Change the current working directory to the parent one. If a target_path is given, the current working is checked
    against it and forced to the parent if not found.
    Used to execute notebooks located in subfolders. For a more general solution, see 'change_dir' function

    Args:
        execution_path (Path or str): Execution path. e.g.: 'my-cloned-repo/'
        show_info (bool, optional): Show info about the change of execution path. Defaults to False.
    """
    if target_path is None:
        target_path = get_root("src")  # default to parent of src folder

    target_path = Path(target_path)
    desired_folder = target_path.stem
    current_folder = Path().absolute().stem
    if current_folder != desired_folder:
        app_dir = Path().absolute() / target_path
        os.chdir(app_dir)
        current_folder = Path().absolute().stem
        log.info(f"Execution Path: {current_folder}\n")
        if show_info:
            log.info(f"Working Path changed to {Path().absolute()}")


def info_os() -> str:
    """Return text with OS version"""
    # log.info('{} {} {}'.format(platform.system(), platform.release(), platform.machine()))
    return f"\n{'OS':<25}{platform.platform()}"


def info_software(modules: list[str] | tuple[str] = None) -> str:
    """Return text with the version of Python and Python modules using pkg_resources
        note: not all modules can be obtained with pkg_resources: e.g: pytorch, mlflow ..
    Args:
        modules (list[str], optional): list of python libraries. Defaults to DEFAULT_MODULES.
    Returns:
        str: text with Python version and modules versions
    Usage Sample:
        modules = ['pandas', 'scikit-learn', 'flask', 'fastapi', 'shap', 'pycaret', 'tensorflow', 'streamlit']
        ds.info_system(hardware=True, modules=modules)

    """
    text = ""
    # Python Environment
    env = getattr(sys, "base_prefix", None) or getattr(sys, "real_prefix", None) or sys.prefix
    text += f"\n{'ENV':<25}{env}"

    python_version = sys.version  # .split('(')[0].strip()
    text += f"\n{'PYTHON':<25}{python_version}"

    if modules is None:
        modules = DEFAULT_MODULES

    for i in modules:
        if i in installed_packages_dict:
            text += f"\n{i:<25}{installed_packages_dict.get(i)}"
        elif i == "pickle":
            text += f"\n{i:<25}{pickle.format_version}"  # type: ignore
        else:
            text += f"\n{i:<25}{'--NO--'}"
    return text


def info_hardware() -> str:
    """Return text with CPU, RAM, and GPU info"""
    # text += ("\n\nHARDWARE:")

    # CPU INFO
    cpu_model = cpuinfo.get_cpu_info().get("brand_raw")
    n_cores = psutil.cpu_count()
    ram = round(psutil.virtual_memory().total / (1024.0**3))

    return f"\n{'MACHINE':<25}{cpu_model} {n_cores} cores - {ram} GB RAM"


def info_system(hardware: bool = True, modules: list[str] = None) -> str:
    """Return a Text with Complete system info:
        - Show CPU & RAM hardware=True (it can take a few seconds)
        - Show OS version.
        - Show versions of Python & Python modules
        - Default list of Python modules:  ['pandas', 'scikit-learn']
    Args:
        hardware (bool, optional): Include hardware info. Defaults to True.
        modules (list[str], optional): list of python libraries. Defaults to None.
    Returns:
        str: Text with complete system info
    """
    text = "\n"
    if hardware:
        text += info_hardware()
    text += info_os()
    text += info_software(modules=modules)
    text += f"\n{'EXECUTION PATH':<25}{Path().absolute()}"
    text += f"\n{'EXECUTION DATE':<25}{time.ctime()}\n"
    return text


def get_memory_usage(obj) -> float:
    """Return a the memory usage in MB
    Args:
        obj: Python object to measure
    Returns:
        float: memory usage in MB
    """
    return round(sys.getsizeof(obj) / 1024**2, 3)
