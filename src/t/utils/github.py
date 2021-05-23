import base64

import click
from ghapi.all import GhApi, GhDeviceAuth

from t.settings import GITHUB_CLIENT_ID, GITHUB_SCOPES
from t.utils.config import get_config, update_config


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
    user = api.users.get_authenticated()  # type: ignore

    with update_config() as config:
        config["github"] = {
            "login": user.login,
            "password": token,
        }


def get_authenticated_client() -> GhApi:
    return GhApi(token=get_config()["github"]["password"])


def check_authentication() -> bool:
    github = get_config().get("github", {})
    return bool(github.get("login") and github.get("password"))


def get_file_contents(owner, repo, path, ref):
    gh = get_authenticated_client()
    file_data = gh.repos.get_content(owner, repo, path, ref)  # type: ignore
    if file_data.encoding != "base64":
        raise ValueError(f"Unsupported encoding {file_data.encoding}")
    return base64.b64decode(file_data.content).decode("utf-8")
