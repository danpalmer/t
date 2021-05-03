import click

from t import cli
from t.utils import output


@cli.command(help="A greetings module to demonstrate how t works.")
@click.option("--name", default="world", help="Who to greet")
def hello_world(name):
    output.success(f"Hello {name}!")
