"""
map of humanity api URLS to fetch
"""
import os

from dotenv import load_dotenv

load_dotenv()

urls = {
    "parent_employees": "https://www.humanity.com/api/v2/employees?disabled=1&access_token={}".format(
        os.environ.get("PAREN_ACCESS_TOKEN")
    ),
    "parent_employees_disabled": "https://www.humanity.com/api/v2/employees?disabled=1&access_token={}".format(
        os.environ.get("PAREN_ACCESS_TOKEN")
    ),
    "parent_positions": "https://www.humanity.com/api/v2/positions?access_token={}".format(
        os.environ.get("PAREN_ACCESS_TOKEN")
    ),
    "gta_employees": "https://www.humanity.com/api/v2/employees?access_token={}".format(
        os.environ.get("GTA_ACCESS_TOKEN")
    ),
    "gta_employees_disabled": "https://www.humanity.com/api/v2/employees?disabled=1&access_token={}".format(
        os.environ.get("GTA_ACCESS_TOKEN")
    ),
    "gta_positions": "https://www.humanity.com/api/v2/positions?access_token={}".format(
        os.environ.get("GTA_ACCESS_TOKEN")
    ),
    "gta_timeclocks": "https://www.humanity.com/api/v2/timeclocks?access_token={}".format(
        os.environ.get("GTA_ACCESS_TOKEN")
    ),
    "gta_shifts": "https://www.humanity.com/api/v2/shifts?access_token={}".format(
        os.environ.get("GTA_ACCESS_TOKEN")
    ),
    "cgy_employees": "https://www.humanity.com/api/v2/employees?access_token={}".format(
        os.environ.get("CGY_ACCESS_TOKEN")
    ),
    "cgy_employees_disabled": "https://www.humanity.com/api/v2/employees?disabled=1&access_token={}".format(
        os.environ.get("CGY_ACCESS_TOKEN")
    ),
    "cgy_positions": "https://www.humanity.com/api/v2/positions?access_token={}".format(
        os.environ.get("CGY_ACCESS_TOKEN")
    ),
    "cgy_timeclocks": "https://www.humanity.com/api/v2/timeclocks?access_token={}".format(
        os.environ.get("CGY_ACCESS_TOKEN")
    ),
    "cgy_shifts": "https://www.humanity.com/api/v2/shifts?access_token={}".format(
        os.environ.get("CGY_ACCESS_TOKEN")
    ),
    "wpg_employees": "https://www.humanity.com/api/v2/employees?access_token={}".format(
        os.environ.get("WPG_ACCESS_TOKEN")
    ),
    "wpg_employees_disabled": "https://www.humanity.com/api/v2/employees?disabled=1&access_token={}".format(
        os.environ.get("WPG_ACCESS_TOKEN")
    ),
    "wpg_positions": "https://www.humanity.com/api/v2/positions?access_token={}".format(
        os.environ.get("WPG_ACCESS_TOKEN")
    ),
    "wpg_timeclocks": "https://www.humanity.com/api/v2/timeclocks?access_token={}".format(
        os.environ.get("WPG_ACCESS_TOKEN")
    ),
    "wpg_shifts": "https://www.humanity.com/api/v2/shifts?access_token={}".format(
        os.environ.get("WPG_ACCESS_TOKEN")
    ),
    "ott_employees": "https://www.humanity.com/api/v2/employees?access_token={}".format(
        os.environ.get("OTT_ACCESS_TOKEN")
    ),
    "ott_employees_disabled": "https://www.humanity.com/api/v2/employees?disabled=1&access_token={}".format(
        os.environ.get("OTT_ACCESS_TOKEN")
    ),
    "ott_positions": "https://www.humanity.com/api/v2/positions?access_token={}".format(
        os.environ.get("OTT_ACCESS_TOKEN")
    ),
    "ott_timeclocks": "https://www.humanity.com/api/v2/timeclocks?access_token={}".format(
        os.environ.get("OTT_ACCESS_TOKEN")
    ),
    "ott_shifts": "https://www.humanity.com/api/v2/shifts?access_token={}".format(
        os.environ.get("OTT_ACCESS_TOKEN")
    ),
    "edm_employees": "https://www.humanity.com/api/v2/employees?access_token={}".format(
        os.environ.get("EDM_ACCESS_TOKEN")
    ),
    "edm_employees_disabled": "https://www.humanity.com/api/v2/employees?disabled=1&access_token={}".format(
        os.environ.get("EDM_ACCESS_TOKEN")
    ),
    "edm_positions": "https://www.humanity.com/api/v2/positions?access_token={}".format(
        os.environ.get("EDM_ACCESS_TOKEN")
    ),
    "edm_timeclocks": "https://www.humanity.com/api/v2/timeclocks?access_token={}".format(
        os.environ.get("EDM_ACCESS_TOKEN")
    ),
    "edm_shifts": "https://www.humanity.com/api/v2/shifts?access_token={}".format(
        os.environ.get("EDM_ACCESS_TOKEN")
    ),
    "mtl_employees": "https://www.humanity.com/api/v2/employees?access_token={}".format(
        os.environ.get("MTL_ACCESS_TOKEN")
    ),
    "mtl_employees_disabled": "https://www.humanity.com/api/v2/employees?disabled=1&access_token={}".format(
        os.environ.get("MTL_ACCESS_TOKEN")
    ),
    "mtl_positions": "https://www.humanity.com/api/v2/positions?access_token={}".format(
        os.environ.get("MTL_ACCESS_TOKEN")
    ),
    "mtl_timeclocks": "https://www.humanity.com/api/v2/timeclocks?access_token={}".format(
        os.environ.get("MTL_ACCESS_TOKEN")
    ),
    "mtl_shifts": "https://www.humanity.com/api/v2/shifts?access_token={}".format(
        os.environ.get("MTL_ACCESS_TOKEN")
    ),

}
