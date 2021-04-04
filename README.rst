Python model of the Fortran package manager
===========================================

This project provides a pydantic model of the fpm package manifest format used
in the `Fortran package manager <https://github.com/fortran-lang/fpm>`_.


Installation
------------

Install this project with pip

.. code:: shell

   pip install -e .


Usage
-----

You can read a package manifest with your TOML library of choice and construct
a manifest object from it which allows to access all package entries directly
in Python

.. code:: python

   >>> from pyfpm.model import Manifest
   >>> from tomlkit import loads
   >>> with open("fpm.toml") as fh:
   ...     package = Manifest(**loads(fh.read()))
   ...
   >>> package.name
   'fpm'
   >>> package.version
   '0.2.0'


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
