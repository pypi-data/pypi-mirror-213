import os

from tenyks.adapters.categories.readers.category_reader import CategoryReader
from tenyks.adapters.categories.readers.json_category_reader import JsonCategoryReader
from tenyks.adapters.categories.readers.txt_category_reader import TxtCategoryReader
from tenyks.adapters.config import CategoryFileExtension


class CategoryReaderFactory:
    category_format_mappings: dict[str, CategoryReader] = {
        CategoryFileExtension.JSON.value: JsonCategoryReader,
        CategoryFileExtension.TXT.value: TxtCategoryReader,
    }

    @staticmethod
    def create_category_reader(file_path: str) -> CategoryReader:
        _, extension = os.path.splitext(file_path)
        return CategoryReaderFactory.category_format_mappings[extension]
