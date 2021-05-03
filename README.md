# t – an engineering user interface

`t` is a template for creating an _organisation specific_ infrastructure tool.
Have you ever:

- Copy/pasted commands around to achieve tasks like getting a production
  shell or exporting some data.
- Searched your shell history, or Slack history, for the right incantation to
  scale a cluster.
- Written or read a [runbook](https://en.wikipedia.org/wiki/Runbook) and wished
  there was a good place to put a script for the process.

If you've done any of these it may be worth creating a tool for your
organisation that engineers can use to run automations and processes. Knowledge
will be kept in code rather than in chat histories, processes can be updated in
version control rather than in document edit history.

## Getting started

1. Click "Use this template" at the top of the repo on GitHub.
2. Set up your new repo, it's fine to make it private. Set this in
   `src/t/settings.py` so that updates work, and add a GitHub client ID if you
   want.
3. Rename to suit your team, we use `t` for `tool`/`template`/`thread`, but
   anything short will probably work well.
4. Start adding scripts to `src/t/scripts`. Any commands in files there will be
   picked up and added to the command line interface (we use
   [click](https://palletsprojects.com/p/click/) for the CLI).
5. Push to GitHub and let Actions build you a new version.
6. Hack `t` into what you need it to be. Swap out Actions for a different CI
   provider, Releases for a different distribution channel, change anything that
   will make `t` more useful for your team.
7. Have your team install `t` by downloading the latest release and putting it
   on their `PATH`.

## What is `t`?

`t` is a _template_ for this tool. It's designed to be forked, renamed, and
hacked to suit your team. Think of it as a starting point and some guidelines to
bootstrap some decision making and solve some of the early problems.

`t` is opinionated about a few things, specifically:

- That this engineering tool should be usable anywhere. `t` provides a static,
  relocatable binary that doesn't have any system dependencies beyond the OS.
- That the scripting should be done in Python. Python has libraries for almost
  everything, it's easily hackable to do most things, and it's quite high-level.
- That updates should be frequent and easy to apply. The tool should change as
  rapidly as necessary and the build process should support this.

## Best practices for using `t`

- Use `t` as a user interface, not a programmatic interface. Tools used by
  automated systems have different needs. `t` should prioritise human needs.
- Access production, but don't run in production. Breaking `t` should be an
  inconvenience not an outage.
- Rapidly iterate. Because `t` isn`t used in production it's safe to "move fast
  and break things".
- Don't over-automate. If a utility in `t` needs credentials for another system
  just check for them and bail out if they're not there, don't try to solve for
  every case.

## Why is `t` a template?

Because `t` uses PyOxidizer and provides a basic Continuous Integration, build,
and deployment process, it's not feasible to ship as a library. Plus, we'd
rather users took it as a starting point and hacked it into what they need than
tried to keep their codebases up to date with a changing framework.

---

## How it works

#### PyOxidizer

`t` uses [PyOxidizer](https://github.com/indygreg/PyOxidizer) to package up a
Python codebase and all of its dependencies into a static binary that can be
trivially installed on most development machines (currently Linux and macOS).

#### Click

`t` uses the `click` library to structure the CLI and as the backbone of the
tool. `click` normalises certain aspects of CLI development (e.g. providing
`--help`, normalising command names to `dash-case`), and provides a number of
utilities. Things like user prompts, colourised output, progress bars, are all
included in the library and work well together.

#### Updates

Updates are built with GitHub Actions and uploaded as a GitHub Release once
complete. `t` is able to check for available updates and update itself.

#### Development

```shell
# to run for development
pip install -e .
t

# to run as it would in real-world use
pyoxidizer run

# to build for release
pyoxidizer build --release
```

This project uses
[pip-compile-multi](https://pypi.org/project/pip-compile-multi/) for
hard-pinning dependencies versions. Please see its documentation for usage
instructions.

In short, `requirements/base/run.in` and `check.in` contain the list of direct
requirements necessary for running and validating the codebase. The
`app.in`/`ci.in`/`dev.in` files are for each use-case – running, CI, and
development, and pull in from the base files. The `txt` files are automatically
generated from the `in` files by adding recursive tree of dependencies with
fixed versions.

To upgrade dependency versions, run `pip-compile-multi`.

To add a new dependency without upgrade, add it to the right file, probably in
`base` and run `pip-compile-multi --no-upgrade`.

For installation always use `.txt` files. For example, command
`pip install -Ue . -r requirements/dev.txt` will install this project in
development mode, with testing requirements and development tools. Another
useful command is `pip-sync requirements/dev.txt`, it uninstalls packages from
your virtualenv that aren't listed in the file.

---

## Contributing

As this is a template for others to create tools, contributions will be accepted
based on how generally applicable they are to all. For example:

- Windows build support would be welcomed!
- A set of utilities for reading/writing configuration that could be re-used
  between many scripts would be welcomed.
- A script for archiving a directory to S3 would likely be too user-specific,
  and would not.

If you're unsure, start a discussion and ask!
