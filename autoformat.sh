#!/usr/bin/env bash

# Autoformats all Python files with isort and black.

isort -s exabel_data_sdk/stubs exabel_data_sdk setup.py
black --exclude exabel_data_sdk/stubs exabel_data_sdk setup.py
