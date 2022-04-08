# Exabel Python SDK

A Python SDK which provides easy access to Exabel APIs.

## Installation

```
pip install exabel-data-sdk
```

or download from [PyPI](https://pypi.org/project/exabel-data-sdk/).

The SDK requires Python 3.6 or later.

> **Note:**
Python 3.6 is deprecated as of version 3.3.0 of the Exabel Python SDK. Support will be removed in a future release. Please upgrade to Python 3.7 or a newer release of Python.

## Getting started

To use the SDK againts Exabel APIs, you need an API key provided by Exabel.

The Exabel Export API can be used by authenticating with username and password, [Export script](https://doc.exabel.com/api/export/script.html)

Scripts for [operations against the API](https://github.com/Exabel/python-sdk/tree/main/exabel_data_sdk/scripts).

[Examples of usage](https://github.com/Exabel/python-sdk/tree/main/exabel_data_sdk/examples).

## Exabel API documentation

### Data API
The Exabel Data API can be used to upload custom data to the Exabel platform. Custom data may include entities, relationships and time series.

Developer guide: https://help.exabel.com/docs/data-api

### Export API
The Exabel Export API can be used to export dashboards and signals from the Exabel Platform

Developer guide: https://doc.exabel.com/api/export/index.html

### Analytics API
The Exabel Analytics API can be used to manage derived signals and prediction models on the Exabel Platform.

Develper guide: https://help.exabel.com/docs/analytics-api

### Management API
The Exabel Management API can be used to manage the library on the Exabel Platform.

Developer guide: https://help.exabel.com/docs/management-api
