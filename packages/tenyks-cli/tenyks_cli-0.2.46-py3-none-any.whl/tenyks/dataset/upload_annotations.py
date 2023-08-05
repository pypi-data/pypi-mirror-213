import click

from tenyks.adapters.config import DetectionFormat
from tenyks.adapters.detection.detection_adapter_factory import DetectionAdapterFactory
from tenyks.api import Api
from tenyks.config.config import Config
from tenyks.convert.detection_file_processor import DetectionFileProcessor


@click.command()
@click.option(
    "--dataset_key",
    prompt="Enter dataset key",
    help="The key/ id of dataset that has been created.",
)
@click.option(
    "--annotations",
    prompt="Enter annotation file path",
    help="The path to image annotation.",
)
@click.option(
    "--format",
    help="Enter annotation file type",
    type=click.Choice(DetectionAdapterFactory.get_supported_input_formats()),
    default=DetectionFormat.COCO.value,
)
@click.option(
    "--images",
    help="The path to image folder.",
    default=None,
)
@click.option(
    "--class_names",
    help="The path to the class names file.",
    default=None,
)
def dataset_annotations_upload(
    dataset_key: str, annotations: str, format: str, images: str, class_names: str
):
    api = Api()
    process_annotations_upload(
        api, dataset_key, annotations, format, images, class_names
    )


def process_annotations_upload(
    api: Api,
    dataset_key: str,
    annotations_path: str,
    format: str,
    images_dir: str,
    class_names_dir: str = None,
):
    data = DetectionFileProcessor.process_annotations_file(
        annotations_path,
        format,
        DetectionFormat.COCO.value,
        images_dir,
        class_names_dir,
    )
    annotation_upload_url = f"/workspaces/{Config.load().workspace_name}/datasets/{dataset_key}/images/annotations"
    upload_annotations(api, annotation_upload_url, data)


def upload_annotations(api: Api, annotation_upload_url: str, data):
    click.echo("Uploading annotations...")
    api.put(annotation_upload_url, files={"file": data})
    click.echo("Successfully ingested annotations.")
