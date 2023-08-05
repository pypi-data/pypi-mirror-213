from dataclasses import dataclass

from dataclasses_json import dataclass_json

from tenyks.dataset.config import ImagesMetadataLocation


@dataclass_json
@dataclass
class AWSS3Credentials:
    aws_access_key_id: str
    aws_secret_access_key: str
    region_name: str


@dataclass_json
@dataclass
class AWSMetadataLocation:
    type: ImagesMetadataLocation
    s3_uri: str
    credentials: AWSS3Credentials


@dataclass_json
@dataclass
class AWSImagesLocation:
    type: ImagesMetadataLocation
    s3_uri: str
    credentials: AWSS3Credentials
