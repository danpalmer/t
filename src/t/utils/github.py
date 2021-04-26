import click
import tinynetrc
from ghapi.all import GhApi, GhDeviceAuth

CLIENT_ID = "8db636a6ea034b12a053"
SCOPES = (
    "repo",
    "workflow",
    # "admin:org",
    # "gist",
    # "read:user",
)

# Doesn't actually matter, we just store against this locally
GITHUB_HOST = "api.github.com"


def authenticate() -> None:
    auth = GhDeviceAuth(CLIENT_ID, *SCOPES)
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