from abc import ABC, abstractmethod
from typing import List


class CategoryReader(ABC):
    """
    Class for reading categories (class names) file
    """

    @abstractmethod
    def read(file_path: str) -> List[str]:
        raise NotImplementedError
