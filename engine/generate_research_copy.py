#!/usr/bin/env python3
import os
import shutil
import fnmatch

# CONFIGURATION
SOURCE_DIR = "."
DEST_DIR = os.path.join(os.path.dirname(SOURCE_DIR), "lucid-empire-research-v2")
MAX_FILE_SIZE = 500 * 1024  # 500KB limit per file (prevents accidental asset copy)

# WHITELIST: Only copy these extensions (The "Brain" of the system)
INCLUDE_EXTENSIONS = {
    '.py', '.c', '.cpp', '.h', '.hpp',   # Source Code
    '.patch',                            # Engine Hardening
    '.sh', '.yml', '.yaml', '.toml',     # Orchestration & Config
    '.json', '.js', '.cfg',              # Browser Preferences
    '.md', '.txt', 'Dockerfile', 'Makefile' # Documentation & Build
}

# BLACKLIST: Explicitly ignore these heavy directories (The "Body" of the system)
IGNORE_DIRS = {
    'bin',           # Compiled Browser Binaries
    'build', 'dist', # Build Artifacts
    'fonts',         # Large font assets (mentioned in README_RESEARCH)
    '__pycache__',
    '.git',
    '.idea', '.vscode', # IDE configs
    'node_modules', 'bundle', 'lucid_browser'
}

# CRITICAL PATHS: Ensure these exist even if empty (Maintain Directory Structure)
CRITICAL_STRUCTURE = [
    "core",
    "modules",
    "patches",
    "network",
    "additions/camoucfg",
    "pythonlib/camoufox",
    "lucid_profile_data/default"
]


def is_safe_to_copy(filename, file_path):
    # Check 1: Extension Whitelist
    _, ext = os.path.splitext(filename)
    if ext not in INCLUDE_EXTENSIONS and filename not in INCLUDE_EXTENSIONS:
        return False

    # Check 2: File Size Cap (Safety net for unlisted binary assets)
    try:
        if os.path.getsize(file_path) > MAX_FILE_SIZE:
            print(f"[SKIP] Too Large: {filename}")
            return False
    except OSError:
        return False

    return True


def ensure_critical_structure(dest_root):
    for p in CRITICAL_STRUCTURE:
        path = os.path.join(dest_root, p)
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)


def main():
    # DEST_DIR is outside SOURCE_DIR by design; normalize
    dest = os.path.abspath(DEST_DIR)
    if os.path.exists(dest):
        print(f"Removing existing build: {dest}")
        shutil.rmtree(dest)

    print(f"Starting Extraction -> {dest}...")

    files_copied = 0
    total_size = 0

    for root, dirs, files in os.walk(SOURCE_DIR):
        # 1. Modify dirs in-place to skip ignored directories
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

        # Skip the destination directory if it lives under SOURCE_DIR
        rel_path = os.path.relpath(root, SOURCE_DIR)
        if rel_path.startswith(os.path.relpath(dest, SOURCE_DIR)):
            continue

        dest_path = os.path.join(dest, rel_path) if rel_path != '.' else dest

        if not os.path.exists(dest_path):
            os.makedirs(dest_path, exist_ok=True)

        for f in files:
            src_file = os.path.join(root, f)

            if is_safe_to_copy(f, src_file):
                try:
                    shutil.copy2(src_file, os.path.join(dest_path, f))
                    files_copied += 1
                    total_size += os.path.getsize(src_file)
                except Exception as e:
                    print(f"[ERROR] Copy failed: {src_file} -> {e}")

    # Ensure critical structure exists
    ensure_critical_structure(dest)

    # Post-Processing: Create README_RESEARCH.md if strictly needed
    research_note = os.path.join(dest, "README_RESEARCH.md")
    with open(research_note, "w", encoding="utf-8") as f:
        f.write("# Lucid Empire (Research Copy)\n")
        f.write("stripped-down version containing only source logic and patches.\n")
        f.write("Binaries and assets removed to minimize footprint.\n")

    print(f"\n[COMPLETE] Copied {files_copied} files.")
    print(f"Total Size: {total_size / 1024 / 1024:.2f} MB")
    print(f"Output: {dest}")


if __name__ == "__main__":
    main()
