=============================
Nobinobi Core
=============================

.. image:: https://badge.fury.io/py/nobinobi-core.svg
    :target: https://badge.fury.io/py/nobinobi-core

.. image:: https://travis-ci.org/prolibre-ch/nobinobi-core.svg?branch=master
    :target: https://travis-ci.org/prolibre-ch/nobinobi-core

.. image:: https://codecov.io/gh/prolibre-ch/nobinobi-core/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/prolibre-ch/nobinobi-core

.. image:: https://pyup.io/repos/github/prolibre-ch/nobinobi-core/shield.svg
     :target: https://pyup.io/repos/github/prolibre-ch/nobinobi-core/
     :alt: Updates

.. image:: https://pyup.io/repos/github/prolibre-ch/nobinobi-core/python-3-shield.svg
     :target: https://pyup.io/repos/github/prolibre-ch/nobinobi-core/
     :alt: Python 3

Core for application Nobinobi

Documentation
-------------

The full documentation is at https://nobinobi-core.readthedocs.io.

Quickstart
----------

Install Nobinobi Core::

    pip install nobinobi-core

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'nobinobi_core.apps.NobinobiCoreConfig',
        ...
    )

Add Nobinobi Core's URL patterns:

.. code-block:: python

    from nobinobi_core import urls as nobinobi_core_urls


    urlpatterns = [
        ...
        path('', include(nobinobi_core_urls)),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox


Development commands
---------------------

::

    pip install -r requirements_dev.txt
    invoke -l


Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
