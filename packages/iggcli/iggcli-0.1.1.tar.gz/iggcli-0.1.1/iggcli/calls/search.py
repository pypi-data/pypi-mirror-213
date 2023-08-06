from datetime import datetime as dt

from bs4 import BeautifulSoup, Tag
from rich import print
from rich.table import Table

from iggcli.core import scrap
from iggcli.values import search as E


def call(query: str, page: int) -> None:
    parse: BeautifulSoup = scrap.parse(["page", str(page)], {"s": query})

    table: Table = Table(title=f"Results for '{query}'", border_style="black")

    table.add_column("Title", style="green")
    table.add_column("Posted by")
    table.add_column("Genres")
    table.add_column("Release")

    for el in parse.select(E["elems"]):
        title: str = el.select_one(E["title"]).text  # type: ignore
        meta: list[Tag] = el.select(E["meta"])

        posted_by: str = meta[0].text
        genres: list[str] = [x.text for x in meta[1:]]
        date: str | dt = el.select_one(E["date"])["datetime"]  # type: ignore

        title = title.split("Free")[0]
        date = dt.fromisoformat(date)  # type: ignore

        table.add_row(
            title, posted_by, ", ".join(genres) + ".", date.strftime("%d/%m/%Y")
        )

    print(table)
