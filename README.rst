===============================================
supervision.website
===============================================

.. contents:: Table of Contents
   :depth: 2

Overview
--------

Goals : 

    * Monitor HTTP and HTTPS URL, checking for valid HTTP status returned.
    * Compute state for each URL : OK (up), SLOW (slow response), KO (down).
    * Send email on state change (text and HTML report).
    * Use simple text files for data storage, no database necessary.

Configuration available : 

    * URL list to monitor.
    * Request timeout.
    * Slow latency threshold.
    * Valid HTTP status list (global and per URL).
    * SMTP settings (subject, from, to, server).
    * Terms of sending emails : never, always, only on state change. 

System requirements
-------------------

    * bash
    * wget
    * a working SMTP server

Installation
------------

Install in a virtualenv
~~~~~~~~~~~~~~~~~~~~~~~

Download ``supervision.website`` and use ``virtualenv`` to test the module::

    easy_install virtualenv
    cd supervision.website
    chmod +x test-module.sh
    ./install.sh

    source bin/activate
    (supervision.website) python
    >>> import supervision.website

Configuration
~~~~~~~~~~~~~~

Create an edit the configuration file :

    (supervision.website) cd src/supervision/website/
    (supervision.website) cp config.py.sample config.py
    (supervision.website) vi config.py

Add a cron JOB
~~~~~~~~~~~~~~~

Create a file <where-you-want>/supervision_website_cron.sh with the following content (don't forget to adapt <egg-directory>). With this script, you can edit your configuration in config.py at any time, the check_hosts.sh script will be generated at each cron call. 

    #!/bin/bash
    cd <egg-directory>
    source bin/activate
    cd src/supervision/website/utils
    python generate_check_host_sh_script.py
    chmod +x check_hosts.sh
    ./check_hosts.sh
    python generate_reports.py

Change permissions settings for the cron bash script :

    chmod +x <where-you-want>/supervision_website_cron.sh

Edit your personal crontab :

    crontab -e

And and adapt the following lines : 

    # Launch supervision.website script every 10 minutes
    */10 * * * * <where-you-want>/supervision_website_cron.sh >> /tmp/supervision.website.cron.log


Launch tests
~~~~~~~~~~~~

Launch tests with nose <https://nose.readthedocs.org/en/latest/>`_ ::

    (supervision.website) nosetests

Launch code coverage
~~~~~~~~~~~~~~~~~~~~

Launch code coverage::

    (supervision.website) nosetests --with-coverage --cover-inclusive --cover-html --cover-html-dir htmlcov
    And open with a browser htmlcov/index.html

Credits
-------

    * Sylvain Boureliou [sylvainb] - `Bitbucket <https://bitbucket.org/sylvainb/>`_ - `Website <http://www.asilax.fr>`_

Source code
-----------

`Source code <https://github.com/sylvainb/supervision.website>`_ is hosted on Github.

How to contribute and submit a patch ?
--------------------------------------

`Source code <https://github.com/sylvainb/supervision.website>`_ and an `issue tracker <https://github.com/sylvainb/supervision.website/issues>`_ is hosted on Github.


