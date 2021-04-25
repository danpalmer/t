import importlib
import pkgutil

import click

from . import scripts
from .__version__ import VERSION


@click.group(name="t")
@click.version_option(VERSION, "-v", "--version")
@click.help_option("-h", "--help")
def cli():
    """Interface to Thread's systems and infrastructure."""
    pass


def autodiscover():
    for _, name, _ in pkgutil.walk_packages(scripts.__path__):
        importlib.import_module(f"{scripts.__name__}.{name}")
