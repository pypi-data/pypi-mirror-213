from typing import List

import click


def required_for(options: List[str]):
    def callback(ctx, param, value):
        for option in options:
            if (
                option in ctx.params
                and ctx.params[option] is not None
                and value is None
            ):
                raise click.BadParameter(f"Required when using --{option}")

        return value

    return callback


def must_not_have(options: List[str]):
    def callback(ctx, param, value):
        for option in options:
            if (
                option in ctx.params
                and ctx.params[option] is not None
                and value is not None
            ):
                raise click.BadParameter(f"Cannot be used with --{option}")

        return value

    return callback


def validate_all(validators):
    def callback(ctx, param, value):
        for validator in validators:
            validator(ctx, param, value)

        return value

    return callback
