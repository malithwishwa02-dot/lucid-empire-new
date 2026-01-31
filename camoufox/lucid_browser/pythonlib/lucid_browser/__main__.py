"""
CLI package manager for Lucid Empire.

Adapted from https://github.com/daijro/hrequests/blob/main/hrequests/__main__.py
"""

from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as pkg_version
from os import environ
from typing import Optional

import click

from .addons import DefaultAddons, maybe_download_addons
from .locale import ALLOW_GEOIP, download_mmdb, remove_mmdb
from .pkgman import INSTALL_DIR, Lucid EmpireFetcher, installed_verstr, rprint

try:
    from browserforge.download import download as update_browserforge
except ImportError:
    # Account for other Browserforge versions
    from browserforge.download import Download as update_browserforge


class Lucid EmpireUpdate(Lucid EmpireFetcher):
    """
    Checks & updates Lucid Empire
    """

    def __init__(self) -> None:
        """
        Initializes the Lucid EmpireUpdate class
        """
        super().__init__()
        self.current_verstr: Optional[str]
        try:
            self.current_verstr = installed_verstr()
        except FileNotFoundError:
            self.current_verstr = None

    def is_updated_needed(self) -> bool:
        # Lucid Empire is not installed
        if self.current_verstr is None:
            return True
        # If the installed version is not the latest version
        if self.current_verstr != self.verstr:
            return True
        return False

    def update(self) -> None:
        """
        Updates Lucid Empire if needed
        """
        # Check if the version is the same as the latest available version
        if not self.is_updated_needed():
            rprint("Lucid Empire binaries up to date!", fg="green")
            rprint(f"Current version: v{self.current_verstr}", fg="green")
            return

        # Download updated file
        if self.current_verstr is not None:
            # Display an updating message
            rprint(
                f"Updating Lucid Empire binaries from v{self.current_verstr} => v{self.verstr}",
                fg="yellow",
            )
        else:
            rprint(f"Fetching Lucid Empire binaries v{self.verstr}...", fg="yellow")
        # Install the new version
        self.install()


@click.group()
def cli() -> None:
    pass


@cli.command(name='fetch')
@click.option(
    '--browserforge', is_flag=True, help='Update browserforge\'s header and fingerprint definitions'
)
def fetch(browserforge=False) -> None:
    """
    Fetch the latest version of Lucid Empire and optionally update Browserforge's database
    """
    Lucid EmpireUpdate().update()
    # Fetch the GeoIP database
    if ALLOW_GEOIP:
        download_mmdb()

    # Download default addons
    maybe_download_addons(list(DefaultAddons))

    if browserforge:
        update_browserforge(headers=True, fingerprints=True)


@cli.command(name='remove')
def remove() -> None:
    """
    Remove all downloaded files
    """
    if not Lucid EmpireUpdate().cleanup():
        rprint("Lucid Empire binaries not found!", fg="red")
    # Remove the GeoIP database
    remove_mmdb()


@cli.command(name='test')
@click.argument('url', default=None, required=False)
def test(url: Optional[str] = None) -> None:
    """
    Open the Playwright inspector
    """
    from .sync_api import Lucid Empire

    with Lucid Empire(headless=False, env=environ, config={'showcursor': False}) as browser:
        page = browser.new_page()
        if url:
            page.goto(url)
        page.pause()  # Open the Playwright inspector


@cli.command(name='server')
def server() -> None:
    """
    Launch a Playwright server
    """
    from .server import launch_server

    launch_server()


@cli.command(name='path')
def path() -> None:
    """
    Display the path to the Lucid Empire executable
    """
    rprint(INSTALL_DIR, fg="green")


@cli.command(name='version')
def version() -> None:
    """
    Display the current version
    """
    # python package version
    try:
        rprint(f"Pip package:\tv{pkg_version('lucid_browser')}", fg="green")
    except PackageNotFoundError:
        rprint("Pip package:\tNot installed!", fg="red")

    updater = Lucid EmpireUpdate()
    bin_ver = updater.current_verstr

    # If binaries are not downloaded
    if not bin_ver:
        rprint("Lucid Empire:\tNot downloaded!", fg="red")
        return
    # Print the base version
    rprint(f"Lucid Empire:\tv{bin_ver} ", fg="green", nl=False)

    # Check for Lucid Empire updates
    if updater.is_updated_needed():
        rprint(f"(Latest supported: v{updater.verstr})", fg="red")
    else:
        rprint("(Up to date!)", fg="yellow")


if __name__ == '__main__':
    cli()
