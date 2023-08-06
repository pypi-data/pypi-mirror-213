"""
- Title:            Utils Date & Time. Wrapper on top of Pandas for common Date/Time operations
- Project/Topic:    Utils Tabular Data. Practical functions for Data Science
- Author/s:         Angel Martinez-Tenor
- Dev Date:         2017 - 2022

- Status:           Planning
"""

from __future__ import annotations

import datetime

import pandas as pd

dict_weekday = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}

# Dicts used to parse the text schedules of the custom designation table:
int2weekday = {0: "Mon", 1: "Tue", 2: "Wed", 3: "Thu", 4: "Fri", 5: "Sat", 6: "Sun"}
weekday2int = {v: k for k, v in int2weekday.items()}

months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]
months_short = [i[:3] for i in months]


def next_sunday(input_datetime: datetime.date) -> datetime.date:
    """
    Return a datetime.date object with the next Sunday of the input_datetime
    Args:
        input_datetime (datetime.date): Input date
    Returns:
        datetime.date: Next Sunday to the input date
    """
    return input_datetime + pd.Timedelta(days=6 - input_datetime.weekday())


def date_delta(delta_days: int = -3, base_date: bool = None) -> datetime.date:
    """
    Return a datetime.date object with 'base_date'+'delta_days'. If no 'base_date' is given, the current date is used
    instead
    Args:
        delta_days (int): Number of days to add to the base date
        base_date (datetime.date): Base date
    Returns:
        datetime.date: Date with the delta applied
    """
    if not base_date:
        base_date = pd.Timestamp.today().date()
    offset = pd.Timedelta(days=delta_days)
    return base_date + offset


def fix_timezone(df: pd.DataFrame, time_variables: list) -> pd.DataFrame:
    """
    Return a time naive dataframe with non-existing times in Europe (DST) fixed
    Args:
        df (pd.DataFrame): Input dataframe
        time_variables (list): List of time variables to fix
    Returns:
        pd.DataFrame: Time naive dataframe with non-existing times in Europe (DST)
    """
    df = df.copy()
    if time_variables:
        for col in time_variables:
            df[col] = df[col].dt.tz_localize(tz="Europe/Madrid", nonexistent="shift_forward", ambiguous="NaT")
            df[col] = df[col].dt.tz_localize(tz=None)
            # Note: ambiguous=infer fails with the input files of this project
    else:
        print("Warning: No DateTime Variables sent to utils.fix_timezone")  # Improvement: Set log/warning level
    return df


def parse_schedule(schedule_text: str) -> tuple[list[int], list[int]]:
    """Parse Single schedule text & return two lists of integer ranges: weekdays & hours
    Sample: Sat 2-6   ->  weekday = [5] , hour = [2,3,4,5,6]
    Used to parse custom schedules
    Args:
        schedule_text (str): Text to parse
    Returns:
        tuple[list[int], list[int]]: List of weekdays & list of hours
    """
    schedule_text = schedule_text.strip()
    if " " in schedule_text:
        weekdays, hours = schedule_text.split(" ")
    else:
        weekdays = schedule_text
        hours = "0-23"
    # processing weekday text range
    if "-" in weekdays:
        weekday_start, weekday_end = weekdays.split("-")
        weekday = list(range(weekday2int[weekday_start], weekday2int[weekday_end]))
    else:
        weekday = [weekday2int[weekdays]]  # only one weekday

    # processing hour text range
    if "-" in hours:
        hour_start_str, hour_end_str = hours.split("-")
        hour_start, hour_end = int(hour_start_str), int(hour_end_str)

        if hour_start <= hour_end:
            hour = list(range(hour_start, hour_end + 1))
        else:
            hour = list(range(hour_start, 23))
            hour = hour + list(range(0, hour_end + 1))
    else:
        hour = [hours]  # type: ignore

    return weekday, hour


def expand_date(timeseries: pd.Series) -> pd.DataFrame:
    """
    Expand a datetime series to a dataframe with the following columns:
    - hour : 0 - 23
    - year
    - month: 1 - 12
    - day
    - weekday : 0 Monday - 6 Sunday
    - holiday : 0 - 1 holiday (US Federal Holiday Calendar) (temporarily disabled)
    - workingday : 0 weekend or holiday - 1 workingday  (temporarily disabled)
    Args:
        timeseries (pd.Series): Datetime series to expand
    Returns:
        pd.DataFrame: Expanded dataframe
    """

    assert isinstance(timeseries, pd.core.series.Series), "input must be pandas series"
    assert timeseries.dtypes == "datetime64[ns]", "input must be pandas datetime"

    df = pd.DataFrame()

    df["hour"] = timeseries.dt.hour

    date = timeseries.dt.date  # USFederalHolUSFederalHolidayCalendaridayCalendar
    df["year"] = pd.DatetimeIndex(date).year
    df["month"] = pd.DatetimeIndex(date).month
    df["day"] = pd.DatetimeIndex(date).day
    df["weekday"] = pd.DatetimeIndex(date).weekday

    # holidays = calendar().holidays(start=date.min(), end=date.max())
    # hol = date.astype("datetime64[ns]").isin(holidays)
    # df["holiday"] = hol.values.astype(int)
    # df["workingday"] = ((df["weekday"] < 5) & (df["holiday"] == 0)).astype(int)

    return df


# def strip_string_columns(df): # directly in table_definitions
#     """ Return a dataframe with the string columns stripped from leading or tailing spaces """
#     df = df.copy()
#     df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
#     return df

# ---- Functions not used in production (Former 'datainfo' module) ----
