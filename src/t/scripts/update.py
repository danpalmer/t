import pathlib
import platform
import stat
import sys
import tarfile
import tempfile
from typing import Any, List, Tuple

import click
import httpx

from t import cli
from t.__version__ import VERSION
from t.settings import UPDATE_REPO
from t.utils import github, output


@cli.command(help=f"Check {'/'.join(UPDATE_REPO)} for updates")
@click.option(
    "--repo",
    type=(str, str),
    metavar=" ".join(UPDATE_REPO),
    default=UPDATE_REPO,
)
def check_for_update(repo: Tuple[str, str]) -> None:
    releases = get_available_releases(repo)
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
@click.option(
    "--repo",
    type=(str, str),
    metavar=" ".join(UPDATE_REPO),
    default=UPDATE_REPO,
)
@click.option(
    "--force",
    is_flag=True,
    help="Update to latest regardless of version",
)
def self_update(path: pathlib.Path, repo: Tuple[str, str], force: bool) -> None:
    if "python" in path.name:
        output.fatal("Aborting update! (Looks like your in dev mode)")

    output.default(f"Updating {path} from {'/'.join(repo)}")
    if not click.confirm("Continue?"):
        output.fatal("Aborting update")

    releases = get_available_releases(repo)
    if not releases:
        output.fatal("No releases found")

    update = get_update(releases, force=force)
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


def get_available_releases(repo: Tuple[str, str]) -> List[Any]:
    gh = github.get_authenticated_client()

    try:
        return gh.repos.list_releases(*repo)
    except Exception:
        output.fatal("Failed to get releases, have you run `config github-login`?")


def get_update(releases: List[Any], force=False) -> Any:
    latest_release = releases[0]
    if force:
        return latest_release

    new_version = int(latest_release.tag_name[1:])

    if VERSION == "dev":
        current_version = -1
    else:
        current_version = int(VERSION[1:])

    if new_version <= current_version:
        return None

    return latest_release


def get_asset(release: Any) -> Any:
    platform = get_platform_name()
    try:
        return next(x for x in release.assets if x.name.startswith(platform))
    except StopIteration:
        raise UnsupportedPlatform(
            f"No compatible asset found on release '{release.name}' "
            f"for platform {platform}",
        )


def get_platform_name() -> str:
    if sys.platform.startswith("darwin"):
        if platform.machine() == "arm64":
            return "macos-arm64"
        return "macos-x86_64"
    if sys.platform.startswith("linux"):
        return "linux-x86_64"


class UnsupportedPlatform(ValueError):
    pass
