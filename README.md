# Exabel Python SDK

A Python SDK which provides easy access to Exabel APIs.

## Installation

```shell
pip install exabel
```

or download from [PyPI](https://pypi.org/project/exabel).

The SDK requires Python 3.10 or later.

### Installation with SQL data source support

For installation with support for exporting data from a various SQL based data sources, add the data source as a pip extra in brackets after the package name:

```shell
# Install the Exabel Python SDK with Snowflake support:
pip install exabel[snowflake]

# Or install multiple data sources at the same time:
pip install exabel[snowflake,bigquery,athena]
```

Supported data sources are:

* Snowflake: `snowflake`
* Google BigQuery: `bigquery`
* AWS Athena: `athena`

## Getting started

To use the SDK against, you need an API key or personal access token. THis can be found in the Exabel app.

[Export API Developer guide](https://help.exabel.com/docs/exporting-via-exabel-sdk)

[Examples of usage](https://github.com/Exabel/python-sdk/tree/main/exabel/examples).

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

## Protocols

For efficiency, the SDK uses gRPC when communicating with the Data API, Analytics API,
and Management API. The Export API is only available as a REST API.

gRPC uses HTTPS on server port 21443, while REST uses HTTPS on server port 443.
