"""campaign_metrics"""
import time
from typing import Dict
import pandas as pd
from pandas import DataFrame as PandasDF

from iterable_etl.libs.network import get_data
from iterable_etl.libs.transform import clean_column_headers, csv_to_dataframe
from iterable_etl.libs.dbg import print_dataframe_head, write_dataframe_to_csv
from iterable_etl.libs.cnst import get_todays_date, urls, get_headers


def get_campaign_ids(api_url: str, headers: Dict[str, str]) -> list[int]:
    """Make a GET request to the Iterable API and return a list of campaign ids."""
    data = get_data(api_url, headers)
    campaign_ids = [campaign["id"] for campaign in data["campaigns"]]
    return campaign_ids


@write_dataframe_to_csv("campaign_metrics")
@print_dataframe_head
def campaign_metrics_df() -> PandasDF:
    """campaign_metrics dataframe"""

    campaign_metrics_url = urls["metrics"]

    start_date = "2021-06-01"
    end_date = get_todays_date()

    batch_size = 300

    df = pd.DataFrame()

    campaign_ids = get_campaign_ids(urls["campaigns"], get_headers())

    campaign_id_batches = [
        campaign_ids[i : i + batch_size]
        for i in range(0, len(campaign_ids), batch_size)
    ]

    for campaign_id_batch in campaign_id_batches:
        campaign_id_params = "&".join(
            [f"campaignId={campaign_id}" for campaign_id in campaign_id_batch]
        )

        url = f"{campaign_metrics_url}?{campaign_id_params}&startDateTime={start_date}&endDateTime={end_date}"

        response_text = get_data(url, get_headers(), json=False)

        time.sleep(11)

        data = csv_to_dataframe(response_text)
        df = pd.concat([df, data])

    df = clean_column_headers(df)
    return df
