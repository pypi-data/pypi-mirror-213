============
sheet_df
============

Google sheet to dataframe

.. image:: https://img.shields.io/pypi/v/sheet_df?style=for-the-badge
   :target: https://pypi.org/project/sheet_df/

Overview
----------

This Python program connects to the google sheets api and creates a pandas dataframe from the target sheet.

Usage
-----

.. code-block:: python

   df = read_google_sheet_into_dataframe(sheet_id, range_name, credentials_path)

Config
------

You must have `SHEET_ID`` and `RANGE_NAME`` env vars. You will also need a `credentials.json` from google. The `credentials_path`
arg defaults to "credentials.json"

DEV
---

Create venv
~~~~~~~~~~~~

.. code-block:: bash

   python -m venv env

Activate venv
~~~~~~~~~~~~~~~

unix

.. code-block:: bash

   source env/bin/activate

windows

.. code-block:: bash

   env\Scripts\activate.bat

Install Packages
~~~~~~~~~~~~~~~~

.. code-block:: bash

   pip install -r requirements.txt

Test
~~~~~

.. code-block:: bash

   make test

Format
~~~~~~

.. code-block:: bash

   make format

.. code-block:: bash

   make lint
