"""network"""

from typing import Dict, Any
import requests

from iterable_etl.libs.dbg import dbg


def get_data(api_url: str, headers: Dict[str, str], json=True) -> Dict[str, Any]:
    """Make a GET request to the Iterable API and return the data."""
    dbg("Making request to {api_url}", api_url=api_url)
    response = requests.get(api_url, headers=headers, timeout=60)
    dbg("{api_url} response code {code}", api_url=api_url, code=response.status_code)
    response.raise_for_status()
    if json == False:
        data = response.text
        return data
    data = response.json()
    return data
