"""CLI entrypoint for chatbrowser."""

import click

from chatbrowser import __version__


@click.group()
@click.version_option(__version__, prog_name="chatbrowser")
def main() -> None:
    """chatbrowser command line interface."""
    # Add package-specific commands here. Prefer ChatStyle helpers for
    # interactive input when a command needs recoverable user input.


if __name__ == "__main__":
    main()
