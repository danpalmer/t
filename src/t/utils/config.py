import contextlib
import json

import xdg

from . import output

CONFIG_LOCATION = xdg.xdg_config_home() / "t.json"


def get_config():
    try:
        config_text = CONFIG_LOCATION.read_text()
    except FileNotFoundError:
        config_text = None

    if config_text:
        try:
            return json.loads(config_text)
        except json.JSONDecodeError:
            output.error("Error decoding config, it may be corrupted,")
            output.error(f"{str(CONFIG_LOCATION)} should be a valid JSON file")
            return {}
    else:
        return {}


@contextlib.contextmanager
def update_config():
    config = get_config()

    yield config

    try:
        config_text = json.dumps(config)
    except ValueError:
        output.error("Error encoding config to JSON, not persisting config change")
        return

    CONFIG_LOCATION.write_text(config_text)
