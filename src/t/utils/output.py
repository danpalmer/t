import sys
from typing import NoReturn, Optional

import click


def default(message: str, exit_with_code: Optional[int] = None) -> None:
    click.echo(message)
    if exit_with_code:
        sys.exit(exit_with_code)


def success(message: str) -> None:
    click.secho(message, fg="green")


def error(message: str, exit_with_code: Optional[int] = None) -> None:
    click.secho(message, fg="red", bold=True)
    if exit_with_code is not None:
        sys.exit(exit_with_code)


def fatal(message: str) -> NoReturn:  # type: ignore
    error(message, exit_with_code=1)
