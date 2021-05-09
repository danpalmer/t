import base64

import click
import tinynetrc
from ghapi.all import GhApi, GhDeviceAuth

from t.settings import GITHUB_CLIENT_ID, GITHUB_SCOPES

# Doesn't actually matter, we just store against this locally
GITHUB_HOST = "api.github.com"


def authenticate() -> None:
    auth = GhDeviceAuth(GITHUB_CLIENT_ID, *GITHUB_SCOPES)
    click.prompt(
        f"Authenticate on GitHub with the code: {auth.user_code}\n"
        "Press enter to continue...",
        prompt_suffix="",
        default="",
        show_default=False,
    )
    auth.open_browser()
    token = auth.wait()
    api = GhApi(token=token)
    user = api.users.get_authenticated()
    netrc = tinynetrc.Netrc()
    netrc[GITHUB_HOST] = {
        "login": user.login,
        "password": token,
    }
    netrc.save()


def get_authenticated_client() -> GhApi:
    netrc = tinynetrc.Netrc()
    return GhApi(token=netrc[GITHUB_HOST]["password"])


def check_authentication() -> bool:
    netrc = tinynetrc.Netrc()
    github = netrc.get(GITHUB_HOST)
    return github.get("login") and github.get("password")


def get_file_contents(owner, repo, path, ref):
    gh = get_authenticated_client()
    file_data = gh.repos.get_content(owner, repo, path, ref)
    if file_data.encoding != "base64":
        raise ValueError(f"Unsupported encoding {file_data.encoding}")
    return base64.b64decode(file_data.content).decode("utf-8")
