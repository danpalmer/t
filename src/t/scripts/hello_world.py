import click

from t import cli


@cli.command(help="A greetings module to demonstrate how t works.")
@click.option("--name", default="world", help="Who to greet")
def hello_world():
    print("Hello world!")
