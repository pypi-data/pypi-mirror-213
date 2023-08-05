import click

from tenyks.adapters.config import DetectionFormat
from tenyks.adapters.detection.detection_adapter_factory import DetectionAdapterFactory
from tenyks.api import Api
from tenyks.click_utilities import must_not_have, required_for
from tenyks.config.config import VALID_IMAGE_EXTENSIONS, Config
from tenyks.dataset.upload_annotations import process_annotations_upload
from tenyks.dataset.upload_class_names import process_upload_class_names
from tenyks.dataset.utilities import get_images_location, get_metadata_location
from tenyks.upload_utilities import upload
from tenyks.utilities import get_key_from_name


@click.command()
@click.option(
    "--name", prompt="Enter dataset name", help="The name of the dataset to be created."
)
@click.option("--images", default=None, help="The path to image folder.")
@click.option("--annotations", default=None, help="The path to image annotation.")
@click.option(
    "--annotations_format",
    default=DetectionFormat.COCO.value,
    help="The annotation file type.",
    type=click.Choice(DetectionAdapterFactory.get_supported_input_formats()),
)
@click.option("--class_names", default=None, help="The path to class names file.")
@click.option(
    "--max_concurrent_uploads", default=20, help="Number of concurrent uploads."
)
@click.option("--verbose", is_flag=True, flag_value=True, help="Verbose flag.")
@click.option(
    "--s3_images_uri",
    default=None,
    help="Images bucket uri",
    callback=must_not_have(["images"]),
)
@click.option(
    "--s3_metadata_uri",
    default=None,
    help="Metadata bucket uri",
)
@click.option(
    "--aws_access_key_id",
    default=None,
    help="AWS access key id",
    callback=required_for(["s3_images_uri", "s3_metadata_uri"]),
)
@click.option(
    "--aws_secret_access_key",
    default=None,
    help="AWS secret access key",
    callback=required_for(["s3_images_uri", "s3_metadata_uri"]),
)
@click.option(
    "--aws_region",
    help="AWS region",
    default=None,
    callback=required_for(["s3_images_uri", "s3_metadata_uri"]),
)
def dataset_create(
    name: str,
    images: str,
    annotations: str,
    annotations_format: str,
    class_names: str,
    max_concurrent_uploads: int,
    verbose: bool,
    s3_images_uri: str,
    s3_metadata_uri: str,
    aws_access_key_id: str,
    aws_secret_access_key: str,
    aws_region: str,
):
    api = Api()

    images_location = get_images_location(
        s3_images_uri, aws_access_key_id, aws_secret_access_key, aws_region
    )
    metadata_location = get_metadata_location(
        s3_metadata_uri, aws_access_key_id, aws_secret_access_key, aws_region
    )
    dataset_key = process_create_dataset(api, name, images_location, metadata_location)

    if dataset_key is None:
        click.echo("Aborting...")
        return

    if images is not None:
        upload_url = f"{api.api_url}/workspaces/{Config.load().workspace_name}/datasets/{dataset_key}/images/files"
        upload(
            api,
            upload_url,
            images,
            "images",
            VALID_IMAGE_EXTENSIONS,
            max_concurrent_uploads,
            verbose,
        )
    if annotations is not None:
        process_annotations_upload(
            api, dataset_key, annotations, annotations_format, images, class_names
        )
    if class_names is not None:
        process_upload_class_names(api, dataset_key, class_names)


def process_create_dataset(
    api: Api, name: str, images_location, metadata_location
) -> str:
    config = Config.load()
    dataset_upload_url = f"/workspaces/{config.workspace_name}/datasets"
    payload = {
        "key": get_key_from_name(name),
        "display_name": name,
        "task_type": config.default_task_type,
    }
    if images_location is not None:
        payload["images_location"] = images_location.to_dict()

    if metadata_location is not None:
        payload["metadata_location"] = metadata_location.to_dict()

    click.echo(f"Creating dataset {name}...")
    response = api.post(dataset_upload_url, body=payload)

    dataset_key = response["key"]
    click.echo(f"Successfully created dataset with the following key: {dataset_key}")
    return dataset_key
