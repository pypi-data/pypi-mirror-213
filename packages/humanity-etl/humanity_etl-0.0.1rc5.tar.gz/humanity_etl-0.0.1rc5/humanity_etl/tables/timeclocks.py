"""list"""

from pandas import DataFrame as PandasDF
import pandas as pd

from humanity_etl.libs.transform import (
    framer,
    get_data_for_all_urls,
    map_data_to_dataframe,
    merge_related_dfs,
    merger,
)
from humanity_etl.libs.dbg import print_dataframe_head, write_dataframe_to_csv
from humanity_etl.libs.cnst import urls


@write_dataframe_to_csv("timeclocks")
@print_dataframe_head
def timeclocks() -> PandasDF:
    """timeclocks dataframe"""

    all_data = get_data_for_all_urls(urls)
    frames = map_data_to_dataframe(all_data)
    frames = merge_related_dfs(frames)

    """
    Final working dataframes
    TODO: The following code is suboptimal. Fix it.
    """

    """
    PARENT
    """
    # Employees
    parent_employees_df = frames["parent_employees"][["name", "email"]].copy()
    parent_employees_df["emp_email"] = parent_employees_df["email"].str[1:]
    parent_employees_df2 = parent_employees_df.drop(
        "email", axis=1
    )  # .rename(columns={'id':'employee_id'})

    # Positions: TODO: @Tony Is this necessary
    # parent_positions_df = parent_positions[['id', 'name', 'location.id', 'location.name']].copy()
    # parent_positions_df.rename(columns={'name':'position', 'location.name':'loc_name'}, inplace=True)

    """
    Locations
    """
    gta_timeclocks_df, gta_employees_df, gta_positions_df, gta_shifts_df = framer(
        frames["gta_timeclocks"],
        frames["gta_employees"],
        frames["gta_positions"],
        frames["gta_shifts"],
    )
    cgy_timeclocks_df, cgy_employees_df, cgy_positions_df, cgy_shifts_df = framer(
        frames["cgy_timeclocks"],
        frames["cgy_employees"],
        frames["cgy_positions"],
        frames["cgy_shifts"],
    )
    wpg_timeclocks_df, wpg_employees_df, wpg_positions_df, wpg_shifts_df = framer(
        frames["wpg_timeclocks"],
        frames["wpg_employees"],
        frames["wpg_positions"],
        frames["wpg_shifts"],
    )
    ott_timeclocks_df, ott_employees_df, ott_positions_df, ott_shifts_df = framer(
        frames["ott_timeclocks"],
        frames["ott_employees"],
        frames["ott_positions"],
        frames["ott_shifts"],
    )
    edm_timeclocks_df, edm_employees_df, edm_positions_df, edm_shifts_df = framer(
        frames["edm_timeclocks"],
        frames["edm_employees"],
        frames["edm_positions"],
        frames["edm_shifts"],
    )
    gta_timeclocks_df, gta_employees_df, gta_positions_df, gta_shifts_df = framer(
        frames["gta_timeclocks"],
        frames["gta_employees"],
        frames["gta_positions"],
        frames["gta_shifts"],
    )
    mtl_timeclocks_df, mtl_employees_df, mtl_positions_df, mtl_shifts_df = framer(
        frames["mtl_timeclocks"],
        frames["mtl_employees"],
        frames["mtl_positions"],
        frames["mtl_shifts"],
    )

    """
    Join regions dataframe into regions output, then into final humanity dataframe
    """
    gta_program_df = merger(
        gta_timeclocks_df, gta_positions_df, gta_employees_df, gta_shifts_df, "GTA"
    )
    cgy_program_df = merger(
        cgy_timeclocks_df, cgy_positions_df, cgy_employees_df, cgy_shifts_df, "CGY"
    )
    wpg_program_df = merger(
        wpg_timeclocks_df, wpg_positions_df, wpg_employees_df, wpg_shifts_df, "WPG"
    )
    ott_program_df = merger(
        ott_timeclocks_df, ott_positions_df, ott_employees_df, ott_shifts_df, "OTT"
    )
    edm_program_df = merger(
        edm_timeclocks_df, edm_positions_df, edm_employees_df, edm_shifts_df, "EDM"
    )
    mtl_program_df = merger(
        mtl_timeclocks_df, mtl_positions_df, mtl_employees_df, mtl_shifts_df, "EDM"
    )

    # "UNION" all region dataframes
    humanity_df = pd.concat(
        [gta_program_df, cgy_program_df, wpg_program_df, edm_program_df, ott_program_df, mtl_program_df]
    )
    humanity_final_df = humanity_df.merge(
        parent_employees_df2, left_on="employee_name", right_on="name", how="left"
    )

    # "Coalesce" emails to fill in blanks
    humanity_final_df["employee_email"] = humanity_final_df.email.combine_first(
        humanity_final_df.emp_email
    )

    humanity_final = humanity_final_df[
        [
            "date",
            "employee_name",
            "employee_email",
            "location_name",
            "length_total_hours",
            "region",
        ]
    ].copy()
    humanity_final["length_total_hours"] = pd.to_numeric(
        humanity_final["length_total_hours"]
    )

    return humanity_final
