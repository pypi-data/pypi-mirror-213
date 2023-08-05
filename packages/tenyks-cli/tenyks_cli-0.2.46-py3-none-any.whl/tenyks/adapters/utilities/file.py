import io
import os


def get_file_content(file_path: str):
    if os.path.exists(file_path):
        data = open(file_path, "rb")
        return data
    else:
        raise ValueError(f"File path {file_path} does not exist...")


def create_file(data: bytes, filename: str, extension: str) -> io.BytesIO:
    file = io.BytesIO(data)
    file.name = filename + extension
    return file
