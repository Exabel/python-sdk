#!/usr/bin/env bash

mkdir -p tests/exabel
cp -r ./exabel/tests ./tests/exabel/

# Workaround for running tests in sub-package
PYTHON_SITE_PACKAGE=$(pip show exabel|grep Location|cut -f 2 -d ' ')
echo "__path__ = __import__('pkgutil').extend_path(__path__, __name__)" >> ${PYTHON_SITE_PACKAGE}/exabel/__init__.py
echo "__path__ = __import__('pkgutil').extend_path(__path__, __name__)" > tests/__init__.py
echo "__path__ = __import__('pkgutil').extend_path(__path__, __name__)" > tests/exabel/__init__.py

cd ./tests/
pytest ./exabel/tests
