import click

from tenyks.adapters.config import DetectionFormat
from tenyks.adapters.detection.detection_adapter_factory import DetectionAdapterFactory
from tenyks.convert.detection_file_processor import DetectionFileProcessor
from tenyks.utilities import write_file


@click.command()
@click.option(
    "--annotations",
    prompt="Enter annotations file path",
    help="The path to image annotations.",
)
@click.option(
    "--input_format",
    prompt="Enter annotations file type",
    type=click.Choice(DetectionAdapterFactory.get_supported_input_formats()),
)
@click.option(
    "--output_format",
    type=click.Choice(DetectionAdapterFactory.get_supported_output_formats()),
    default=DetectionFormat.COCO.value,
)
@click.option("--images", default=None, help="The path to image folder.")
@click.option("--class_names", default=None, help="The path to class names file.")
def convert_annotations(
    annotations: str,
    input_format: str,
    output_format: str,
    images: str,
    class_names: str,
):
    output = DetectionFileProcessor.process_annotations_file(
        annotations, input_format, output_format, images, class_names
    )
    write_file(output)


@click.command()
@click.option(
    "--predictions",
    prompt="Enter predictions file path",
    help="The path to image predictions.",
)
@click.option(
    "--input_format",
    prompt="Enter predictions file type",
    type=click.Choice(DetectionAdapterFactory.get_supported_input_formats()),
)
@click.option(
    "--output_format",
    type=click.Choice(DetectionAdapterFactory.get_supported_output_formats()),
    default=DetectionFormat.COCO.value,
)
@click.option("--images", default=None, help="The path to image folder.")
@click.option("--class_names", default=None, help="The path to class names file.")
def convert_predictions(
    predictions: str,
    input_format: str,
    output_format: str,
    images: str,
    class_names: str,
):
    output = DetectionFileProcessor.process_predictions_file(
        predictions, input_format, output_format, images, class_names
    )
    write_file(output)
