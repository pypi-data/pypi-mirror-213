import os
import re
from asyncio import Semaphore
from pathlib import Path
from typing import Generator, Tuple, Optional

import httpx
from httpx import HTTPStatusError

WRITE_TIMEOUT = 60 * 3
VALID_NAME_PATTERN = re.compile("^[a-zA-Z0-9_.\-:=\/&$@;,?]+$")
INVALID_NAME_PATTERN = re.compile("[^a-zA-Z0-9_.\-:=\/&$@;,?]+")


class HttpClient:
    def __init__(self, timeout: int = WRITE_TIMEOUT):
        self.client = httpx.AsyncClient(timeout=timeout)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()

    async def stream(self, method: str, url: str, files=None, params=None):
        async with self.client.stream(method, url, files=files, params=params) as response:
            try:
                response.raise_for_status()
                return response
            except HTTPStatusError as e:  # Ensure we get a 2xx response
                raise e


class Uploader:
    def __init__(self, semaphore: Semaphore, file_path: str, url: str, dev: bool):
        self.semaphore = semaphore
        self.file_path = file_path
        self.url = url
        self.dev = dev

    @staticmethod
    def _validate_file_path(file_path: str) -> Optional[str]:
        if not re.match(VALID_NAME_PATTERN, file_path):
            invalids = "".join(re.findall(INVALID_NAME_PATTERN, file_path))
            return f"Invalid file name. Replace the following characters {invalids}, " \
                   f"and any spaces if you have them in your filepath."
        return None

    @staticmethod
    def _get_file(file_path: str) -> dict:
        with open(file_path, 'rb') as fp:
            return {'file': (fp.name, fp)}

    async def upload_file(self) -> Tuple[str, bool, Optional[str]]:
        """Asynchronously upload a file to a given URL."""

        if validation_error := self._validate_file_path(self.file_path):
            return self.file_path, False, validation_error

        try:
            files = self._get_file(self.file_path)
            async with HttpClient() as client:
                async with self.semaphore:
                    await client.stream('POST', self.url, files=files, params={"dev": self.dev})
                    return self.file_path, True, None
        except httpx.WriteTimeout:
            return self.file_path, False, "Upload took too long, check connection and try again."
        except Exception:
            return self.file_path, False, "Something went wrong uploading this file."


def find_files(filepath: Path) -> Generator[str, None, None]:
    # pattern = re.compile(r'\.(jpeg|jpg|png|mp4|mov)$')
    pattern = re.compile(r'\.(mp4|mov)$')
    for root, dirs, files in os.walk(filepath.absolute()):
        for file in files:
            lowered = file.lower()

            if re.search(pattern, lowered):
                yield os.path.join(root, file)
