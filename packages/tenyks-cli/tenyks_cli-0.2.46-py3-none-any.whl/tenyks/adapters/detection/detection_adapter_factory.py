from tenyks.adapters.config import DetectionFormat
from tenyks.adapters.detection.detection_adapter import DetectionAdapter
from tenyks.adapters.detection.readers.classification_reader import ClassificationReader
from tenyks.adapters.detection.readers.deepstream_reader import DeepstreamReader
from tenyks.adapters.detection.readers.detection_reader import DetectionReader
from tenyks.adapters.detection.readers.vott_csv_reader import VottCsvReader
from tenyks.adapters.detection.readers.yolo_reader import YoloReader
from tenyks.adapters.detection.writers.coco_writer import CocoWriter
from tenyks.adapters.detection.writers.detection_writer import DetectionWriter


class DetectionAdapterFactory:
    reader_mappings: dict[DetectionFormat, DetectionReader] = {
        DetectionFormat.COCO.value: DetectionReader,  # DetectionReader for now until coco to x format is needed
        DetectionFormat.VOTT_CSV.value: VottCsvReader,
        DetectionFormat.YOLO.value: YoloReader,
        DetectionFormat.DEEPSTREAM.value: DeepstreamReader,
        DetectionFormat.CLASSIFICATION.value: ClassificationReader,
    }
    writer_mappings: dict[DetectionFormat, DetectionWriter] = {
        DetectionFormat.COCO.value: CocoWriter
    }

    @staticmethod
    def create_detection_adapter(
        input_file_type: str,
        output_file_type: str,
    ):
        reader = DetectionAdapterFactory.reader_mappings[input_file_type]
        writer = DetectionAdapterFactory.writer_mappings[output_file_type]
        return DetectionAdapter(
            reader,
            writer,
            input_file_type,
            output_file_type,
        )

    @staticmethod
    def get_supported_input_formats():
        return DetectionAdapterFactory.reader_mappings.keys()

    @staticmethod
    def get_supported_output_formats():
        return DetectionAdapterFactory.writer_mappings.keys()
