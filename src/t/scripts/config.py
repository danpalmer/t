import click

from t import cli
from t.utils import github, output


@cli.group(help="Configuration for t")
def config():
    pass


@config.command(help="Sign in to GitHub to enable related features")
@click.option("--force", is_flag=True, help="Force sign in even if credentials exist.")
def github_login(force):
    if force or not github.check_authentication():
        github.authenticate()
    else:
        output.default("Already logged in to GitHub")
