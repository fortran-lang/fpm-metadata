Python model of the Fortran package manager
===========================================

.. image:: https://img.shields.io/github/v/release/fortran-lang/fpm-metadata
   :alt: Latest release
   :target: https://github.com/fortran-lang/fpm-metadata/releases/latest

.. image:: https://img.shields.io/pypi/v/fpm-metadata
   :alt: PyPI
   :target: https://pypi.org/project/fpm-metadata/

.. image:: https://img.shields.io/github/license/fortran-lang/fpm-metadata
   :alt: License
   :target: LICENSE

.. image:: https://github.com/fortran-lang/fpm-metadata/actions/workflows/CI.yml/badge.svg
   :alt: CI status
   :target: https://github.com/fortran-lang/fpm-metadata/actions/workflows/CI.yml

.. image:: https://img.shields.io/codecov/c/gh/fortran-lang/fpm-metadata
   :alt: Codecov
   :target: https://codecov.io/gh/fortran-lang/fpm-metadata

This project provides a pydantic model of the fpm package manifest format used
in the `Fortran package manager <https://fpm.fortran-lang.org>`_.


Installation
------------

Install this project with pip

.. code:: shell

   pip install git+https://github.com/fortran-lang/fpm-metadata


Usage
-----

You can read a package manifest with your TOML library of choice and construct
a manifest object from it which allows to access all package entries directly
in Python

.. code:: python

   >>> from fpm.metadata import Manifest
   >>> from tomlkit import loads
   >>> with open("fpm.toml") as fh:
   ...     package = Manifest(**loads(fh.read()))
   ...
   >>> package.name
   'fpm'
   >>> package.version
   '0.2.0'

Alternatively, you can use the ``load_manifest`` function to read a package manifest

.. code:: python

   >>> from pathlib import Path
   >>> from fpm.metadata import load_manifest
   >>> package = load_manifest(Path("fpm.toml"))
   >>> package.name
   'fpm'
   >>> package.version
   '0.2.0'

Finally, you can dump a package manifest to a TOML string using the ``dump_manifest`` function

.. code:: python

   >>> from pathlib import Path
   >>> from fpm.metadata import dump_manifest, load_manifest
   >>> package = load_manifest(Path("fpm.toml"))
   >>> print(dump_manifest(package))
   name = "fpm"
   version = "0.2.0"
   ...


Development
-----------

This project is hosted on GitHub at `fortran-lang/fpm-metadata <https://github.com/fortran-lang/fpm-metadata>`__.
Obtain the source by cloning the repository with

.. code::

   git clone https://github.com/fortran-lang/fpm-metadata
   cd fpm-metadata

We recommend using a `conda <https://conda.io/>`__ environment to install the package.
You can setup the environment manager using a `mambaforge <https://github.com/conda-forge/miniforge>`__ installer.
Install the required dependencies from the conda-forge channel.

.. code::

   mamba env create -n devel -f environment.yml
   mamba activate devel

Install this project with pip in the environment

.. code::

   pip install .

Add the option ``-e`` for installing in development mode.

The following dependencies are required

- `pydantic <https://pydantic-docs.helpmanual.io/>`__
- `tomli <https://https://github.com/hukkin/tomli>`__ (tests only)
- `requests <https://requests.readthedocs.io>`__ (tests only)
- `pytest <https://docs.pytest.org/>`__ (tests only)

You can check your installation by running the test suite with

.. code::

   pytest tests/ --pyargs fpm.metadata --doctest-modules


For code formatting `black <https://black.readthedocs.io/>`_ is used:

.. code:: shell

   black src/ tests/


Contributing
------------

This is a volunteer open source projects and contributions are always welcome.
Please, take a moment to read the `contributing guidelines <CONTRIBUTING.md>`__.


License
-------

Licensed under the Apache License, Version 2.0 (the “License”);
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an *“as is” basis*,
*without warranties or conditions of any kind*, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Unless you explicitly state otherwise, any contribution intentionally
submitted for inclusion in this project by you, as defined in the
Apache-2.0 license, shall be licensed as above, without any additional
terms or conditions.
