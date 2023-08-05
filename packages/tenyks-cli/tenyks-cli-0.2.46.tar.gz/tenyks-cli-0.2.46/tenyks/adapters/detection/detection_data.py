from dataclasses import dataclass
from typing import Optional

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class BoundingBox:
    image_id: int
    category_id: int
    bbox: list[float]
    score: Optional[float]


@dataclass_json
@dataclass
class DetectionData:
    images: dict  # file_name -> image_id
    bbox: list[BoundingBox]
    categories: dict  # category_name -> category_id
