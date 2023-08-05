========
SaxTract
========


.. image:: https://img.shields.io/pypi/v/saxtract.svg
        :target: https://pypi.python.org/pypi/saxtract

.. image:: https://img.shields.io/travis/danwald/saxtract.svg
        :target: https://travis-ci.com/danwald/saxtract

.. image:: https://readthedocs.org/projects/saxtract/badge/?version=latest
        :target: https://saxtract.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/danwald/saxtract/shield.svg
     :target: https://pyup.io/repos/github/danwald/saxtract/
     :alt: Updates



Python SAX parser to extract xml


* Free software: MIT license
* Documentation: https://saxtract.readthedocs.io


Features
--------

Uses a SAXParser to maintain a fix memory footprint to parse and 'extract' tags from an  xml file and push it to an output stream.

With `performance tests <tests/perf_tests.py>`_ on a trimmed down to 10k records from the `dbpl <https://dblp.org/xml/>`_ dataset, SaxTrack ran in about half the time and half the `memory footprint <https://pypi.org/project/memory-profiler/>`_

.. code-block:: bash

	python tests/perf_tests.py --filename test.xml --tag authors --runs 5

	SaxTrack run took ~0.05381571219999999s
	DOM Parser run took ~0.09159613900000001s


Todo's
------

allow xsd/dtd input for validation

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

The main parser code was copied from `tutorialspoint <https://www.tutorialspoint.com/python3/python_xml_processing.htm>`_
