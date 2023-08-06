from rich import print

from iggcli import __meta__ as meta
from iggcli import __url__ as repo_url


def call() -> None:
    print(f"Author: [red]{meta['Author']}[/] - {meta['Version']}")
    print(f"Repository: {repo_url}")
