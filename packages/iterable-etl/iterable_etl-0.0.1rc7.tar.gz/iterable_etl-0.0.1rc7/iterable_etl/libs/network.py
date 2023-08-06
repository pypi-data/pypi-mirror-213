"""network"""

from typing import Dict, Any
import requests
from urllib.parse import urlparse, urlunparse

from iterable_etl.libs.dbg import dbg


def remove_query_params(url):
    """shorten url for printing"""
    parsed_url = urlparse(url)
    new_url = parsed_url._replace(query=None)
    cleaned_url = urlunparse(new_url)
    return cleaned_url


def get_data(api_url: str, headers: Dict[str, str], json=True) -> Dict[str, Any]:
    """Make a GET request to the Iterable API and return the data."""
    dbg_url = remove_query_params(api_url)
    dbg("Making request to {api_url}", api_url=dbg_url)
    response = requests.get(api_url, headers=headers, timeout=60)
    dbg("{api_url} response code {code}", api_url=dbg_url, code=response.status_code)
    response.raise_for_status()
    if json == False:
        data = response.text
        return data
    data = response.json()
    return data
