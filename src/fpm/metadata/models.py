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
Package manifest format
=======================

Definition of the manifest format as used by the Fortran package manager (`fpm`_).

.. _fpm: https://fpm.fortran-lang.org


Example
-------

>>> import tomli as tomllib
>>> raw = '''
... name = "toml-f"
... version = "0.2.4"
... license = "Apache-2.0 OR MIT"
... maintainer = ["@awvwgk"]
... author = ["Sebastian Ehlert"]
... copyright = "2019-2021 Sebastian Ehlert"
... homepage = "https://toml-f.github.io/toml-f"
... keywords = ["toml", "io", "serde"]
... description = "TOML parser implementation for data serialization and deserialization"
...
... [library]
... source-dir = "src"
...
... [build]
... auto-tests = false
...
... [[test]]
... name = "tftest"
... source-dir = "test/tftest"
... [test.dependencies]
... test-drive.git = "https://github.com/fortran-lang/test-drive.git"
... '''
>>> manifest = Manifest(**tomllib.loads(raw))
>>> manifest.name
'toml-f'
>>> manifest.version
'0.2.4'
>>> len(manifest.test)
1
"""

from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field


class Build(BaseModel):
    """
    .. Build settings

    Definitions regarding the build model for the project, like
    automatic target discovery for executables, examples or tests.
    External dependencies like system libraries are declared here
    and propagated to dependent projects.
    """

    auto_tests: bool = Field(True, alias="auto-tests")
    """Automatic discovery of tests"""

    auto_executables: bool = Field(True, alias="auto-executables")
    """Automatic discovery of executables"""

    auto_examples: bool = Field(True, alias="auto-examples")
    """Automatic discovery of examples"""

    link: Union[str, List[str]] = []
    """Libraries to link against"""

    external_modules: Union[str, List[str]] = Field([], alias="external-modules")
    """Modules used from non-fpm packages"""


class Dependency(BaseModel):
    """
    .. Dependency

    A dependency on another fpm project.
    """

    ...


class LocalDependency(Dependency):
    """
    .. Local dependency definition

    Defines a dependency on another fpm-enabled project. The definition
    can reference local dependencies declared by relative paths.
    """

    path: str
    """Local target"""


class GitDependency(Dependency):
    """
    .. Remote dependency definition

    Defines a dependency on another fpm-enabled project. The definition
    can take targets under version control systems, like git.
    """

    git: str
    """Git repository target"""


class GitDependencyTag(GitDependency):
    """
    Git dependency using a tag as reference.
    """

    tag: str
    """Tag in git repository"""


class GitDependencyBranch(GitDependency):
    """
    Git dependency using a branch name as reference.
    """

    branch: str
    """Branch in git repository"""


class GitDependencyRev(GitDependency):
    """
    Git dependency using a commit hash as reference.
    """

    rev: str
    """Commit hash"""


DependencyUnion = Union[
    LocalDependency,
    GitDependencyTag,
    GitDependencyBranch,
    GitDependencyRev,
    GitDependency,
]


class Library(BaseModel):
    """
    .. Library settings

    Definition of the exported library target of the project.
    """

    source_dir: str = Field("src", alias="source-dir")
    """Source path prefix"""

    include_dir: Union[str, List[str]] = Field("include", alias="include-dir")
    """Include path prefix"""


class Executable(BaseModel):
    """
    .. Executable settings

    Definition of an executable target in the project.
    """

    name = str
    """Name of the resulting executable"""

    source_dir: str = Field("app", alias="source-dir")
    """Source directory for collecting the executable"""

    main: str = "main.f90"
    """Name of the source file declaring the main program"""

    link: Union[str, List[str]] = []
    """Libraries to link against"""

    dependencies: Dict[str, DependencyUnion] = {}
    """Dependency meta data for this executable"""


class Example(Executable):
    """
    .. Example settings

    Definition of an example target in the project.
    """

    source_dir: str = Field("example", alias="source-dir")
    """Source directory for collecting the executable"""


class Test(Executable):
    """
    .. Test settings

    Definition of a test target in the project.
    """

    source_dir: str = Field("test", alias="source-dir")
    """Source directory for collecting the executable"""


class Install(BaseModel):
    """
    .. Installation settings

    Targets defined by this project to be exported upon installation.
    """

    library: bool = False
    """Install library with this project"""


class Preprocess(BaseModel):
    """
    .. Preprocessing settings

    Preprocessing directives for the project.
    """

    macros: Union[str, List[str]] = []
    """Preprocessor macros e.g. ['HAVE_MPI', 'VALUE=1', 'VERSION={version}']"""

    directories: Union[str, List[str]] = []
    """Include directories"""

    suffixes: Union[str, List[str]]= []
    """Suffixes the preprocessor should run on"""


class Manifest(BaseModel):
    """
    .. Package manifest settings

    Package manifest definitions for the project. The package manifest
    contains all meta data describing the project and its contained targets.
    """

    name: str
    """Name of the project`"""

    version: str = "0"
    """Project version"""

    license: Optional[str]
    """Project license information"""

    maintainer: Union[str, List[str]] = []
    """Maintainer of the project"""

    author: Union[str, List[str]] = []
    """Author of the project"""

    copyright: Optional[str]
    """Copyright of the project"""

    description: Optional[str]
    """Description of the project"""

    categories: Union[str, List[str]] = []
    """Categories associated with the project"""

    keywords: List[str] = []
    """Keywords describing the project"""

    build = Build()
    """Build configuration data"""

    install = Install()
    """Installation configuration data"""

    library = Library()
    """Library meta data"""

    executable: List[Executable] = []
    """Executable meta data"""

    example: List[Example] = []
    """Example meta data"""

    test: List[Test] = []
    """Test meta data"""

    dependencies: Dict[str, DependencyUnion] = {}
    """Dependency meta data"""

    dev_dependencies: Dict[str, DependencyUnion] = Field({}, alias="dev-dependencies")
    """Development dependency meta data"""
    
    preprocess: Dict[str, Preprocess] = {}
    """Preprocessor meta data"""

    extra: Dict[str, Any] = {}
    """Additional free data field"""
