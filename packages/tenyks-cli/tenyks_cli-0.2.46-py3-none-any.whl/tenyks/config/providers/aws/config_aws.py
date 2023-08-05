from dataclasses import asdict, dataclass

from tenyks.config.config import Config

AWS_CONFIG_SECTION = "default.aws"


@dataclass
class ConfigAws:
    aws_access_key_id: str = None
    aws_secret_access_key: str = None
    aws_region_name: str = None

    def get_masked_secret_key(self):
        if self.aws_secret_access_key:
            return f"{len(self.aws_secret_access_key[:-4]) * '#'} {self.aws_secret_access_key[-4:]}"

        return self.aws_secret_access_key

    def save(self):
        config = Config.read_config()
        config[AWS_CONFIG_SECTION] = asdict(self)
        Config.write_config(config)

    @classmethod
    def load(cls):
        config_parser = Config.read_config()
        if config_parser.has_section(AWS_CONFIG_SECTION):
            return cls(**config_parser[AWS_CONFIG_SECTION])

        return cls()
