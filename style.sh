#!/usr/bin/env bash

# Runs all the style checks.

set -euf
mypy exabel_data_sdk setup.py
isort --check-only -s exabel_data_sdk/stubs exabel_data_sdk setup.py
black --check --exclude exabel_data_sdk/stubs exabel_data_sdk setup.py
pycodestyle --exclude exabel_data_sdk/stubs exabel_data_sdk setup.py
pylint exabel_data_sdk setup.py
