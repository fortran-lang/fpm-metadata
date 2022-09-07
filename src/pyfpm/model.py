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
.. Package manifest format

Definition of the manifest format as used by the Fortran package manager (fpm).
"""

from __future__ import annotations

from typing import Any
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

    link: str | list[str] = []
    """Libraries to link against"""

    external_modules: str | list[str] = Field([], alias="external-modules")
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


DependencyUnion = (
    LocalDependency
    | GitDependencyTag
    | GitDependencyBranch
    | GitDependencyRev
    | GitDependency
)


class Library(BaseModel):
    """
    .. Library settings

    Definition of the exported library target of the project.
    """

    source_dir: str = Field("src", alias="source-dir")
    """Source path prefix"""

    include_dir: str | list[str] = Field("include", alias="include-dir")
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

    link: str | list[str] = []
    """Libraries to link against"""

    dependencies: dict[str, DependencyUnion] = {}
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

    license: str | None
    """Project license information"""

    maintainer: str | list[str] = []
    """Maintainer of the project"""

    author: str | list[str] = []
    """Author of the project"""

    copyright: str | None
    """Copyright of the project"""

    description: str | None
    """Description of the project"""

    categories: str | list[str] = []
    """Categories associated with the project"""

    keywords: list[str] = []
    """Keywords describing the project"""

    build = Build()
    """Build configuration data"""

    install = Install()
    """Installation configuration data"""

    library = Library()
    """Library meta data"""

    executable: list[Executable] = []
    """Executable meta data"""

    example: list[Example] = []
    """Example meta data"""

    test: list[Test] = []
    """Test meta data"""

    dependencies: dict[str, DependencyUnion] = {}
    """Dependency meta data"""

    dev_dependencies: dict[str, DependencyUnion] = Field({}, alias="dev-dependencies")
    """Development dependency meta data"""

    extra: dict[str, Any] = {}
    """Additional free data field"""
