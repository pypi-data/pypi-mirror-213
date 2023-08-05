from abc import ABC, abstractmethod
from io import BytesIO

from tenyks.adapters.detection.detection_data import DetectionData


class DetectionWriter(ABC):
    @abstractmethod
    def write_annotations(filename: str, data: DetectionData) -> BytesIO:
        raise NotImplementedError

    @abstractmethod
    def write_predictions(filename: str, data: DetectionData) -> BytesIO:
        raise NotImplementedError
