import click

from tenyks.config.config import Config

current_config = Config.load()


@click.command()
@click.option(
    "--api_url",
    prompt="Enter API URL",
    help="The tenyks api url",
    default=current_config.api_url,
)
@click.option(
    "--username",
    prompt="Enter tenyks username",
    help="The tenyks username",
    default=current_config.username,
)
@click.option(
    "--password",
    prompt="Enter tenyks password",
    help="The tenyks password",
    hide_input=True,
    default=current_config.get_masked_password(),
)
@click.option(
    "--workspace_name",
    prompt="Enter tenyks workspace name",
    help="The tenyks workspace name",
    prompt_required=False,
    default=current_config.workspace_name,
)
@click.option(
    "--default_task_type",
    prompt="Enter tenyks default task type",
    help="Enter tenyks default task type",
    prompt_required=False,
    default=current_config.default_task_type,
    type=click.Choice(current_config.get_default_task_types(), case_sensitive=True),
)
def configure(
    api_url: str,
    username: str,
    password: str,
    workspace_name: str,
    default_task_type: str,
):
    if password == current_config.get_masked_password():
        # don't override the password with masked one
        password = current_config.password

    Config(
        api_url=api_url,
        username=username,
        password=password,
        workspace_name=workspace_name,
        default_task_type=default_task_type,
    ).save()
