import pathlib
import sys
from typing import Optional

import pkg_resources


def get_resource(path: pathlib.Path) -> Optional[bytes]:
    """
    Return a file handle on a named resource next to this module.

    File path must be within the "src/t/resources" directory.
    """

    if getattr(sys, "oxidized", False):
        name = path.name
        formatted_path = str(path.parent).replace("/", ".")
        reader = __loader__.get_resource_reader(  # type: ignore
            f"t.resources.{formatted_path}",
        )
        try:
            return reader.open_resource(name).read()
        except FileNotFoundError:
            return None
    else:
        return pkg_resources.resource_stream(
            "t",
            str(pathlib.Path("resources") / path),
        ).read()
