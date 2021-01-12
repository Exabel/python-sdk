#!/usr/bin/env bash

# Run all the style checks.

set -e
mypy exabel_data_sdk tests setup.py
isort --check-only exabel_data_sdk tests setup.py
black --check exabel_data_sdk tests setup.py
pycodestyle --exclude exabel_data_sdk/stubs exabel_data_sdk tests setup.py
pylint exabel_data_sdk tests setup.py
