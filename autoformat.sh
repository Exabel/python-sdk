#!/usr/bin/env bash

# Autoformats all Python files with isort and black.

ruff check --fix exabel_data_sdk
ruff format exabel_data_sdk
