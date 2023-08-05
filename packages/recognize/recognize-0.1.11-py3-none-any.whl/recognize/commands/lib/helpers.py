import os
import re
from asyncio import Semaphore
from pathlib import Path
from typing import Generator, Tuple, Optional

import httpx
from httpx import HTTPStatusError

WRITE_TIMEOUT = 60 * 3


async def upload_file(semaphore: Semaphore, file_path: str, url: str, dev: bool) -> Tuple[str, bool, Optional[str]]:
    """Asynchronously upload a file to a given URL."""
    with open(file_path, 'rb') as fp:
        files = {'file': (fp.name, fp)}
        try:
            async with httpx.AsyncClient(timeout=WRITE_TIMEOUT) as client:
                async with semaphore:
                    async with client.stream('POST', url, files=files, params={"dev": dev}) as response:
                        try:
                            response.raise_for_status()
                            return file_path, True, None
                        except HTTPStatusError as e:  # Ensure we get a 2xx response
                            return file_path, False, str(e)
        except httpx.WriteTimeout:
            return file_path, False, "Upload took too long, check connection and try again."
        except Exception:
            return file_path, False, "Something went wrong uploading this file."


def find_files(filepath: Path) -> Generator[str, None, None]:
    # pattern = re.compile(r'\.(jpeg|jpg|png|mp4|mov)$')
    pattern = re.compile(r'\.(mp4|mov)$')
    for root, dirs, files in os.walk(filepath.absolute()):
        for file in files:
            lowered = file.lower()

            if re.search(pattern, lowered):
                yield os.path.join(root, file)
