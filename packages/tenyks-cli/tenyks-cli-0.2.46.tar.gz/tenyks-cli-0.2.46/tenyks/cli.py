import click

from tenyks.config.configure import configure
from tenyks.config.providers.aws.configure_aws import configure_aws
from tenyks.convert.convert_detections_file import (
    convert_annotations,
    convert_predictions,
)
from tenyks.dataset.create_dataset import dataset_create
from tenyks.dataset.upload_annotations import dataset_annotations_upload
from tenyks.dataset.upload_class_names import dataset_class_names_upload
from tenyks.dataset.upload_images import dataset_images_upload
from tenyks.embeddings.upload_annotation_bbox_embeddings import (
    annotation_bbox_embedding_upload,
)
from tenyks.embeddings.upload_image_embeddings import image_embedding_upload
from tenyks.embeddings.upload_prediction_bbox_embeddings import (
    prediction_bbox_embedding_upload,
)
from tenyks.exceptions_handler import CatchAllExceptions
from tenyks.model.create_model import model_create
from tenyks.model.upload_predictions import model_predictions_upload


@click.group(cls=CatchAllExceptions)
def commands():
    pass


commands.add_command(configure)
commands.add_command(configure_aws)

commands.add_command(dataset_create)
commands.add_command(dataset_images_upload)
commands.add_command(dataset_annotations_upload)
commands.add_command(dataset_class_names_upload)
commands.add_command(model_create)
commands.add_command(model_predictions_upload)
commands.add_command(convert_annotations)
commands.add_command(convert_predictions)
commands.add_command(image_embedding_upload)
commands.add_command(annotation_bbox_embedding_upload)
commands.add_command(prediction_bbox_embedding_upload)
