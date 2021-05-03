from .cli import autodiscover, cli

REPO = ("danpalmer", "t")  # https://github.com/danpalmer/t

def main():
    autodiscover()
    cli()


__all__ = (
    "autodiscover",
    "cli",
    "main",
    "REPO",
)
