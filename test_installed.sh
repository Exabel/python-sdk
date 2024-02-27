#!/usr/bin/env bash

mkdir -p tests/exabel_data_sdk
cp -r ./exabel_data_sdk/tests ./tests/exabel_data_sdk/

# Workaround for running tests in sub-package
PYTHON_SITE_PACKAGE=$(pip show exabel_data_sdk|grep Location|cut -f 2 -d ' ')
echo "__path__ = __import__('pkgutil').extend_path(__path__, __name__)" >> ${PYTHON_SITE_PACKAGE}/exabel_data_sdk/__init__.py
echo "__path__ = __import__('pkgutil').extend_path(__path__, __name__)" > tests/__init__.py

cd ./tests/
python -m unittest discover -s ./exabel_data_sdk/tests
