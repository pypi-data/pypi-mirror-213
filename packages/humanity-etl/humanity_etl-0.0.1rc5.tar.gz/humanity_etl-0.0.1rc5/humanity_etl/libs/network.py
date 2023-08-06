"""network"""

import json
from typing import Dict, Any
import requests

from humanity_etl.libs.dbg import dbg


def get_data(api_url: str, headers: Dict[str, str]) -> Dict[str, Any]:
    """Make a GET request to the Humanity API and return the data."""
    dbg("Making request to {api_url}", api_url=api_url)
    response = requests.get(api_url, headers=headers, timeout=20)
    dbg("{api_url} response code {code}", api_url=api_url, code=response.status_code)
    response.raise_for_status()
    data = json.loads(response.text)
    return data
