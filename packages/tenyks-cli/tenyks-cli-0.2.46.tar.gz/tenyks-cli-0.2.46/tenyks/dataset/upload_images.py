import click

from tenyks.api import Api
from tenyks.config.config import VALID_IMAGE_EXTENSIONS, Config
from tenyks.upload_utilities import upload


@click.command()
@click.option(
    "--dataset_key",
    prompt="Enter dataset key",
    help="The key/ id of dataset that has been created.",
)
@click.option(
    "--images", prompt="Enter image folder path", help="The path to image folder."
)
@click.option(
    "--max_concurrent_uploads", default=20, help="Number of concurrent uploads."
)
@click.option("--verbose", is_flag=True, flag_value=True, help="Verbose flag.")
def dataset_images_upload(
    dataset_key: str, images: str, max_concurrent_uploads: int, verbose: bool
):
    api = Api()
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
