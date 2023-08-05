import click

from tenyks.api import Api
from tenyks.config.config import Config
from tenyks.utilities import get_file_content


@click.command()
@click.option(
    "--dataset_key",
    prompt="Enter dataset key",
    help="The key/ id of dataset that has been created.",
)
@click.option(
    "--class_names",
    prompt="Enter path to class names",
    help="The path to class names file.",
)
def dataset_class_names_upload(dataset_key: str, class_names: str):
    api = Api()
    process_upload_class_names(api, dataset_key, class_names)


def process_upload_class_names(api: Api, dataset_key: str, class_names_path: str):
    data = get_file_content(class_names_path)
    class_upload_url = f"/workspaces/{Config.load().workspace_name}/datasets/{dataset_key}/classes/file"

    upload_class_names(api, class_upload_url, data)


def upload_class_names(api: Api, class_upload_url: str, data):
    click.echo("Uploading class names...")
    api.put(class_upload_url, files={"file": data})
    click.echo("Successfully ingest class names.")
