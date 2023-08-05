from io import BytesIO
from typing import Callable

from tenyks.adapters.detection.detection_adapter_factory import DetectionAdapterFactory


class DetectionFileProcessor:
    """
    Class for converting one detection format to another.
    "Detection" here is meant to mean either annotations or predictions.
    """

    @staticmethod
    def process_annotations_file(
        annotations_file_path: str,
        input_format: str,
        output_format: str,
        images_dir: str,
        class_names_dir: str,
    ) -> BytesIO:
        detection_adapter = DetectionAdapterFactory.create_detection_adapter(
            input_format, output_format
        )
        return DetectionFileProcessor.__process_file(
            annotations_file_path,
            images_dir,
            class_names_dir,
            detection_adapter.convert_annotations,
        )

    @staticmethod
    def process_predictions_file(
        predictions_file_path: str,
        input_format: str,
        output_format: str,
        images_dir: str,
        class_names_dir: str,
    ) -> BytesIO:
        detection_adapter = DetectionAdapterFactory.create_detection_adapter(
            input_format, output_format
        )
        return DetectionFileProcessor.__process_file(
            predictions_file_path,
            images_dir,
            class_names_dir,
            detection_adapter.convert_predictions,
        )

    @staticmethod
    def __process_file(
        path: str, images_dir: str, class_names_dir: str, convert_fn: Callable
    ) -> BytesIO:
        return convert_fn(path, images_dir, class_names_dir)
