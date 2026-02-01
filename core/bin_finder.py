"""Utility to locate the Sovereign browser binary (Camoufox/Firefox).
Centralizes discovery logic so callers and tests can rely on one behavior.
"""
from pathlib import Path
import os
import glob
import platform
import logging

LOG = logging.getLogger("bin_finder")


def find_sovereign_binary():
    """Return a Path to the browser binary or None if not found.

    Search order:
    1. LUCID_FIREFOX_BIN environment variable (explicit override)
    2. ./bin/firefox/firefox
    3. ./firefox/firefox
    4. obj-*/dist/bin/firefox (local build artifacts)
    5. Windows exe fallback: ./bin/firefox/firefox.exe
    """
    env_path = os.environ.get("LUCID_FIREFOX_BIN")
    if env_path:
        p = Path(env_path)
        if p.exists():
            LOG.info(f"Using LUCID_FIREFOX_BIN={p}")
            return p

    candidate = Path("./bin/firefox/firefox")
    if candidate.exists():
        return candidate

    candidate = Path("./firefox/firefox")
    if candidate.exists():
        return candidate

    for candidate_str in glob.glob("obj-*/dist/bin/firefox"):
        p = Path(candidate_str)
        if p.exists():
            LOG.info(f"Using discovered build artifact: {p}")
            return p

    if platform.system().lower().startswith("win"):
        win = Path("./bin/firefox/firefox.exe")
        if win.exists():
            return win

    return None
