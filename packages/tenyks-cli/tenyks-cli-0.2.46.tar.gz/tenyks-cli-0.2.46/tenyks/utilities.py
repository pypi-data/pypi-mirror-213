import io
import os

import click


def get_key_from_name(name: str):
    return name.lower()


def get_file_content(file_path: str):
    if os.path.exists(file_path):
        data = open(file_path, "rb")
        return data
    else:
        raise ValueError(f"File path {file_path} does not exist...")


def get_file_path_extension(file_path: str) -> str:
    return os.path.splitext(file_path)[1]


def write_file(data: io.BytesIO):
    with open(data.name, "wb") as f:
        f.write(data.getbuffer())


def exit_application_with_message(message: str):
    click.echo(click.style(f"Error: {message}", fg="red"))
    exit(1)
