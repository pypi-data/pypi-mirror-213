from enum import Enum


class DetectionType(Enum):
    ANNOTATIONS = "annotations"
    PREDICTIONS = "predictions"


class DetectionFormat(Enum):
    COCO = "coco"
    VOTT_CSV = "vott_csv"
    YOLO = "yolo"
    DEEPSTREAM = "deepstream"
    CLASSIFICATION = "classification"


class CategoryFileExtension(Enum):
    JSON = ".json"
    TXT = ".txt"
