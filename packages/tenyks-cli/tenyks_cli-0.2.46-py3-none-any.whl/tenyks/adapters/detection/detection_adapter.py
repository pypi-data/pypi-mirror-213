import os
import traceback
from io import BytesIO
from typing import Callable

from tenyks.adapters.detection.readers.detection_reader import DetectionReader
from tenyks.adapters.detection.writers.detection_writer import DetectionWriter
from tenyks.adapters.utilities.file import create_file, get_file_content


class DetectionAdapter:
    """
    This class is responsible for converting one annotations/predictions format to another.
    """

    def __init__(
        self,
        reader: DetectionReader,
        writer: DetectionWriter,
        input_file_type: str,
        output_file_type: str,
    ):
        self.reader = reader
        self.writer = writer
        self.input_file_type = input_file_type
        self.output_file_type = output_file_type

    def convert_annotations(
        self,
        input_file: str,  # input file path or directory
        images_folder_path: str = None,
        classnames_file_path: str = None,
    ) -> BytesIO:
        return self.__convert(
            input_file,
            images_folder_path,
            classnames_file_path,
            self.reader.read_annotations,
            self.writer.write_annotations,
        )

    def convert_predictions(
        self,
        input_file: str,  # input file path or directory
        images_folder_path: str = None,
        classnames_file_path: str = None,
    ) -> BytesIO:
        return self.__convert(
            input_file,
            images_folder_path,
            classnames_file_path,
            self.reader.read_predictions,
            self.writer.write_predictions,
        )

    def __convert(
        self,
        input_file: str,
        images_folder_path: str,
        classnames_file_path: str,
        read_fn: Callable,
        write_fn: Callable,
    ) -> BytesIO:
        try:
            if self.input_file_type == self.output_file_type:
                file = get_file_content(input_file)
                return create_file(
                    data=file.read(),
                    filename=file.name,
                    extension=os.path.splitext(input_file)[1],
                )

            data = read_fn(input_file, images_folder_path, classnames_file_path)

            filename = "output"
            if os.path.isfile(input_file):
                filename = os.path.splitext(os.path.basename(input_file))[0]

            return write_fn(filename, data)
        except Exception as e:
            print(traceback.format_exc())
            raise ValueError(f"Invalid file: {str(e)}")
