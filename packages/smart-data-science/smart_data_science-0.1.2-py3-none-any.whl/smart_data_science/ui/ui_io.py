"""
- Title:            Utils I/O files for User Interface (streamlit)
- Project/Topic:    Utils Tabular Data. Practical functions for Data Science
- Author/s:         Angel Martinez-Tenor
- Dev Date:         2017 - 2022

- Status:           In progress.

- Acknowledgements. Partially Based on:
    - Personal Repo: https://github.com/angelmtenor/data-science-keras/blob/master/helper_ds.py
"""

# TO IMPROVE: Add functions from other dev


import base64
import os
from pathlib import Path
from zipfile import ZipFile

import pandas as pd
import streamlit as st  # For error messages only
from PIL import Image

from smart_data_science import logger
from smart_data_science.core import io

log = logger.get_logger(__name__)


def save_zip_copy(filepath: str | Path):
    """Save a compressed zipped file of an input file (needed for streamlit downloadable links)
    Args:
        filepath (str|Path): path of the file
    """
    filepath = Path(filepath)
    zip_filepath = filepath.with_suffix(".zip")

    with ZipFile(zip_filepath, mode="w") as zf:
        zf.write(filepath, arcname=filepath.name)


# def save_zip_copy(filepath: str | Path):
#     """Save a compressed zipped file of an input xlsx file (needed for streamlit downloadable links)
#     Args:
#         filepath (str|Path): path of the excel file
#     """
#     filepath = Path(filepath)
#     zip_filepath = filepath.parent / (filepath.stem + ".zip")

#     with ZipFile(zip_filepath, mode="w") as zf:
#         zf.write(filepath, os.path.basename(filepath))


def save_file_and_zip(datafile, filepath: str | Path) -> None:
    """
    Save a datafile uploaded from streamlit to 'filepath' and generates a zipped file (streamlit downloadable)
    Args:
        datafile: datafile uploaded from streamlit (binary)
        filepath (str|Path): path of the file to save
    """
    with open(filepath, "wb") as f:
        f.write(datafile.getbuffer())
    save_zip_copy(filepath)


def generate_download_link(
    filepath: str | Path, force_new_zip: bool = False, caption: str = "Download Excel File"
) -> str:
    """
    Generate a downloadable link of the zipped file of the Excel file (xlsx) file for streamlit
    The compressed zip version is created if nor found or 'force_new_zip'=True
    (direct downloadable links of excel do not work in streamlit at the time of this project)
    Args:
        filepath (str|Path): path of the excel file
        force_new_zip (bool): if True, a new zip file is created even if it already exists
        caption (str): caption of the link
    Returns:
        str: link to download the zipped file
    """
    filepath = Path(filepath)
    # zip_filepath = filepath.split(".xlsx")[0] + ".zip"
    zip_filepath = filepath.parent / (filepath.stem + ".zip")
    if not zip_filepath.exists() or force_new_zip:
        save_zip_copy(filepath)
    with open(zip_filepath, "rb") as f:
        bytes_read = f.read()
        b64 = base64.b64encode(bytes_read).decode()
        href = f"<a href=\"data:file/zip;base64,{b64}\" download='{os.path.basename(filepath)}.zip'> {caption} </a>"
    return href


def read_excel_file(filepath: str | Path, sheet_name: str = None) -> pd.DataFrame:
    """
    Read a sheet from excel file (to be uploaded to streamlit UI)
    Args:
        filepath (str|Path): path of the excel file
        sheet_name (str): name of the sheet to read (optional)
    Returns:
        pd.DataFrame: frame read from the excel file
    """
    ef = pd.ExcelFile(filepath)
    if sheet_name:
        if sheet_name not in ef.sheet_names:
            throw_error_in_UI(f"Excel file with sheet '{sheet_name}' not found")
    df = ef.parse(sheet_name, usecols="A:AF")
    df = df.drop_duplicates()
    return df


def frame_to_excel_and_zip(df: pd.DataFrame, filepath: str | Path, sheet_name: str = "Exported Data") -> None:
    """
    Export the dataframe 'df' to a formatted excel file 'filepath' and generate a  zipped file (streamlit downloadable)
    Excel Style guide used to customize the format: https://xlsxwriter.readthedocs.io/index.html
    Args:
        df: The dataframe to export to excel
        filepath (str|Path): path of the excel file
        sheet_name (str): name of the sheet to read (optional)
    """
    writer = pd.ExcelWriter(filepath, engine="xlsxwriter")  # pylint: disable=abstract-class-instantiated
    df.to_excel(writer, sheet_name=sheet_name)  # needed for custom header
    workbook = writer.book
    all_format = workbook.add_format({"font_color": "#808080", "text_wrap": True, "valign": "top"})
    worksheet = writer.sheets[sheet_name]
    worksheet.set_column("A:Z", 30, all_format)
    worksheet.autofilter("A1:Z1")

    # header
    header_format = workbook.add_format(
        {"bold": True, "font_color": "black", "text_wrap": False, "valign": "top", "border": 1, "fg_color": "#B7C4DD"}
    )  # 'fg_color': '#D7E4BC'
    # Header
    for col_num, value in enumerate(df.columns.values):
        worksheet.write(0, col_num + 1, value, header_format)

    # Save Excel & Zip files (applied to all data & output excel files)
    writer.save()
    save_zip_copy(filepath)


def save_excel_and_generate_downloadable_link(
    df: pd.DataFrame,
    filepath: str | Path,
    sheet_name: str,
):
    """Save Excel & Zip Results. Generate & display a link to download the zip file"""

    filepath = Path(filepath)
    frame_to_excel_and_zip(df, filepath, sheet_name)
    link_zip = generate_download_link(filepath, caption="**DOWNLOAD THE RESULTS (Excel)**")
    st.write("")
    st.markdown(link_zip, unsafe_allow_html=True)


@st.cache
def frame_to_csv_cache(df: pd.DataFrame) -> str:
    """Export to csv for the download option
    Args:
        df: The dataframe to export to csv
    Returns:
        str: The csv file in string format
    """
    return df.to_csv().encode("utf-8")


def download_to_csv_option(df: pd.DataFrame, file_name: str | Path, label: str = None) -> None:
    """Create a csv file and a download button from dataframe
    Args:
        df: The dataframe to export to csv
        file_name: The filename of the csv file
        label: The label of the download button (optional)
    """
    csv = frame_to_csv_cache(df)
    st.download_button(
        label=label,
        data=csv,
        file_name=str(file_name),
        mime="text/csv",
    )


def throw_error_in_UI(msg: str = None) -> None:
    """Show an error msg in the UI with the input message and stop the execution
    Args:
        msg: message to be displayed in the UI
    """
    if not msg:
        msg = ""
    st.error(msg)
    st.stop()


@st.cache_data
def load_image(path: str | Path) -> Image:
    """Load a image from the given path
    Args:
        path: The path of the image to load
    Returns:
        Image: Logo as an Image
    """
    path = Path(path)
    if not path.exists():
        st.error(f"Image not found: {path}")
        return None
    return Image.open(path)


def show_image(path: str | Path, caption: str = None) -> None:
    """Load & Show an image in the UI
    Args:
        filename: The filename of the image to load
        caption: The caption to show above the image (optional)
    """
    image = load_image(path)
    try:
        st.image(image, caption=caption)
    except ValueError:
        error_msg = "The Image is too large to be shown"
        # log.error(error_msg)
        st.error(error_msg)


def save_results_and_generate_downloadable_link(  # TO IMPROVE - UPDATE
    df,
    filepath,
    sheet_name,
    secondary_df=None,
    secondary_sheet_name=None,
    df_3=None,
    sheet_name_3=None,
    df_4=None,
    sheet_name_4=None,
):
    """Save Excel & Zip Results. Generate & display a link to download the zip file"""

    # filepath = OUTPUT_PATH / f"{current_date_string} {label}.xlsx"
    filepath = Path(filepath)
    io.frame_to_excel_and_zip(
        df, filepath, sheet_name, secondary_df, secondary_sheet_name, df_3, sheet_name_3, df_4, sheet_name_4
    )
    link_zip = io.generate_download_link(filepath, caption="**DOWNLOAD THE RESULTS (Excel)**")
    st.write("")
    st.markdown(link_zip, unsafe_allow_html=True)
