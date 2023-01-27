# Exabel Python SDK

A Python SDK which provides easy access to Exabel APIs.

## Installation

```
pip install exabel-data-sdk
```

or download from [PyPI](https://pypi.org/project/exabel-data-sdk/).

The SDK requires Python 3.7 or later.

### Installation with SQL data source support

For installation with support for exporting data from a various SQL based data sources, add the data source as a pip extra in brackets after the package name:

```sh
# Install the Exabel Python SDK with Snowflake support:
pip install exabel-data-sdk[snowflake]

# Or install multiple data sources at the same time:
pip install exabel-data-sdk[snowflake,bigquery,athena]
```

Supported data sources are:
* Snowflake: `snowflake`
* Google BigQuery: `bigquery`
* AWS Athena: `athena`

## Getting started

To use the SDK against the Data API, Analytics API or Management API, you need an API key provided by Exabel.

The Exabel Export API can be used by authenticating with username and password.
The first time you run the script a web browser window is opened where you are asked to provide username and password. The script stores an access token in ``~/.exabel``, so you will not be asked again
until the token expires.

[Export API Developer guide](https://help.exabel.com/docs/exporting-via-exabel-sdk)

[Examples of usage](https://github.com/Exabel/python-sdk/tree/main/exabel_data_sdk/examples).

## Exabel API documentation

### Data API
The Exabel Data API can be used to upload custom data to the Exabel platform. Custom data may include entities, relationships and time series.

[Data API Developer guide](https://help.exabel.com/docs/data-api)

### Export API
The Exabel Export API can be used to export dashboards and signals from the Exabel Platform.

[Export API Developer guide](https://help.exabel.com/docs/exporting-via-exabel-sdk)

### Analytics API
The Exabel Analytics API can be used to manage derived signals and prediction models on the Exabel Platform.

[Analytics API Developer guide](https://help.exabel.com/docs/analytics-api)

### Management API
The Exabel Management API can be used to manage the library on the Exabel Platform.

[Management API Developer guide](https://help.exabel.com/docs/management-api)
