from tenyks.dataset.aws.dataclasses import (
    AWSImagesLocation,
    AWSMetadataLocation,
    AWSS3Credentials,
)
from tenyks.dataset.config import ImagesMetadataLocation


def get_metadata_location(
    s3_metadata_uri: str,
    aws_access_key_id: str,
    aws_secret_access_key: str,
    aws_region: str,
):
    return (
        AWSMetadataLocation(
            type=ImagesMetadataLocation.AWS_S3.value,
            s3_uri=s3_metadata_uri,
            credentials=AWSS3Credentials(
                aws_access_key_id, aws_secret_access_key, aws_region
            ),
        )
        if s3_metadata_uri is not None
        else None
    )


def get_images_location(
    s3_images_uri: str,
    aws_access_key_id: str,
    aws_secret_access_key: str,
    aws_region: str,
):
    return (
        AWSImagesLocation(
            type=ImagesMetadataLocation.AWS_S3.value,
            s3_uri=s3_images_uri,
            credentials=AWSS3Credentials(
                aws_access_key_id, aws_secret_access_key, aws_region
            ),
        )
        if s3_images_uri is not None
        else None
    )
