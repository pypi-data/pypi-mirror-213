import os
from typing import List

from PIL import Image

from tenyks.adapters.categories.category_reader_factory import CategoryReaderFactory


def get_images_info(images_dir):
    images_map = {}  # filename (without extension) -> (extension, width, height)

    for filename in os.listdir(images_dir):
        name, extension = os.path.splitext(filename)

        # try to read the image, if invalid, continue to the next image
        try:
            img = Image.open(os.path.join(images_dir, filename))
        except Exception:
            continue

        images_map[name] = (extension, img.width, img.height)

    return images_map


def get_images(images_dir):
    images = {}  # filename -> image id

    for i, filename in enumerate(os.listdir(images_dir)):
        images[filename] = i

    return images


def get_categories_from_classname_file(classnames_file_path: str):
    category_reader = CategoryReaderFactory.create_category_reader(classnames_file_path)
    categories_array = category_reader.read(classnames_file_path)
    return get_categories(categories_array)


def get_categories(categories_array: List[str]):
    categories = {}

    for i in range(len(categories_array)):
        categories[str(categories_array[i])] = i

    return categories
