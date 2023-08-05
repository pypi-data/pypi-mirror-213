import os

import pandas as pd
from pandas import DataFrame

from tenyks.adapters.detection.detection_data import BoundingBox, DetectionData
from tenyks.adapters.detection.readers.detection_reader import DetectionReader
from tenyks.adapters.utilities.bbox import (
    get_categories_from_classname_file,
    get_images,
    get_images_info,
)


class ClassificationReader(DetectionReader):
    def read_annotations(
        detection_file_path: str, images_dir: str, classnames_file_path: str
    ) -> DetectionData:
        return ClassificationReader.__read(
            detection_file_path, images_dir, classnames_file_path, "ground_truth"
        )

    def read_predictions(
        detection_file_path: str, images_dir: str, classnames_file_path: str
    ) -> DetectionData:
        return ClassificationReader.__read(
            detection_file_path, images_dir, classnames_file_path, "prediction"
        )

    def __read(
        detection_file_path: str,
        images_dir: str,
        classnames_file_path: str,
        category_col_name: str,
    ) -> DetectionData:
        assert images_dir is not None

        images_map = get_images_info(images_dir)
        csv_df = ClassificationReader.__read_detection_file(
            detection_file_path, category_col_name
        )

        images = get_images(images_dir)
        categories = get_categories_from_classname_file(classnames_file_path)
        bbox = ClassificationReader.__get_bbox(
            csv_df, images, images_map, category_col_name
        )

        return DetectionData(images, bbox, categories)

    def __read_detection_file(
        detection_file_path: str, category_col_name: str
    ) -> DataFrame:
        return pd.read_csv(
            detection_file_path,
            dtype={
                category_col_name: str,
                "file_path": str,
                "score": float,
            },
        )

    def __get_bbox(
        csv_df: DataFrame,
        images: dict,
        images_map: dict,
        category_col_name: str,
    ):
        bbox_array = []

        for i in range(len(csv_df["file_path"])):
            filename = csv_df["file_path"].iloc[i]
            name, _ = os.path.splitext(filename)
            image_id = images[filename]
            category_id = int(csv_df[category_col_name].iloc[i])
            bbox = [
                0,
                0,
                images_map[name][1],
                images_map[name][2],
            ]
            score = csv_df["score"].iloc[i]
            bbox_array.append(BoundingBox(image_id, category_id, bbox, score))

        return bbox_array
