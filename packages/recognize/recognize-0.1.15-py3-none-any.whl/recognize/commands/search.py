import re
from pathlib import Path
from typing import List, Optional

import typer
from typing_extensions import Annotated

from .lib.client import DataAPI
from .lib.entries import LabelEntryType

short_help_description = "Commands that allow you to search through analysed content."
app = typer.Typer(help=short_help_description, short_help=short_help_description)


@app.command()
def keywords(
        words: Annotated[List[str], typer.Argument(help="A list of keywords to search for.")],
        output: Annotated[Path, typer.Option(help="The output path where the search results will be stored.")],
        json: Annotated[bool, typer.Option(
            "--json",
            help="An optional flag indicating whether the output should be in JSON format. If False, the output is CSV."
                 "This flag will override the filetype given in the file name."
        )] = False,
        dev: Annotated[bool, typer.Option(
            "--dev",
            help="An optional flag indicating whether to use the dev stack. Uses dev stack if True."
        )] = False,
        url: Annotated[Optional[str], typer.Option(help="URL override for the API.", hidden=True)] = None
):
    """
    Execute a keyword search.

    :param url: URL override for the API
    :param words: A list of keywords to search for.
    :param output: The output path where the search results will be stored.
    :param json: An optional flag indicating whether the output should be in JSON format. If False, the output is CSV.
    :param dev: An optional flag indicating whether to use the dev stack. Uses dev stack if True.
    :return: The result of the search operation.
    """
    api = DataAPI(dev=dev, url=url)
    pattern = re.compile("\.json$")
    json = json or re.search(pattern, str(output).lower()) is not None

    return api.keyword_search(words, output, response_type="csv" if not json else "json")


@app.command()
def entry(
        entry_type: Annotated[LabelEntryType, typer.Argument(help="The type of entries to search for.")],
        output: Annotated[Path, typer.Option(help="The output path where the search results will be stored.")],
        json: Annotated[bool, typer.Option(
            "--json",
            help="An optional flag indicating whether the output should be in JSON format. If False, the output is CSV."
                 "This flag will override the filetype given in the file name."
        )] = False,
        dev: Annotated[bool, typer.Option(
            "--dev",
            help="An optional flag indicating whether to use the dev stack. Uses dev stack if True."
        )] = False,
        url: Annotated[Optional[str], typer.Option(help="URL override for the API.", hidden=True)] = None
):
    """
    Execute a search for entries of a specific type.

    :param url: URL override for the API.
    :param entry_type: The type of entries to search for.
    :param output: The output path where the search results will be stored.
    :param json: An optional flag indicating whether the output should be in JSON format. If False, the output is CSV.
    :param dev: An optional flag indicating whether to use the dev stack. Uses dev stack if True.
    :return: The result of the search operation.
    """
    api = DataAPI(dev=dev, url=url)
    pattern = re.compile("\.json$")
    json = json or re.search(pattern, str(output).lower()) is not None

    return api.entry_search(entry_type, output, response_type="csv" if not json else "json")


@app.command()
def faces(
        image_file: Annotated[
            Path, typer.Argument(help="The path to the image file that will be used for the face search.")],
        output: Annotated[Path, typer.Option(help="The output path where the search results will be stored.")],
        json: Annotated[bool, typer.Option(
            "--json",
            help="An optional flag indicating whether the output should be in JSON format. If False, the output is CSV."
                 "This flag will override the filetype given in the file name."
        )] = False,
        dev: Annotated[bool, typer.Option(
            "--dev",
            help="An optional flag indicating whether to use the dev stack. Uses dev stack if True."
        )] = False,
        url: Annotated[Optional[str], typer.Option(help="URL override for the API.", hidden=True)] = None
):
    """
    Execute a face search using a provided image file.

    :param url: URL override for the API.
    :param image_file: The path to the image file that will be used for the face search.
    :param output: The output path where the search results will be stored.
    :param json: An optional flag indicating whether the output should be in JSON format. If False, the output is CSV. This flag will override the filetype given in the file name.
    :param dev: An optional flag indicating whether to use the dev stack. Uses dev stack if True.
    :return: The result of the search operation.
    """
    api = DataAPI(dev=dev, url=url)

    with open(image_file, 'rb') as fp:
        pattern = re.compile("\.json$")
        json = json or re.search(pattern, str(output).lower()) is not None

        return api.faces_search(fp, output, response_type="csv" if not json else "json")
