def make_dist():
    return default_python_distribution()


def make_exe(dist):
    policy = dist.make_python_packaging_policy()

    python_config = dist.make_python_interpreter_config()

    # Work around https://github.com/indygreg/PyOxidizer/issues/307
    # This hack causes sys.argv[0] to be set to something reasonable, necessary
    # for most CLIs to work.
    python_config.run_command = "import t.__main__"
    # Once fixed can probably be simplified to this, equivalent of python -m t
    # python_config.run_module = "t"

    exe = dist.to_python_executable(
        name="t",

        # If no argument passed, the default `PythonPackagingPolicy` for the
        # distribution is used.
        packaging_policy=policy,

        # If no argument passed, the default `PythonInterpreterConfig` is used.
        config=python_config,
    )

    exe.add_python_resources(exe.pip_install(["-r", "requirements/app.txt"]))

    exe.add_python_resources(exe.read_package_root(
       path=".",
       packages=["t"],
    ))

    return exe

def make_embedded_resources(exe):
    return exe.to_embedded_resources()


def make_install(exe):
    files = FileManifest()
    files.add_python_resource(".", exe)
    return files


register_target("dist", make_dist)
register_target("exe", make_exe, depends=["dist"])
register_target("install", make_install, depends=["exe"], default=True)
register_target(
    "resources",
    make_embedded_resources,
    depends=["exe"],
    default_build_script=True,
)

resolve_targets()

# END OF COMMON USER-ADJUSTED SETTINGS.
PYOXIDIZER_VERSION = "0.13.2"
PYOXIDIZER_COMMIT = "UNKNOWN"
