#!/usr/bin/env python

from setuptools import setup, find_packages

with open("README_PUBLIC.md", "r") as fh:
    long_description = fh.read()

setup(
    author="Neo Financial",
    author_email="engineering@neofinancial.com",
    python_requires=">=3.6",
    name="humanity_etl",
    version="0.0.1rc5",
    description="Replicate humanity data in databricks",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
    ],
    license="UNLICENSED",
    packages=find_packages(include=["humanity_etl", "humanity_etl.*"]),
    url="https://github.com/neofinancial/humanity_etl",
    include_package_data=True,
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["click", "pandas>=1,<2", "requests", "pyspark", "loguru", "python-dotenv", "typing_extensions"],
    tests_require=["pytest"],
)
