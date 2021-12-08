import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("VERSION", "r", encoding="utf-8") as fh:
    version = fh.read()

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
        'dataclasses == 0.8; python_version <= "3.6"',
        "google-api-core==1.31.2",
        "grpcio",
        "pandas",
        "protobuf",
        "requests",
    ],
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
