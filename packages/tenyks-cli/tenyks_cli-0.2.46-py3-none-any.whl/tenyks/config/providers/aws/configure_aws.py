import click

from tenyks.config.providers.aws.config_aws import ConfigAws

aws_config = ConfigAws.load()


@click.command(name="configure-aws")
@click.option(
    "--access_key",
    prompt="Enter AWS access key",
    help="AWS access key",
    default=aws_config.aws_access_key_id,
)
@click.option(
    "--secret_key",
    prompt="Enter AWS Secret key",
    help="AWS secret key",
    hide_input=True,
    default=aws_config.get_masked_secret_key(),
)
@click.option(
    "--region",
    prompt="Enter S3 region",
    help="S3 region",
    default=aws_config.aws_region_name,
)
def configure_aws(access_key: str, secret_key: str, region: str):
    if secret_key == aws_config.get_masked_secret_key():
        # don't override the aws_secret_key with masked one
        secret_key = aws_config.aws_secret_access_key

    updated_configuration = ConfigAws(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        aws_region_name=region,
    )
    updated_configuration.save()
