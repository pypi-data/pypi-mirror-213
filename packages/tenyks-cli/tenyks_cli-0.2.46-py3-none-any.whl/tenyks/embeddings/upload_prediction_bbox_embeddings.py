import click

from tenyks.api import Api
from tenyks.config.config import VALID_ACTIVATION_EXTENSIONS, Config
from tenyks.upload_utilities import upload


@click.command()
@click.option(
    "--dataset_key",
    prompt="Enter dataset key",
    help="The key/ id of dataset that has been created.",
)
@click.option(
    "--model_key",
    prompt="Enter model key",
    help="The id of the model for which these embeddings belong.",
)
@click.option(
    "--embeddings",
    prompt="Enter embedding folder path",
    help="The path to activations folder.",
)
@click.option(
    "--embedding_name",
    prompt="Enter embedding name",
    help="A name for the embeddings which will be visible in the UI",
)
@click.option(
    "--max_concurrent_uploads", default=20, help="Number of concurrent uploads."
)
@click.option("--verbose", is_flag=True, flag_value=True, help="Verbose flag.")
def prediction_bbox_embedding_upload(
    dataset_key: str,
    model_key: str,
    embeddings: str,
    embedding_name: str,
    max_concurrent_uploads: int,
    verbose: bool,
):
    api = Api()
    upload_url = (
        f"{api.api_url}/workspaces/{Config.load().workspace_name}"
        f"/datasets/{dataset_key}/{model_key}/prediction_bounding_box_embeddings/{embedding_name}"
    )
    upload(
        api,
        upload_url,
        embeddings,
        "annotation bounding box embeddings",
        VALID_ACTIVATION_EXTENSIONS,
        max_concurrent_uploads,
        verbose,
    )
