# Packaging Lucid Empire as a .deb

This document describes how to build a .deb package of the Lucid Empire bundle.

Quick build (local):

1. Ensure you have dpkg tools: `sudo apt install dpkg-dev fakeroot rsync`
2. Run: `./camoufox/scripts/package_deb.sh [version]`
   - If you omit `[version]`, the script will try to use `git describe --tags --always` for a sensible default.
3. Output will be placed in `dist/`.

Reproducible Docker build:

  ./camoufox/scripts/build_deb_docker.sh 0.1.0~dev

Post-install notes:
- The package installs files to `/opt/lucid-empire` and creates `/usr/bin/lucid-empire`.
- To enable GUI, create a venv at `/opt/lucid-empire/venv` and run `pip install -r /opt/lucid-empire/gui_requirements.txt`.
- To automatically install GUI dependencies during package install set the env flag `INSTALL_REQUIREMENTS=1` at install time (e.g. `sudo env INSTALL_REQUIREMENTS=1 dpkg -i dist/*.deb`), or create `/etc/default/lucid-empire-install` containing `INSTALL_REQUIREMENTS=1` before installing the package.
- The package includes LICENSE files under `/usr/share/doc/lucid-empire/` and contains a `copyright` file indicating MPL-2.0.

