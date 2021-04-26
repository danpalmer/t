import click

from t import cli
from t.utils import github


@cli.group(help="Configuration for t")
def config():
    pass


@config.command(help="Check configuration setup")
def check():
    if not github.check_authentication():
        click.secho("Missing GitHub token", fg="red")
    else:
        click.secho("GitHub token set")


@config.command(help="Sign in to GitHub to enable related features")
def github_login():
    github.authenticate()
