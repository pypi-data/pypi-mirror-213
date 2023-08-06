"""campaign_list_history"""

from typing import Dict, Any, List
import pandas as pd
from pandas import DataFrame as PandasDF

from iterable_etl.libs.network import get_data
from iterable_etl.libs.dbg import print_dataframe_head, write_dataframe_to_csv
from iterable_etl.libs.cnst import urls, get_headers


def get_campaign_data(api_url: str, headers: Dict[str, str]) -> List[Dict[str, Any]]:
    """Make a GET request to the Iterable API and return a dictionary of campaigns data."""
    data = get_data(api_url, headers)
    return data["campaigns"]


def explode_list_ids(data: List[Dict[str, Any]]) -> PandasDF:
    """flatten listIds and associate with campaignId"""
    df_data = []
    for campaign in data:
        if "listIds" in campaign:
            for list_id in campaign["listIds"]:
                df_data.append(
                    {
                        "campaignId": campaign["id"],
                        "listId": list_id,
                        "updatedAt": campaign["updatedAt"],
                    }
                )

    df = pd.DataFrame(df_data)

    return df


@write_dataframe_to_csv("campaign_list_history")
@print_dataframe_head
def campaign_list_history_df() -> PandasDF:
    """campaign_history_dataframe"""
    data = get_campaign_data(urls["campaigns"], get_headers())
    df = explode_list_ids(data)

    return df
