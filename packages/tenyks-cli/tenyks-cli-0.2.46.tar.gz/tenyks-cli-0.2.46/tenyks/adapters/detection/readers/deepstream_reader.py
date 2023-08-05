import pandas as pd
from pandas import DataFrame

from tenyks.adapters.detection.detection_data import BoundingBox, DetectionData
from tenyks.adapters.detection.readers.detection_reader import DetectionReader
from tenyks.adapters.utilities.bbox import (
    get_categories_from_classname_file,
    get_images,
    get_images_info,
)


class DeepstreamReader(DetectionReader):
    SCALING_FACTOR = 3.75

    def read_annotations(
        input_file_path: str, images_dir: str, classnames_file_path: str
    ) -> DetectionData:
        return DeepstreamReader.__read(
            input_file_path, images_dir, classnames_file_path
        )

    def read_predictions(
        input_file_path: str, images_dir: str, classnames_file_path: str
    ) -> DetectionData:
        return DeepstreamReader.__read(
            input_file_path, images_dir, classnames_file_path
        )

    def __read(
        input_file_path: str, images_dir: str, classnames_file_path: str
    ) -> DetectionData:
        assert images_dir is not None
        assert classnames_file_path is not None

        csv_df = DeepstreamReader.__read_detection_file(input_file_path)
        images_map = get_images_info(images_dir)

        images = get_images(images_dir)
        bbox = DeepstreamReader.__get_bbox(images, images_map, csv_df)
        categories = get_categories_from_classname_file(classnames_file_path)

        return DetectionData(images, bbox, categories)

    def __read_detection_file(input_file_path: str):
        return pd.read_csv(
            input_file_path,
            dtype={
                "frame_num": str,
                "model_l": float,
                "model_t": float,
                "model_w": float,
                "model_h": float,
                "class_id": int,
                "label": str,
                "model_confidence": float,
            },
        )

    def __get_bbox(images: dict, images_map: dict, csv_df: DataFrame):
        bbox_array = []

        for i in range(len(csv_df["model_l"])):
            image_name = csv_df["frame_num"].iloc[i]
            image_extension = images_map[csv_df["frame_num"].iloc[i]][0]
            image_id = images[image_name + image_extension]
            category_id = int(csv_df["class_id"].iloc[i])

            left = float(csv_df["model_l"].iloc[i])
            top = float(csv_df["model_t"].iloc[i])
            width = float(csv_df["model_w"].iloc[i])
            height = float(csv_df["model_h"].iloc[i])
            bbox = DeepstreamReader.__calculate_bbox(
                left, top, width, height, DeepstreamReader.SCALING_FACTOR
            )

            score = csv_df["model_confidence"].iloc[i]

            bbox_array.append(BoundingBox(image_id, category_id, bbox, score))

        return bbox_array

    def __calculate_bbox(
        left: float, top: float, width: float, height: float, scaling_factor: float
    ):
        x_min = left * scaling_factor
        y_min = top * scaling_factor
        x_max = (left + width) * scaling_factor
        y_max = (top + height) * scaling_factor

        return [x_min, y_min, x_max, y_max]
