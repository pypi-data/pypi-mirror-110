####################################################
Dynata Reporting & Analytics API
####################################################

.. image:: https://marketsight.readthedocs.io/en/latest/_static/marketsight-logo.png
  :alt: Dynata Reporting & Analytics
  :align: right
  :width: 120
  :height: 120
  :target: https://marketsight.readthedocs.io/en/latest.html

**Python bindings for the Dynata Reporting & Analytics (MarketSight) API**


The **MarketSight Client API** library provides Python bindings for the
Dynata Reporting & Analytics API, providing a Pythonic interface for
interacting with the underlying platform's RESTful APIs.

.. contents::
  :depth: 3
  :backlinks: entry

------------------------

*****************
Installation
*****************

To install **MarketSight API Client**, just execute:

  .. code:: bash

   $ pip install marketsight

Dependencies
=================

* `Validator-Collection v.1.5.0 <https://github.com/insightindustry/validator-collection>`_ or higher
* `simplejson v.3.0 <https://github.com/simplejson/simplejson>`_ or higher
* `bravado v.10.6.0 <https://github.com/Yelp/bravado/>`_ or higher
* `dpath v.2.0.1 <https://github.com/akesterson/dpath-python>`_ or higher

-----------------------------------

*********************************
Key MarketSight API Features
*********************************

* Ability to manage your Account settings within the Dynata Reporting
  & Analytics platform.
* Ability to manage data within the Dynata Reporting & Analytics platform.
* Ability to perform high-end statistical analyses on your data in the
  Dynata Reporting & Analytics platform.
* Ability to produce interactive visualizations of your data and insights.
* Ability to produce and share interactive dashboards to deliver your insights
  to downstream users.
* Ability to embed or otherwise integrate the MarketSight platform into your
  applications.

-----------------------

**********************************
Hello, World and Basic Usage
**********************************

1. Initialize the Library
==========================================


.. code-block:: bash


   # Import the MarketSight API Client
   import marketsight

   # Call the "client" factory function.
   api = marketsight.client("https://application.marketsight.com/api/v1/swagger/public.json")


2. Authorize Against the API
================================


.. code-block:: bash

    # Initialize the MarketSight API Client.
    api = marketsight.client("https://application.marketsight.com/api/v1/swagger/public.json")

    # Connect your instance to the API and authorize as a partner.
    api.connect(
        client_id = "MY CLIENT ID GOES HERE",
        client_secret = "MY CLIENT SECRET GOES HERE"
    )

3. Call the API
=====================

Execute API calls to perform operations, for example:


.. code-block:: bash

  # Retrieve an Account
  account = api.Accounts.retrieve(account_id = "MY ACCOUNT ID GOES HERE")

  # Retrieve a User
  user = api.Users.retrieve(user_id = "MY USER ID GOES HERE")

  # Retrieve a Dataset's Meta-data
  dataset = api.Datasets.retrieve(dataset_id = "MY DATASET ID GOES HERE")

---------------

*********************
Questions and Issues
*********************

You can ask questions and report issues on the project's
`Github Issues Page <https://github.com/dynata/msight-csl/issues>`_


--------------------

**********************
License
**********************

**MarketSight Core** is made available under an
`MIT License <https://marketsight.readthedocs.org/en/latest/license.html>`_.
