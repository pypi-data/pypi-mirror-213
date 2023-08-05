import json
from io import BytesIO

from tenyks.adapters.config import DetectionType
from tenyks.adapters.detection.detection_data import DetectionData
from tenyks.adapters.detection.writers.detection_writer import DetectionWriter
from tenyks.adapters.utilities.file import create_file


class CocoWriter(DetectionWriter):
    def write_predictions(filename: str, data: DetectionData) -> BytesIO:
        return CocoWriter.__write(filename, data, DetectionType.PREDICTIONS)

    def write_annotations(filename: str, data: DetectionData) -> BytesIO:
        return CocoWriter.__write(filename, data, DetectionType.ANNOTATIONS)

    def __write(
        filename: str,
        data: DetectionData,
        detection_type: DetectionType,
    ) -> BytesIO:
        coco = {
            "images": [
                {"id": int(data.images[file_name]), "file_name": str(file_name)}
                for file_name in data.images.keys()
            ],
            detection_type.value: [
                {
                    "id": i,
                    "image_id": int(bbox.image_id),
                    "category_id": int(bbox.category_id),
                    "bbox": bbox.bbox,
                    "score": float(bbox.score) if bbox.score else None,
                }
                for i, bbox in enumerate(data.bbox)
            ],
            "categories": [
                {"id": int(data.categories[name]), "name": str(name)}
                for name in data.categories.keys()
            ],
        }

        file = create_file(json.dumps(coco).encode(), filename, ".json")
        return file
