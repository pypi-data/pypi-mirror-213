# `iterable_etl`

> Replicate data from iterable in databricks

[![pypi](https://img.shields.io/pypi/v/iterable_etl?style=for-the-badge)](https://pypi.org/project/iterable_etl/)

### CLI

```bash
python -m iterable_etl --table <table-name>
```

where <table-name> is one of the following: `campaign_history`, `campaign_metrics`, `campaign_list_history`, `list`, or `ALL`.

### API

```python
from iterable_etl.tables.campaign_history import campaign_history_df
from iterable_etl.tables.campaign_metrics import campaign_metrics_df
from iterable_etl.tables.list import list_df
from iterable_etl.tables.campaign_list_history import campaign_list_history_df

campaign_history_df()
campaign_metrics_df()
list_df()
campaign_list_history_df()
```

Further configs are set via environment variables:

- `ITERABLE_KEY`: API access
- `APP_ENV`: <development/production> - debug mode
- `SAMPLE_OUTPUT`: <True/False> - Save dataframes to csv

## DEV

### Create venv

```bash
python -m venv env
```

### Activate venv

- unix

```bash
source env/bin/activate
```

- windows

```bash
env\Scripts\activate.bat
```

### Install Packages

```bash
pip install -r requirements.txt
```

## Test

```bash
make test
```

## Format

```bash
make format
```

```bash
make lint
```
