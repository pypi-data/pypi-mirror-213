#!/usr/bin/env python

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

setup(
    author="Andrew Moss",
    author_email="andrew.moss@neofinancial.com",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="Google sheet to dataframe",
    install_requires=[
        "google-api-python-client",
        "google-auth-httplib2",
        "google-auth-oauthlib",
        "pandas",
        "python-dotenv",
        "typing_extensions",
    ],
    license="MIT license",
    long_description=readme,
    include_package_data=True,
    keywords="sheet_df",
    name="sheet_df",
    packages=find_packages(include=["sheet_df", "sheet_df.*"]),
    test_suite="tests",
    tests_require=["pytest"],
    url="https://github.com/neo-andrew-moss/sheet_df",
    version="0.0.1rc2",
    zip_safe=False,
)
