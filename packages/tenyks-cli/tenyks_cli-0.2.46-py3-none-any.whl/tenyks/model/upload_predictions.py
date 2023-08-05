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
    "--model_key",
    prompt="Enter model key",
    help="The key/ id of model that has been created.",
)
@click.option(
    "--predictions",
    prompt="Enter prediction file path",
    help="The path to prediction.",
)
@click.option(
    "--format",
    prompt="Enter prediction file type",
    help="The prediction file type.",
    type=click.Choice(DetectionAdapterFactory.get_supported_input_formats()),
    default=DetectionFormat.COCO.value,
)
@click.option(
    "--images",
    default=None,
    help="The path to image folder. Required for some predictions formats",
)
@click.option("--class_names", default=None, help="The path to class names file.")
def model_predictions_upload(
    dataset_key: str,
    model_key: str,
    predictions: str,
    format: str,
    images: str,
    class_names: str,
):
    api = Api()

    process_upload_predictions(
        api, dataset_key, model_key, predictions, format, images, class_names
    )


def process_upload_predictions(
    api: Api,
    dataset_key: str,
    model_key: str,
    predictions_file_path: str,
    format: str,
    images_dir: str,
    class_names_dir: str,
):
    prediction_upload_url = (
        f"/workspaces/{Config.load().workspace_name}/datasets/{dataset_key}"
        f"/model_inferences/{model_key}/predictions"
    )
    data = DetectionFileProcessor.process_predictions_file(
        predictions_file_path,
        format,
        DetectionFormat.COCO.value,
        images_dir,
        class_names_dir,
    )
    click.echo("Uploading model predictions...")
    api.put(prediction_upload_url, files={"file": data})
    click.echo("Successfully ingested model predictions.")
