#!/usr/bin/env bash

# Autoformats all Python files with isort and black.

ruff check --fix exabel
ruff format exabel
