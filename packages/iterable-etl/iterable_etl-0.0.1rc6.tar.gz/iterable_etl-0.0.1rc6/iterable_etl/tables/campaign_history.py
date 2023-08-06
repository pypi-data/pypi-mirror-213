"""campaign_history_meta"""

from pandas import DataFrame as PandasDF
from typing import Dict, Any

from iterable_etl.libs.network import get_data
from iterable_etl.libs.transform import json_to_dataframe
from iterable_etl.libs.dbg import print_dataframe_head, write_dataframe_to_csv
from iterable_etl.libs.cnst import urls, get_headers


def get_campaign_data(api_url: str, headers: Dict[str, str]) -> Dict[str, Any]:
    """Make a GET request to the Iterable API and return a dictionary of campaigns data."""
    data = get_data(api_url, headers)
    return data["campaigns"]


@write_dataframe_to_csv("campaign_history")
@print_dataframe_head
def campaign_history_df() -> PandasDF:
    """campaign_history_dataframe"""
    data = get_campaign_data(urls["campaigns"], get_headers())
    df = json_to_dataframe(data)
    return df
