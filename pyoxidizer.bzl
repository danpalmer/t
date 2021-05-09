def make_dist():
    return default_python_distribution()


def make_exe(dist):
    policy = dist.make_python_packaging_policy()
    policy.resources_location = "in-memory"
    policy.include_file_resources = True

    python_config = dist.make_python_interpreter_config()
    python_config.run_command = """import t; t.main()"""

    exe = dist.to_python_executable(
        name="t",

        # If no argument passed, the default `PythonPackagingPolicy` for the
        # distribution is used.
        packaging_policy=policy,

        # If no argument passed, the default `PythonInterpreterConfig` is used.
        config=python_config,
    )

    exe.add_python_resources(exe.pip_install(["-r", "requirements/app.txt"]))
    exe.add_python_resources(exe.setup_py_install(package_path="."))

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
