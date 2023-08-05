import configparser
import os
from dataclasses import asdict, dataclass

VALID_IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png"]
VALID_ACTIVATION_EXTENSIONS = [".npy"]
RETRIES_PER_FILE = 3
DEFAULT_CONFIG_SECTION = "default"


@dataclass
class Config:
    api_url: str = "https://dashboard.tenyks.ai/api"
    username: str = None
    password: str = None
    workspace_name: str = "tenyks"
    default_task_type: str = "object_detection"

    def get_default_task_types(self):
        return ["object_detection"]

    def get_masked_password(self):
        if self.password:
            return f"{len(self.password[:-4]) * '#'} {self.password[-4:]}"

        return self.password

    def save(self):
        config = Config.read_config()
        config[DEFAULT_CONFIG_SECTION] = asdict(self)
        Config.write_config(config)

    @classmethod
    def load(cls):
        config_parser = Config.read_config()
        if DEFAULT_CONFIG_SECTION in config_parser:
            return cls(**config_parser[DEFAULT_CONFIG_SECTION])

        return cls()

    @classmethod
    def get_credentials_file_path(cls):
        dir_path = os.path.expanduser("~/.tenyks")
        os.makedirs(dir_path, exist_ok=True)
        return os.path.expanduser("~/.tenyks/credentials")

    @classmethod
    def read_config(cls) -> configparser.ConfigParser:
        config_parser = configparser.ConfigParser()
        config_parser.read(Config.get_credentials_file_path())

        return config_parser

    @classmethod
    def write_config(cls, config: configparser.ConfigParser) -> None:
        credentials_path = Config.get_credentials_file_path()
        with open(credentials_path, "w") as config_file:
            config.write(config_file)
