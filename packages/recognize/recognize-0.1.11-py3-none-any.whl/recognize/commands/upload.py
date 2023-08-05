import asyncio
from pathlib import Path
from typing import Optional

import typer
from typing_extensions import Annotated

from .lib.client import DataAPI
from .lib.helpers import find_files

short_help_description = "Commands that allow you to upload to files and folders into the S3 bucket for analysis."
help_description = "Commands that allow you to upload to files and folders into the S3 bucket for analysis."
app = typer.Typer(help=help_description, short_help=short_help_description)


@app.command()
def directory(
        path: Annotated[
            Path, typer.Argument(help="The directory path from which files will be retrieved and uploaded.")],
        dev: Annotated[bool, typer.Option("--dev",
                                          help="An optional flag indicating whether to use the dev stack. Uses dev stack if True.")] = False,
        url: Annotated[Optional[str], typer.Option(help="URL override for the API.")] = None
):
    """
    Uploads all files of types mp4, and mov from a given directory. In the future we will handle: png, jpeg

    :param url: URL override for the API.
    :param path: The directory path from which files will be retrieved and uploaded.
    :param dev: An optional flag indicating whether to use the dev stack. Uses dev stack if True.
    :return: None
    """
    if Path.is_file(path):
        print("File path is a file use 'file' subcommand")
    else:
        base = path.absolute().name
        files = find_files(path)
        api = DataAPI(dev=dev, url=url)
        asyncio.run(api.upload_files(base, files))


@app.command()
def file(
        path: Annotated[Path, typer.Argument(help="The file path of the file to upload.")],
        directory: Annotated[
            str, typer.Option(help="The directory in the bucket to upload the file to. Defaults to 'misc'.")] = "misc",
        dev: Annotated[bool, typer.Option("--dev",
                                          help="An optional flag indicating whether to use the dev stack. Uses dev stack if True.")] = False,
        url: Annotated[Optional[str], typer.Option(help="URL override for the API.")] = None
):
    """
    Uploads file at path of types mp4, and mov. In the future we will handle: png, jpeg

    :param path: The file path of the file to upload.
    :param directory: The directory in the bucket to upload the file to. Defaults to 'misc'.
    :param url: URL override for the API.
    :param dev: An optional flag indicating whether to use the dev stack. Uses dev stack if True.
    :return: None
    """
    if Path.is_file(path):
        files = (x for x in [str(path)])
        api = DataAPI(dev=dev, url=url)
        asyncio.run(api.upload_files(directory, files))
    else:
        print("File path is a directory use 'directory' subcommand")
