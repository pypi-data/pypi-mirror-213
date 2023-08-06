import typer as ty

from iggcli import calls as c

app: ty.Typer = ty.Typer(help="Download your games from Igg Games more easily")


@app.command()
def credits() -> None:
    c.credits()


@app.command()
def search(title: list[str], page: int = 1) -> None:
    c.search(" ".join(title), page)
