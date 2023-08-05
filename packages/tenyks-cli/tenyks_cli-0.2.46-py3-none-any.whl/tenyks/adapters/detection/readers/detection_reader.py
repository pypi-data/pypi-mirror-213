from abc import ABC, abstractmethod

from tenyks.adapters.detection.detection_data import DetectionData


class DetectionReader(ABC):
    @abstractmethod
    def read_annotations(
        input: str, images_dir: str = None, classnames: str = None
    ) -> DetectionData:
        raise NotImplementedError

    @abstractmethod
    def read_predictions(
        input: str, images_dir: str = None, classnames: str = None
    ) -> DetectionData:
        raise NotImplementedError
