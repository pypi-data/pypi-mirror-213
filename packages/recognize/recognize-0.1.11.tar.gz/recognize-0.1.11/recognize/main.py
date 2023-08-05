from typing import Optional

import typer
from typing_extensions import Annotated

from .commands import search, upload
from .commands.lib.client import DataAPI

app = typer.Typer()
app.add_typer(search.app, name="search")
app.add_typer(upload.app, name="upload")


@app.command()
def hello(
        dev: Annotated[bool, typer.Option("--dev")] = False,
        url: Annotated[Optional[str], typer.Option()] = None
):
    """
    Checks if API is running.

    :param url: URL override for the API.
    :param dev: An optional flag indicating whether to use the dev stack. Uses dev stack if True.
    :return: None
    """
    api = DataAPI(dev=dev, url=url)
    api.hello()


if __name__ == "__main__":
    app()
