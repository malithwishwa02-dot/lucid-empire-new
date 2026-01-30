import os
from pathlib import Path
import tempfile
import shutil
import pytest

from core.bin_finder import find_sovereign_binary


def touch(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"stub")


def test_respects_env_var(tmp_path, monkeypatch):
    bin_path = tmp_path / "foo" / "firefox"
    touch(bin_path)
    monkeypatch.setenv("LUCID_FIREFOX_BIN", str(bin_path))
    found = find_sovereign_binary()
    assert found is not None and Path(found) == bin_path


def test_prefers_bin_firefox(tmp_path, monkeypatch):
    cwd = tmp_path
    monkeypatch.chdir(cwd)
    bin_path = cwd / "bin" / "firefox" / "firefox"
    touch(bin_path)
    found = find_sovereign_binary()
    assert found is not None and Path(found).name == "firefox"


def test_fallback_to_root_firefox(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    root_bin = tmp_path / "firefox" / "firefox"
    touch(root_bin)
    found = find_sovereign_binary()
    assert found is not None and Path(found).parent.name == "firefox"


def test_none_when_missing(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    if "LUCID_FIREFOX_BIN" in os.environ:
        monkeypatch.delenv("LUCID_FIREFOX_BIN")
    found = find_sovereign_binary()
    assert found is None
