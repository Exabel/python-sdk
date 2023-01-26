#!/usr/bin/env bash

# Runs all the style checks.

set -euf
echo "Running mypy."
mypy exabel_data_sdk setup.py

echo "Check imports"
isort --check-only -s exabel_data_sdk/stubs exabel_data_sdk setup.py

echo "Check formatting"
black --check --exclude exabel_data_sdk/stubs exabel_data_sdk setup.py

echo "Running pylint."
pylint exabel_data_sdk setup.py
