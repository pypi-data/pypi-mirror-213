import asyncio
from pathlib import Path
from typing import List, IO, Generator, Optional
from urllib.parse import urljoin

import httpx
import rich
import speedtest

from .entries import LabelEntryType
from .helpers import upload_file

PROD_URL = "http://media-farga-PEWZKMSNKOF4-22fe798e318ef706.elb.eu-west-2.amazonaws.com"
DEV_URL = "http://media-farga-OX4UJ0DDZR98-6ba3d7c365204667.elb.eu-west-2.amazonaws.com"


class DataAPI:
    def __init__(self, dev: bool = False, url: Optional[str] = None):
        self.dev = dev
        self.timeout = 60 * 3
        self.url = (DEV_URL if dev else PROD_URL) if url is None else url

    def hello(self):
        with httpx.Client() as client:
            response = client.get(self.url)
            message = response.json().get("message", None)
            if message is None:
                print("API is not available.")
            else:
                print("API is available.")

    def keyword_search(self, keywords: List[str], output_file: Path, response_type: str):
        url = urljoin(self.url, f"search/")

        with httpx.stream("GET", url, timeout=self.timeout, params={
            "keywords": ",".join(keywords),
            "response_type": response_type,
            "dev": self.dev
        }) as response, \
                open(output_file, "wb") as output:
            self._process_response(output, response)

    def entry_search(self, entry: LabelEntryType, output_file: Path, response_type: str):
        url = urljoin(self.url, f"search/")

        with httpx.stream("GET", url, timeout=self.timeout, params={
            "entry_type": entry.value,
            "response_type": response_type,
            "dev": self.dev
        }) as response, \
                open(output_file, "wb") as output:
            self._process_response(output, response)

    def faces_search(self, image: IO[bytes], output_file: Path, response_type: str):
        files = {'file': (image.name, image)}
        url = urljoin(self.url, f"search/faces")

        with httpx.stream("POST", url, timeout=self.timeout, params={
            "response_type": response_type,
            "dev": self.dev
        }, files=files) as response, \
                open(output_file, "wb") as output:
            self._process_response(output, response)

    async def upload_files(self, base_path, file_paths: Generator[str, None, None]) -> None:
        """Upload files concurrently to a given URL."""
        url = urljoin(self.url, f"upload/{base_path}")

        try:
            st = speedtest.Speedtest()
            upload_speed_mbps = st.upload() / 1e6  # Convert bits per second to Mbps
        except:
            upload_speed_mbps = 10

        max_concurrent_uploads = min(15, max(1, int(upload_speed_mbps / 2)))
        semaphore = asyncio.Semaphore(max_concurrent_uploads)

        tasks = [upload_file(semaphore, file_path, url, self.dev) for file_path in file_paths]

        with rich.progress.Progress(
                "[progress.percentage]{task.percentage:>3.0f}%",
                rich.progress.BarColumn(bar_width=None),
                rich.progress.MofNCompleteColumn(),
        ) as progress:
            download_task = progress.add_task(description="Uploading files...", total=len(tasks))
            progress.console.print(
                f'[bold green]Current upload speed: {int(upload_speed_mbps)} Mbps. '
                f'Number of concurrent uploads limited to {max_concurrent_uploads}.'
            )
            for task in asyncio.as_completed(tasks):
                path, success, message = await task
                progress.console.print(
                    f"{'[bold blue]Uploaded' if success else '[bold red]Failed'}: {path}. {message if not success else ''}")
                progress.update(download_task, advance=1)

    def get_upload_url(self) -> dict:
        with httpx.Client(base_url=self.url) as client:
            response = client.get("upload/url")
            return response.json()

    @staticmethod
    def _process_response(output, response):
        total = int(response.headers.get("Content-Length"))

        with rich.progress.Progress(
                "[progress.percentage]{task.percentage:>3.0f}%",
                rich.progress.BarColumn(bar_width=None),
                rich.progress.DownloadColumn(),
                rich.progress.TransferSpeedColumn(),
        ) as progress:
            download_task = progress.add_task("Download", total=total)

            for chunk in response.iter_bytes():
                output.write(chunk)
                progress.update(download_task, completed=response.num_bytes_downloaded)
