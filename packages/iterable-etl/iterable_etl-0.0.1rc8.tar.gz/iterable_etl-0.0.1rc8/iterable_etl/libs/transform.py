"""transform"""

from typing import Dict, Any
import io
import re

import pandas as pd
from pandas import DataFrame as PandasDF


def json_to_dataframe(data: Dict[str, Any]) -> PandasDF:
    """Convert the JSON data to a Pandas DataFrame."""
    df = pd.json_normalize(data)
    return df


def csv_to_dataframe(data: str) -> PandasDF:
    """Convert the CSV data to a Pandas DataFrame."""
    df = pd.read_csv(io.StringIO(data))
    return df


def clean_column_headers(df: PandasDF) -> PandasDF:
    """Remove special characters and spaces, columns as camelCase."""
    clean_headers = []
    for column in df.columns:
        clean_header = re.sub(r"[^a-zA-Z0-9_ ]", "", column.lower())
        words = clean_header.split()
        clean_header = "".join(word.title() for word in words)
        clean_headers.append(clean_header)

    # Assign the clean headers to the DataFrame
    df.columns = clean_headers

    return df
