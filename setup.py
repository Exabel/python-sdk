import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("VERSION", "r", encoding="utf-8") as fh:
    version = fh.read()

_SQLALCHEMY_REQUIREMENTS = [
    "sqlalchemy",
]

_BIGQUERY_REQUIREMENTS = [
    "google-cloud-bigquery",
    "sqlalchemy-bigquery",
]

_SNOWFLAKE_REQUIREMENTS = _SQLALCHEMY_REQUIREMENTS + [
    "snowflake-connector-python",
    "snowflake-sqlalchemy",
]

_ATHENA_REQUIREMENTS = _SQLALCHEMY_REQUIREMENTS + [
    "pyathena",
    "pyarrow",
]

setuptools.setup(
    name="exabel-data-sdk",
    version=version,
    author="Exabel",
    author_email="support@exabel.com",
    description="Python SDK for the Exabel Data API",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Exabel/python-sdk",
    packages=setuptools.find_packages(),
    install_requires=[
        "google-api-core>1.31.3",
        "googleapis-common-protos>=1.56.0",
        "grpcio",
        "openpyxl",
        "pandas",
        "protobuf>=4",
        "requests",
    ],
    extras_require={
        "snowflake": _SNOWFLAKE_REQUIREMENTS,
        "bigquery": _BIGQUERY_REQUIREMENTS,
        "athena": _ATHENA_REQUIREMENTS,
    },
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Financial and Insurance Industry",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
