import pytest
import requests
import tempfile
from pathlib import Path

import fpm.metadata
from fpm.metadata import Manifest, load_manifest, dump_manifest

toml = []
for impl in ["tomllib", "tomli", "tomlkit", "pytomlpp"]:
    try:
        toml.append(__import__(impl))
    except ModuleNotFoundError:
        pass


tomlw = []
for impl in ["tomli_w", "tomlkit", "pytomlpp"]:
    try:
        tomlw.append(__import__(impl))
    except ModuleNotFoundError:
        pass



root = Path(__file__).parent
with open(root / "fpm-projects.txt") as fd:
    data = fd.read()

repos = [
    line.strip().split()[-1]
    for line in data.splitlines()
    if "https://github.com/" in line
]


@pytest.mark.parametrize("impl", toml)
def test_load_manifest(impl):
    _toml = fpm.metadata.toml
    fpm.metadata.toml = impl
    with tempfile.TemporaryDirectory() as tmpdir:
        file = Path(tmpdir) / "fpm.toml"
        with open(file, "w") as fd:
            fd.write("name = 'hello'\nkeywords = ['foo', 'bar']")
        manifest = load_manifest(file)
        assert manifest.name == "hello"
        assert manifest.keywords == ["foo", "bar"]
    fpm.metadata.toml = _toml


def test_load_manifest_no_impl():
    _toml = fpm.metadata.toml
    fpm.metadata.toml = None
    with tempfile.TemporaryDirectory() as tmpdir:
        file = Path(tmpdir) / "fpm.toml"
        with open(file, "w") as fd:
            fd.write("name = 'hello'")
        with pytest.raises(ModuleNotFoundError):
            load_manifest(file)
    fpm.metadata.toml = _toml


@pytest.mark.parametrize("impl", tomlw)
def test_dump_manifest(impl):
    _toml = fpm.metadata.tomlw
    fpm.metadata.tomlw = impl
    with tempfile.TemporaryDirectory() as tmpdir:
        file = Path(tmpdir) / "fpm.toml"
        dump_manifest(Manifest(name="hello", keywords=["foo", "bar"]), file)
        assert file.exists()
        manifest = load_manifest(file)
        assert manifest.name == "hello"
        assert manifest.keywords == ["foo", "bar"]
    fpm.metadata.tomlw = _toml


def test_dump_manifest_no_impl():
    _toml = fpm.metadata.tomlw
    fpm.metadata.tomlw = None
    manifest = Manifest(name="hello")
    with tempfile.TemporaryDirectory() as tmpdir:
        file = Path(tmpdir) / "fpm.toml"
        with pytest.raises(ModuleNotFoundError):
            dump_manifest(manifest, file)
    fpm.metadata.tomlw = _toml


@pytest.mark.parametrize("repo", repos)
def test_github(repo):
    repo = repo.replace("https://github.com/", "")
    response = requests.get(f"https://raw.githubusercontent.com/{repo}/HEAD/fpm.toml")
    if response.status_code == 200:
        try:
            load_manifest(response.text)
        except Exception as e:
            print(response.text)
            print(e)
            assert False


if __name__ == "__main__":

    for repo in repos:
        test_github(repo)
