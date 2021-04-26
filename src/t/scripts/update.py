import sys

import click

from t import cli
from t.__version__ import VERSION
from t.utils import github

OWNER = "danpalmer"
REPO = "t"


@cli.command()
def check_for_update():
    gh = github.get_authenticated_client()
    releases = gh.repos.list_releases(OWNER, REPO)
    if not releases:
        click.secho("No releases found", fg="red", bold=True)
        sys.exit(1)

    latest_release = releases[0]
    new_version = int(latest_release.tag_name)

    try:
        current_version = int(VERSION)
    except ValueError:
        current_version = -1

    if new_version > current_version:
        click.secho("New version found", fg="green")
        click.echo(f"  {VERSION} => {new_version}")

        download_urls = {
            x.name.replace("t-", "", 1): x.browser_download_url
            for x in latest_release.assets
        }
        click.echo(download_urls)
