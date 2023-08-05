import os

import pandas as pd

from tenyks.adapters.detection.detection_data import BoundingBox, DetectionData
from tenyks.adapters.detection.readers.detection_reader import DetectionReader
from tenyks.adapters.utilities.bbox import (
    get_categories_from_classname_file,
    get_images,
    get_images_info,
)


# https://roboflow.com/formats/yolov8-pytorch-txt
class YoloReader(DetectionReader):
    def read_annotations(
        detection_dir: str, images_dir: str, classnames_file_path: str
    ) -> DetectionData:
        return YoloReader.__read(detection_dir, images_dir, classnames_file_path)

    def read_predictions(
        detection_dir: str, images_dir: str, classnames_file_path: str
    ) -> DetectionData:
        return YoloReader.__read(detection_dir, images_dir, classnames_file_path)

    def __read(
        detection_dir: str, images_dir: str, classnames_file_path: str
    ) -> DetectionData:
        assert images_dir is not None
        assert classnames_file_path is not None

        images_map = get_images_info(images_dir)

        images = get_images(images_dir)
        bbox = YoloReader.__get_bbox(detection_dir, images_map, images)
        categories = get_categories_from_classname_file(classnames_file_path)

        return DetectionData(images, bbox, categories)

    def __read_detection_file(detection_file_path: str):
        return pd.read_csv(detection_file_path, sep=" ", header=None)

    def __get_bbox(detection_dir: str, images_map: dict, images: dict):
        bbox_array = []

        for filename in os.listdir(detection_dir):
            detection_file_path = os.path.join(detection_dir, filename)
            name = os.path.splitext(filename)[0]

            if name not in images_map:
                continue

            img_extension, img_width, img_height = images_map[name]
            img_key = name + img_extension

            if os.path.getsize(detection_file_path) > 0:
                df = YoloReader.__read_detection_file(detection_file_path)

                for _, row in df.iterrows():
                    category_id = row.values[0]
                    center_x = row.values[1]
                    center_y = row.values[2]
                    width = row.values[3]
                    height = row.values[4]
                    image_id = images[img_key]
                    bbox = YoloReader.__calculate_bbox(
                        center_x, center_y, width, height, img_width, img_height
                    )
                    score = 1 if len(row.values) == 5 else row.values[5]

                    bbox_array.append(
                        BoundingBox(
                            image_id,
                            category_id,
                            bbox,
                            score,
                        )
                    )

        return bbox_array

    def __calculate_bbox(
        center_x: float,
        center_y: float,
        width: float,
        height: float,
        img_width: int,
        img_height: int,
    ):
        x_min = (center_x - width / 2) * img_width
        x_max = (center_x + width / 2) * img_width
        y_min = (center_y - height / 2) * img_height
        y_max = (center_y + height / 2) * img_height

        return [x_min, y_min, x_max, y_max]
