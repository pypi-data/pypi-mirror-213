from enum import Enum


class ImagesMetadataLocation(str, Enum):
    LOCAL = "local"
    AWS_S3 = "aws_s3"
