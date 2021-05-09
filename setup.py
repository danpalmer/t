import os
import pathlib

from setuptools import find_packages, setup

VERSION = os.environ.get("VERSION", "dev")
VERSION_FILE = pathlib.Path("src/t/__version__.py")

if os.environ.get("PYOXIDIZER") is not None:
    original_version_text = VERSION_FILE.read_text()
    VERSION_FILE.write_text(original_version_text.replace("dev", VERSION))

setup(
    name="t",
    version=VERSION,
    author="Thread engineering",
    author_email="tech@thread.com",
    description="Interface to Thread's systems and processes.",
    license="PROPRIETARY",
    url="https://github.com/thread/t",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={"t": ["src/t/resources/**/*"]},
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: Other/Proprietary License",
        "Private :: Do not Upload",
    ],
    entry_points={"console_scripts": ["t-dev=t.__main__:main"]},
)

if os.environ.get("PYOXIDIZER") is not None:
    VERSION_FILE.write_text(original_version_text)
