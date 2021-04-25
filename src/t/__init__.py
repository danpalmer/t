from .cli import autodiscover, cli


def main():
    autodiscover()
    cli()


__all__ = (
    "autodiscover",
    "cli",
    "main",
)
