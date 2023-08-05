import click

from tenyks.utilities import exit_application_with_message


class CatchAllExceptions(click.Group):
    def __call__(self, *args, **kwargs):
        try:
            return self.main(*args, **kwargs)
        except SystemExit:
            exit(0)
        except Exception as exc:
            exit_application_with_message(str(exc))
