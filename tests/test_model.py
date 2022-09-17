import pytest
import requests
import tomli as toml
from pathlib import Path

from pyfpm.models import Manifest


root = Path(__file__).parent
with open(root / "fpm-projects.txt") as fd:
    data = fd.read()

repos = [
    line.strip().split()[-1]
    for line in data.splitlines()
    if "https://github.com/" in line
]


@pytest.mark.parametrize("repo", repos)
def test_github(repo):
    repo = repo.replace("https://github.com/", "")
    response = requests.get(f"https://raw.githubusercontent.com/{repo}/HEAD/fpm.toml")
    if response.status_code == 200:
        try:
            manifest = Manifest(**toml.loads(response.text))
        except Exception as e:
            print(response.text)
            print(e)
            assert False


if __name__ == "__main__":

    for repo in repos:
        test_github(repo)
