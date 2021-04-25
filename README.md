⚠️Warning: Experimental⚠️

This is liable to change and is full of half baked ideas.

# t – an interface to Thread

The `t` tool defines the canonical ways to achieve various tasks in Thread's
infrastructure and systems.

`t` is designed for humans, not for computers. Interfaces should be easy to use
and `t` should always run on a development machine.

### How it works

##### PyOxidizer

`t` is a PyOxidizer project. That means there are some things to bear in mind.
The advantage of this is that we get a single static binary that has no runtime
dependencies on virtualenvs, Python versions, etc, but we do need a Rust
toolchain to compile it and there are some limitations to how it runs as all
files have to be embedded and Python versions availability is limited.

##### Click

We use the `click` library to structure the CLI and as the backbone of the tool.
`click` normalises certain aspects of CLI development (e.g. providing `--help`,
normalising command names to `dash-case`), and provides a number of utilities.
Things like user prompts, colourised output, progress bars, are all included in
the library and work well together.

##### Updates

TODO: How do updates work?

### Development

```shell
# to run for development
pip install -e .
t

# to run as it would in real-world use
pyoxidizer run

# to build
pyoxidizer build --release
```
