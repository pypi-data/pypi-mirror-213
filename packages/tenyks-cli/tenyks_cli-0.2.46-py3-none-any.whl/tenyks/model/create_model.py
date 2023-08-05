import click

from tenyks.adapters.config import DetectionFormat
from tenyks.adapters.detection.detection_adapter_factory import DetectionAdapterFactory
from tenyks.api import Api
from tenyks.config.config import Config
from tenyks.model.upload_predictions import process_upload_predictions
from tenyks.utilities import get_key_from_name


@click.command()
@click.option(
    "--name", prompt="Enter model name", help="The name of the model to be created."
)
@click.option(
    "--dataset_key",
    prompt="Enter dataset key",
    help="The key/ id of dataset that has been created.",
)
@click.option("--predictions", default=None, help="The path to model prediction.")
@click.option(
    "--predictions_format",
    default=DetectionFormat.COCO.value,
    help="The predictions file type.",
    type=click.Choice(DetectionAdapterFactory.get_supported_input_formats()),
)
@click.option(
    "--images",
    default=None,
    help="The path to image folder. Required for some predictions formats",
)
@click.option(
    "--iou_threshold",
    default=0.5,
    help="IoU threshold for model prediction.",
    type=click.FloatRange(0, 1),
)
@click.option(
    "--confidence_threshold",
    default=0.0,
    help="Confidence threshold for model prediction.",
    type=click.FloatRange(0, 1),
)
@click.option("--class_names", default=None, help="The path to class names file.")
def model_create(
    name: str,
    dataset_key: str,
    predictions: str,
    predictions_format: str,
    images: str,
    iou_threshold: float,
    confidence_threshold: float,
    class_names: str,
):
    api = Api()

    model_key = process_create_model(
        api, name, dataset_key, iou_threshold, confidence_threshold
    )
    if model_key is None:
        click.echo("Aborting...")
        return

    if predictions is not None:
        process_upload_predictions(
            api,
            dataset_key,
            model_key,
            predictions,
            predictions_format,
            images,
            class_names,
        )


def process_create_model(
    api: Api,
    name: str,
    dataset_key: str,
    iou_threshold: float,
    confidence_threshold: float,
) -> str:
    model_upload_url = f"/workspaces/{Config.load().workspace_name}/datasets/{dataset_key}/model_inferences"
    payload = {
        "key": get_key_from_name(name),
        "display_name": name,
        "iou_threshold": iou_threshold,
        "confidence_threshold": confidence_threshold,
    }
    click.echo(f"Creating model {name}...")
    response = api.post(model_upload_url, body=payload)

    model_key = response["key"]
    click.echo(
        f"Successfully creating model {name} with the following key: {model_key}"
    )
    return model_key
