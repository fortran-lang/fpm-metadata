# This file is part of pyfpm.
# SPDX-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Python model for Fortran package manifests
"""

from pathlib import Path
from typing import Optional, Union

from .models import Manifest


for impl in ["tomllib", "tomli", "tomlkit", "pytomlpp"]:
    try:
        toml = __import__(impl)
        break
    except ModuleNotFoundError:
        toml = None


for impl in ["tomli_w", "tomlkit", "pytomlpp"]:
    try:
        tomlw = __import__(impl)
        break
    except ModuleNotFoundError:
        tomlw = None


def load_manifest(inp: Union[str, Path]) -> Manifest:
    """
    Load a manifest from a file or string

    Parameters
    ----------
    inp : str or Path
        Path to a manifest file or a string containing a manifest

    Returns
    -------
    Manifest
        A manifest object

    Examples
    --------
    >>> manifest = load_manifest("name = 'hello'")
    >>> manifest.name
    'hello'
    """

    if toml is None:
        raise ModuleNotFoundError("No TOML library available")

    if isinstance(inp, Path):
        with open(inp, "rb") as fd:
            data = toml.load(fd)
    else:
        data = toml.loads(inp)

    return Manifest(**data)


def dump_manifest(manifest: Manifest, out: Optional[Path] = None) -> Optional[str]:
    """
    Write a manifest to a file

    Parameters
    ----------
    manifest : Manifest
        A manifest object
    out : Path, optional
        Path to a file to write the manifest to, by default None

    Returns
    -------
    str or None
        If out is None, the manifest is returned as a string

    Examples
    --------
    >>> manifest = Manifest(name="hello")
    >>> print(dump_manifest(manifest))
    name = "hello"
    version = "0"
    <BLANKLINE>
    [build]
    auto_tests = true
    auto_executables = true
    auto_examples = true
    <BLANKLINE>
    [install]
    library = false
    <BLANKLINE>
    [library]
    source_dir = "src"
    include_dir = "include"
    <BLANKLINE>
    """

    if tomlw is None:
        raise ModuleNotFoundError("No TOML library available")

    def empty(data):
        return data is None or (isinstance(data, (list, dict)) and not data)

    def prune(data):
        if isinstance(data, dict):
            return {k: prune(v) for k, v in data.items() if not empty(v)}
        if isinstance(data, list):
            return [prune(v) for v in data if not empty(v)]
        return data

    data = prune(manifest.dict())

    if out is None:
        return tomlw.dumps(data)

    with open(out, "wb" if tomlw.__name__ == "tomli_w" else "w") as fd:
        tomlw.dump(prune(data), fd)
