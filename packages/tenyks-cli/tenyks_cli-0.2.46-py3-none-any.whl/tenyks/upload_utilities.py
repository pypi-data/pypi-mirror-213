import asyncio
import glob
import os
import time
from dataclasses import dataclass
from typing import Callable, List

import aiohttp
import click

from tenyks.api import Api
from tenyks.config.config import RETRIES_PER_FILE
from tenyks.utilities import get_file_path_extension


@dataclass
class FileInfo:
    path: str

    @property
    def name(self):
        return os.path.basename(self.path)


def upload(
    api: Api,
    upload_url: str,
    file_dir_path: str,
    description_of_file: str,
    accepted_extensions: List[str],
    max_concurrent_uploads: int = 20,
    verbose: bool = False,
):
    file_info_list = get_valid_files_from_directory(file_dir_path, accepted_extensions)

    click.echo(f"Starting {description_of_file} upload..")
    s = time.perf_counter()

    (successes, failures) = asyncio.run(
        start_file_upload(
            file_info_list,
            upload_url,
            api,
            max_concurrent_uploads,
            verbose,
        ),
        debug=False,
    )

    elapsed = time.perf_counter() - s
    print(f"Upload finished in {elapsed:0.2f} seconds.")

    click.echo(f"Successfully uploaded {len(successes)} {description_of_file}.")
    if len(failures) > 0:
        click.echo(f"Failed to upload: {failures}")


async def start_file_upload(
    file_info_list: List[FileInfo],
    upload_url: str,
    api: Api,
    max_concurrent: int,
    verbose: bool,
):
    sem = asyncio.Semaphore(max_concurrent)
    upload_tasks = []
    successful_upload_file_names = []
    failed_upload_file_names = []
    authenticated_headers = api.headers

    async with aiohttp.ClientSession(headers=authenticated_headers) as session:
        with click.progressbar(length=len(file_info_list)) as progress_bar:

            def handle_succeeded(file_info: FileInfo) -> None:
                successful_upload_file_names.append(file_info.name)
                if verbose:
                    click.echo(f"Successfully uploaded {file_info.name}")
                else:
                    progress_bar.update(1)

            def handle_failed(file_info: FileInfo, response) -> None:
                failed_upload_file_names.append(file_info.name)
                if verbose:
                    click.echo(f"Failed to upload {file_info.name}, {response}")
                else:
                    progress_bar.update(1)

            for file_info in file_info_list:
                task = asyncio.create_task(
                    upload_file_to_location(
                        file_info,
                        upload_url,
                        session,
                        sem,
                        api,
                        handle_succeeded,
                        handle_failed,
                    )
                )
                upload_tasks.append(task)

            await asyncio.gather(*upload_tasks)
    return (successful_upload_file_names, failed_upload_file_names)


async def upload_file_to_location(
    file_info: FileInfo,
    upload_url: str,
    session,
    sem,
    api: Api,
    on_succeeded: Callable[[str], None],
    on_failed: Callable[[str, object], None],
):
    async with sem:
        file = open(file_info.path, "rb")
        file_content = file.read()
        file.close()
        for i in range(RETRIES_PER_FILE):
            data = aiohttp.FormData()
            data.add_field("file", file_content, filename=file_info.name)
            try:
                async with session.put(upload_url, data=data) as response:
                    status = response.status
                    if status == 200:
                        if i > 0:
                            click.echo(
                                f" Succeeded retrying to upload {file_info.name}."
                            )
                        on_succeeded(file_info)
                        return

                    click.echo(
                        f"Failed to upload {file_info.name} on attempt {i+1} out of {RETRIES_PER_FILE}. Retrying.."
                    )

                    if i >= RETRIES_PER_FILE:
                        on_failed(file_info, response)
                        return
                    elif status == 401:
                        new_auth = api.get_authenticated_header()
                        session.headers["Authorization"] = new_auth["Authorization"]
                        await asyncio.sleep(i * i)

            except aiohttp.ClientError as exception:
                on_failed(file_info, exception)


def get_valid_files_from_directory(
    directory: str, accepted_extensions: List[str]
) -> List[FileInfo]:
    if os.path.exists(directory) is False:
        raise ValueError(f"File path {directory} does not exist...")

    files = [
        FileInfo(path=file_path)
        for file_path in glob.iglob(directory + "/*", recursive=True)
        if get_file_path_extension(file_path) in accepted_extensions
    ]

    return files
