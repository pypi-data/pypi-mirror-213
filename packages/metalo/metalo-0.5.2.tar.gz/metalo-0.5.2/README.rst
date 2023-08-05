|black| |rtd| |gpl|
|pypi-version| |pypi-python| |pypi-wheel| |deps|

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/python/black
   :alt: Code style: black

.. |rtd| image:: https://readthedocs.org/projects/metalo/badge/?version=latest
   :target: https://metalo.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. |gpl| image:: https://img.shields.io/pypi/l/metalo
   :target: https://gitlab.inria.fr/soliman/metalo/-/raw/main/LICENSE
   :alt: PyPI - License

.. |pypi-version| image:: https://img.shields.io/pypi/v/metalo
   :target: https://pypi.org/project/metalo/
   :alt: PyPI

.. |pypi-python| image:: https://img.shields.io/pypi/pyversions/metalo
   :alt: PyPI - Python Version
   :target: https://pypi.org/project/metalo/

.. |pypi-wheel| image:: https://img.shields.io/pypi/wheel/metalo
   :target: https://pypi.org/project/metalo/
   :alt: PyPI - Wheel

.. |deps| image:: https://img.shields.io/librariesio/release/pypi/metalo
   :target: https://pypi.org/project/metalo/
   :alt: Libraries.io dependency status for latest release

**MetaLo** is a framework for the Metabolic analysis (FBA) of Logical models extracted automatically from detailed mechanistic maps.
See this `published article`_ for more details.

.. _`published article`: http://dx.doi.org/10.1371/journal.pcbi.1010408

Install
=======

Metalo is provided as a Python3 package, you can install it from the `Python package index`_ with ``pip``, ``conda`` or your Python package manager of choice:

.. _`Python package index`: https://pypi.org/project/metalo/

.. code:: bash

   $ python3 -m pip install metalo

If you want to use the GUI you will need to explicitly request that feature, but it depends on ``wxPython`` which sometimes fails to build on some platformes.

.. code:: bash

   $ python3 -m pip install metalo[gui]

Command-line usage
==================

Just follow the instructions::

   $ metalo --help

   usage: metalo [-h] [-v] [-D] [-f] [-i INIT] [-c CASQ] MAP METABOLISM

   Metabolic analysis of Logical models extracted from maps. Copyright (C) 2023 Sahar.Aghakhani@inria.fr and Sylvain.Soliman@inria.fr
   GPLv3

   positional arguments:
   MAP                   CellDesigner file containing the mechanistic map
   METABOLISM            MitoCore style metabolic model

   options:
   -h, --help            show this help message and exit
   -v, --version         show program's version number and exit
   -D, --debug           display some debug information
   -f, --fva             run FVA to get interval of values
   -i INIT, --init INIT  CSV file with forced initial values for the Logic model
   -c CASQ, --casq CASQ  Additional arguments for CaSQ like -u, -d or -r

Or run ``metalo`` with no arguments to launch the GUI, if it is installed.
