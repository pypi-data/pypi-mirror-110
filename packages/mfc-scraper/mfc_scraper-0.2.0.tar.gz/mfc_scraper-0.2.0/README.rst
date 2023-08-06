===========
MFC Scraper
===========


.. image:: https://img.shields.io/pypi/v/mfc_scraper.svg
        :target: https://pypi.python.org/pypi/mfc_scraper


.. image:: https://github.com/laurent-radoux/mfc_scraper/actions/workflows/python-test.yml/badge.svg
        :target: https://github.com/laurent-radoux/mfc_scraper/actions


.. image:: https://readthedocs.org/projects/mfc-scraper/badge/?version=latest
        :target: https://mfc-scraper.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status



Scrapes the content of one's collection of figures listed on MyFigureCollection


* Free software: MIT license
* Documentation: https://mfc-scraper.readthedocs.io.


Features
--------

* Scrapes the following information from MFC

  * All figure IDs owned by a particular user
  * For a particular figure

    * The characters represented
    * Its origin
    * The companies manufacturing the figure
    * Its classifications
    * Its version
    * Its release date
    * The main image URL

  * Images associated to a given figure

* Stores the scraped content as a JSON list in a file.
* Stores the figure images.

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
