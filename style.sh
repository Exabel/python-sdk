#!/usr/bin/env bash

# Runs all the style checks.

set -euf
echo "Running mypy."
mypy exabel

echo "Check style with ruff linter."
ruff check exabel

echo "Check formatting with ruff formatter."
ruff format --check exabel
