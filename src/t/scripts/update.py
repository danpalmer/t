import pathlib
import platform
import stat
import sys
import tarfile
import tempfile

import click
import httpx

from t import cli
from t.__version__ import VERSION
from t.settings import UPDATE_REPO
from t.utils import github, output


@cli.command(help=f"Check {'/'.join(UPDATE_REPO)} for updates")
def check_for_update():
    releases = get_available_releases()
    if not releases:
        output.fatal("No releases found")

    update = get_update(releases)
    if not update:
        output.default("No update available", exit_with_code=0)

    try:
        asset = get_asset(update)
    except UnsupportedPlatform as e:
        output.fatal(str(e))

    output.success("New version found")
    output.default(f"  {VERSION} => {update.tag_name} {asset.browser_download_url}")
    output.default("  Update with `t self-update` or download manually")


@cli.command(help=f"Update to the latest release from {'/'.join(UPDATE_REPO)}")
@click.option(
    "--path",
    type=pathlib.Path,
    default=pathlib.Path(sys.executable),
    help="Override install path",
)
def self_update(path: pathlib.Path) -> None:
    if "python" in path.name:
        output.fatal("Aborting update! (Looks like your in dev mode)")

    if not click.confirm(f"This will update the binary at {path}"):
        output.fatal("Aborting update!")

    releases = get_available_releases()
    if not releases:
        output.fatal("No releases found")

    update = get_update(releases)
    if not update:
        output.default("No update available", exit_with_code=0)

    try:
        asset = get_asset(update)
    except UnsupportedPlatform as e:
        output.fatal(str(e))

    github_client = github.get_authenticated_client()

    with tempfile.TemporaryDirectory() as tempdir:
        temp_asset_path = pathlib.Path(tempdir) / asset.name

        with temp_asset_path.open("wb") as f:
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

        tar = tarfile.open(temp_asset_path)
        tar_members = tar.getmembers()
        if not tar_members:
            output.fatal("No items in release archive")
            return

        binary_contents = tar.extractfile(tar_members[0].name)
        if binary_contents is None:
            output.fatal("Could not extract 't' from release archive")
            return

        path.write_bytes(binary_contents.read())
        path.chmod(stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)


def get_available_releases():
    gh = github.get_authenticated_client()

    try:
        return gh.repos.list_releases(*UPDATE_REPO)
    except Exception:
        output.fatal("Failed to get releases, have you run `config github-login`?")


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
    platform = get_platform_name()
    try:
        return next(x for x in release.assets if x.name.startswith(platform))
    except StopIteration:
        raise UnsupportedPlatform(
            f"No compatible asset found on release '{release.name}' "
            f"for platform {platform}",
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
