import pathlib
import platform
import stat
import sys

import click
import httpx

from t import REPO, cli
from t.__version__ import VERSION
from t.utils import github


@cli.command()
def check_for_update():
    releases = get_available_releases()
    if not releases:
        click.secho("No releases found", fg="red", bold=True)
        sys.exit(1)

    update = get_update(releases)
    if not update:
        click.echo("No update available")
        sys.exit(0)

    try:
        asset = get_asset(update)
    except UnsupportedPlatform as e:
        click.secho(str(e), fg="red", bold=True)
        sys.exit(1)

    click.secho("New version found", fg="green")
    click.echo(f"  {VERSION} => {update.tag_name} {asset.browser_download_url}")
    click.echo("  Update with `t self-update` or download manually")


@cli.command()
@click.option(
    "--path",
    type=pathlib.Path,
    default=pathlib.Path(sys.executable),
    help="Override install path",
)
def self_update(path: pathlib.Path) -> None:
    if "python" in path.name:
        click.secho("Aborting update!", fg="red", bold=True)
        click.echo("It looks like you're running in development mode.")
        sys.exit(1)

    if not click.confirm(f"This will update the binary at {path}"):
        click.secho("Aborting update!", fg="red", bold=True)
        sys.exit(1)

    releases = get_available_releases()
    if not releases:
        click.secho("No releases found", fg="red", bold=True)
        sys.exit(1)

    update = get_update(releases)
    if not update:
        click.echo("No update available")
        sys.exit(0)

    try:
        asset = get_asset(update)
    except UnsupportedPlatform as e:
        click.secho(str(e), fg="red", bold=True)
        sys.exit(1)

    github_client = github.get_authenticated_client()

    with path.open("wb") as f:
        click.echo(f"Downloading {asset.url}")

        with httpx.stream(
            "GET",
            asset.url,
            headers={
                **github_client.headers,
                "User-Agent": "t",
                "Accept": "application/octet-stream",
            },
        ) as response:
            response.raise_for_status()

            with click.progressbar(response.iter_bytes()) as bar:
                for chunk in bar:
                    f.write(chunk)

    path.chmod(stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)


def get_available_releases():
    gh = github.get_authenticated_client()
    return gh.repos.list_releases(*REPO)


def get_update(releases):
    latest_release = releases[0]
    new_version = int(latest_release.tag_name[1:])

    try:
        current_version = int(VERSION)
    except ValueError:
        current_version = -1

    if new_version <= current_version:
        return None

    return latest_release


def get_asset(release):
    rust_triple = get_platform_name()
    try:
        return next(x for x in release.assets if x.name.startswith(rust_triple))
    except StopIteration:
        raise UnsupportedPlatform(
            f"No compatible asset found on release '{release.name}' "
            f"for platform {rust_triple}",
        )


def get_platform_name():
    if sys.platform.startswith("darwin"):
        if platform.machine() == "arm64":
            return "macos-arm64"
        return "macos-x86_64"
    if sys.platform.startswith("linux"):
        return "linux-x86_64"


class UnsupportedPlatform(ValueError):
    pass
