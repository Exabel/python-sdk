#!/usr/bin/env bash

# Autoformats all Python files with isort and black.

isort exabel_data_sdk tests setup.py
black exabel_data_sdk tests setup.py
