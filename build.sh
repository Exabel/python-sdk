#!/usr/bin/env bash

# Runs first all the style checks and tests, and if they succeed, builds the files for distribution.

set -e
bash style.sh
bash tests.sh
rm -rf dist
python3 setup.py sdist bdist_wheel
