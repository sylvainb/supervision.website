===============================================
supervision.website
===============================================

.. contents:: Table of Contents
   :depth: 2

Overview
--------

supervision.website is a Python package ...
supervision.website provides utils to supervise websites.

Requirements
------------

    * 

Screenshot
------------

.. image:: https://github.com/sylvainb/supervision.website/raw/master/docs/supervision-website-screenshot.png
   :height: 1039px
   :width: 1026px
   :scale: 70 %
   :alt: Screenshot
   :align: center

Installation
------------

Quickly test ?
~~~~~~~~~~~~~~~~~~~~

Download ``supervision.website`` and use ``virtualenv`` to test the module::

	easy_install virtualenv
	cd supervision.website
	chmod +x test-module.sh
  ./test-module.sh

	source bin/activate
  (supervision.website) python
  >>> import supervision.website

Launch tests with nose <https://nose.readthedocs.org/en/latest/>`_ ::

	(supervision.website) nosetests

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


