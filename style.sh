#!/usr/bin/env bash

# Runs all the style checks.

set -euf
echo "Running mypy."
mypy exabel_data_sdk

echo "Check style with ruff linter."
ruff check exabel_data_sdk

echo "Check formatting with ruff formatter."
ruff format --check exabel_data_sdk
