import json

from tenyks.adapters.categories.readers.category_reader import CategoryReader
from tenyks.adapters.utilities.file import get_file_content


class JsonCategoryReader(CategoryReader):
    def read(file_path: str):
        data = get_file_content(file_path)
        return json.loads(data.read())["categories"]
