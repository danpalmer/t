import sys

import click


def default(message, exit_with_code=None):
    click.echo(message)
    if exit_with_code:
        sys.exit(exit_with_code)


def success(message):
    click.secho(message, fg="green")


def error(message, exit_with_code=None):
    click.secho(message, fg="red", bold=True)
    if exit_with_code is not None:
        sys.exit(exit_with_code)


def fatal(message):
    error(message, exit_with_code=1)
