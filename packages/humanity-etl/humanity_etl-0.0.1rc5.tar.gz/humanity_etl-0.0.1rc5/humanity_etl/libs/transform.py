"""transform"""

from typing import Dict, Any

import pandas as pd
from pandas import DataFrame as PandasDF

from humanity_etl.libs.network import get_data


def check_pandas_version() -> None:
    """
    pandas v2 does not work well with our pyspark version
    """
    pandas_version = pd.__version__
    major_version = int(pandas_version.split(".")[0])

    if major_version != 1:
        raise ValueError(
            f"Unsupported pandas version: {pandas_version}. Only version 1.X.X is allowed."
        )

    print("Pandas version is compatible.")


def get_data_for_all_urls(urls: Dict[str, str]) -> Dict[str, Any]:
    """
    url dict -> json dict

    Map the dict of [key:urls] to a dictionary of [key:json] values
    this is where the api fetched take place. It will take the longest to run
    TODO: Add in a HTTP validation layer"""
    data = {}
    for key, url in urls.items():
        data[key] = get_data(url, headers={"accept": "application/json"})
    return data


def map_data_to_dataframe(data: Dict[str, Any]) -> Dict[str, PandasDF]:
    """
    json dict -> dataframe dict

    map a dictionary of [key:json] to [key:dataframe]
    """
    dfs = {}
    for key, value in data.items():
        dfs[key] = pd.DataFrame.from_records(value["data"])
        dfs[key] = normalize(dfs[key])
    return dfs


def normalize(frame: PandasDF) -> PandasDF:
    """
    normalize

    Apply the normalization impl to the target col
    TODO: This isnt super great
    """
    if "schedule" in frame:
        frame["schedule_id"] = frame.apply(get_normalized("schedule", "id"), axis=1)
    if "employee" in frame:
        frame["employee_id"] = frame.apply(get_normalized("employee", "id"), axis=1)
        frame["employee_name"] = frame.apply(get_normalized("employee", "name"), axis=1)
    if "length" in frame:
        frame["length_total_hours"] = frame.apply(
            get_normalized("length", "total_hours"), axis=1
        )
    if "location" in frame:
        frame["location_id"] = frame.apply(get_normalized("location", "id"), axis=1)
        frame["location_name"] = frame.apply(get_normalized("location", "name"), axis=1)
    return frame


def get_normalized(target_col, target_dict_key):
    """
    Normalize

    Explode a dataframe dictionary row value into a new column
    This is curried to allow for vectorized application"""

    # This is called via .apply
    def change(row):
        try:
            schedule = row[target_col]
            if schedule is not None and schedule != {}:
                return schedule[target_dict_key]
            else:
                return None
        except:
            return None

    return change


def merge_related_dfs(df_dict: Dict[str, PandasDF]) -> Dict[str, PandasDF]:
    """
    Union the employees and disabled employess associated dataframes
    """
    merged_dfs = {}
    for key, df in df_dict.items():
        if key.endswith("_employees") or key.endswith("_employees_disabled"):
            # Get the prefix of the key
            prefix = (
                key.rsplit("_", 1)[0]
                if key.endswith("_employees")
                else key.rsplit("_", 2)[0]
            )

            # If the merged df already exists, append to it, else create a new one
            if prefix + "_employees" in merged_dfs:
                merged_dfs[prefix + "_employees"] = pd.concat(
                    [merged_dfs[prefix + "_employees"], df]
                )
            else:
                merged_dfs[prefix + "_employees"] = df
        else:
            merged_dfs[key] = df
    return merged_dfs


def merger(
    timeclocks_df: PandasDF,
    positions_df: PandasDF,
    employees_df: PandasDF,
    shifts_df: PandasDF,
    region: str,
) -> PandasDF:
    """
    Join regions dataframe into regions output, then into final humanity dataframe
    """
    program_df = (
        timeclocks_df.merge(
            employees_df, left_on="employee_id", right_on="employee_id", how="left"
        )
        .merge(positions_df, left_on="position_id", right_on="id", how="left")
        .merge(shifts_df, left_on="shift_id", right_on="id", how="left")
    )
    final_df = program_df[
        [
            "date",
            "employee_name",
            "email",
            "location_name",
            "rate",
            "length_total_hours",
        ]
    ].copy()
    final_df["region"] = region
    return final_df


def framer(
    timeclocks_df: PandasDF,
    employees_df: PandasDF,
    positions_df: PandasDF,
    shifts_df: PandasDF,
) -> list[PandasDF]:
    """
    Final working dataframes

    This is some data wrangling to the regional dataframes"""

    """
    EDM
    """
    # Timeclocks
    _timeclocks_df = timeclocks_df[
        [
            "employee_id",
            "employee_name",
            "created",
            "schedule_id",
            "length_total_hours",
            "shift",
        ]
    ].copy()
    _timeclocks_df.rename(
        columns={"shift": "shift_id", "schedule_id": "position_id"}, inplace=True
    )
    _timeclocks_df["date"] = pd.to_datetime(_timeclocks_df["created"], unit="s").dt.date
    _timeclocks_df["position_id"] = (
        _timeclocks_df["position_id"].fillna(0).astype("int")
    )
    _timeclocks_df.drop("created", axis=1, inplace=True)

    # Employees
    _employees_df = employees_df[["id", "email"]].copy()
    _employees_df.rename(columns={"id": "employee_id"}, inplace=True)

    # Positions
    _positions_df = positions_df[["id", "name", "location_id", "location_name"]].copy()
    _positions_df.rename(columns={"name": "position"}, inplace=True)

    # Shifts
    _shifts_df = shifts_df[["id", "employees"]].copy()
    _shifts_df["e_name"] = _shifts_df["employees"].str[0].str.get("name")
    _shifts_df["rate"] = _shifts_df["employees"].str[0].str.get("wage")
    _shifts_df.drop("employees", axis=1, inplace=True)

    return [_timeclocks_df, _employees_df, _positions_df, _shifts_df]
