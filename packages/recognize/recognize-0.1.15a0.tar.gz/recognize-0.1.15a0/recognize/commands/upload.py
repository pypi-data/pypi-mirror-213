import asyncio
from pathlib import Path
from typing import Optional

import rich
import typer
from typing_extensions import Annotated

from .lib.client import DataAPI
from .lib.helpers import find_files, validate_file_path

short_help_description = "Commands that allow you to upload to files and folders into the S3 bucket for analysis."
help_description = "Commands that allow you to upload to files and folders into the S3 bucket for analysis."
app = typer.Typer(help=help_description, short_help=short_help_description)


@app.command()
def directory(
        path: Annotated[
            Path, typer.Argument(help="The directory path from which files will be retrieved and uploaded.")],
        tag: Annotated[Optional[str], typer.Option(help="Custom directory name used in the S3 bucket."
                                                        " If None the directory name will be used.")] = None,
        dev: Annotated[bool, typer.Option("--dev",
                                          help="An optional flag indicating whether to use the dev stack. Uses dev stack if True.")] = False,
        url: Annotated[Optional[str], typer.Option(help="URL override for the API.")] = None
):
    """
    Uploads all files of types mp4, and mov from a given directory. In the future we will handle: png, jpeg

    :param tag: Custom directory name used in the S3 bucket. If None the directory name will be used.
    :param url: URL override for the API.
    :param path: The directory path from which files will be retrieved and uploaded.
    :param dev: An optional flag indicating whether to use the dev stack. Uses dev stack if True.
    :return: None
    """
    if Path.is_file(path):
        print("File path is a file use 'file' subcommand")
    else:
        base = path.absolute().name if tag is None else tag

        if validation_error := validate_file_path(base):
            rich.print(f"[bold red] {validation_error}")
            return

        files = find_files(path)
        api = DataAPI(dev=dev, url=url)
        asyncio.run(api.upload_files(base, files))


@app.command()
def file(
        path: Annotated[Path, typer.Argument(help="The file path of the file to upload.")],
        tag: Annotated[str, typer.Option(help="Custom directory name used in the S3 bucket."
                                              "If None the directory name will be used.")] = "misc",
        dev: Annotated[bool, typer.Option("--dev",
                                          help="An optional flag indicating whether to use the dev stack. Uses dev stack if True.")] = False,
        url: Annotated[Optional[str], typer.Option(help="URL override for the API.")] = None
):
    """
    Uploads file at path of types mp4, and mov. In the future we will handle: png, jpeg

    :param path: The file path of the file to upload.
    :param tag: Custom directory name used in the S3 bucket. Defaults to 'misc'.
    :param url: URL override for the API.
    :param dev: An optional flag indicating whether to use the dev stack. Uses dev stack if True.
    :return: None
    """
    if Path.is_file(path):
        if validation_error := validate_file_path(tag):
            rich.print(f"[bold red] {validation_error}")
            return

        files = (x for x in [str(path)])
        api = DataAPI(dev=dev, url=url)
        asyncio.run(api.upload_files(tag, files))
    else:
        print("File path is a directory use 'directory' subcommand")
