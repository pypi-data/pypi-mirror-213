import os

from tenyks.adapters.categories.readers.category_reader import CategoryReader
from tenyks.adapters.utilities.file import get_file_content


class TxtCategoryReader(CategoryReader):
    def read(file_path: str):
        data = get_file_content(file_path)
        categories = data.read().decode("UTF-8").split(os.linesep)
        categories = [category.strip(" ") for category in categories if category]
        return categories
