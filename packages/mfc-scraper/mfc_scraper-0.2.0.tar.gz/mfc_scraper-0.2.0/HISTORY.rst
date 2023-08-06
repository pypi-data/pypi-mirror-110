=======
History
=======


0.2.0 (2021-06-22)
------------------
* Added origin, version and release date to scraped information
* Changed company and classification to return a list instead of a string

  * Handles cases where multiple companies or classifications are involved


0.1.2 (2021-06-21)
------------------
* First release on PyPI.
* Allows to scrape

  * All figure IDs owned by a particular user
  * For a particular figure

    * The characters represented
    * The company manufacturing the figure
    * Its classification
    * The main image URL

  * Images associated to a given figure

* Stores the scraped content as a JSON list in a file.
* Stores the figure images.
