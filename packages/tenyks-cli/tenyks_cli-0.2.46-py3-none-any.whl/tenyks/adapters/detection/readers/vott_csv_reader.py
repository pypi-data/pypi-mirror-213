import pandas as pd
from pandas import DataFrame

from tenyks.adapters.detection.detection_data import BoundingBox, DetectionData
from tenyks.adapters.detection.readers.detection_reader import DetectionReader
from tenyks.adapters.utilities.bbox import get_categories_from_classname_file


class VottCsvReader(DetectionReader):
    def read_annotations(
        detection_file_path: str, images_dir: str, classnames_file_path: str
    ) -> DetectionData:
        return VottCsvReader.__read(
            detection_file_path, images_dir, classnames_file_path
        )

    def read_predictions(
        detection_file_path: str, images_dir: str, classnames_file_path: str
    ) -> DetectionData:
        return VottCsvReader.__read(
            detection_file_path, images_dir, classnames_file_path
        )

    def __read(detection_file_path: str, _, classnames_file_path: str) -> DetectionData:
        csv_df = VottCsvReader.__read_detection_file(detection_file_path)

        categories = get_categories_from_classname_file(classnames_file_path)
        images = VottCsvReader.__get_images(csv_df)
        bbox = VottCsvReader.__get_bbox(images, csv_df)

        return DetectionData(images, bbox, categories)

    def __read_detection_file(detection_file_path: str):
        return pd.read_csv(
            detection_file_path,
            dtype={
                "image": str,
                "xmin": float,
                "ymin": float,
                "xmax": float,
                "ymax": float,
                "label": int,
                "score": float,
            },
        )

    def __get_images(csv_df: DataFrame):
        images = {}
        cur_image_id = 0
        for i in range(len(csv_df["image"])):
            if not csv_df["image"].iloc[i] in images:
                images[csv_df["image"].iloc[i]] = cur_image_id
                cur_image_id += 1
        return images

    def __get_bbox(images: dict, csv_df: DataFrame):
        bboxes = []
        for i in range(len(csv_df["xmin"])):
            score = csv_df["score"].iloc[i] if ("score" in csv_df) else 1
            bbox = BoundingBox(
                image_id=images[csv_df["image"].iloc[i]],
                category_id=int(csv_df["label"].iloc[i]),
                bbox=[
                    float(csv_df["xmin"].iloc[i]),
                    float(csv_df["ymin"].iloc[i]),
                    float(csv_df["xmax"].iloc[i]),
                    float(csv_df["ymax"].iloc[i]),
                ],
                score=score,
            )
            bboxes.append(bbox)

        return bboxes
