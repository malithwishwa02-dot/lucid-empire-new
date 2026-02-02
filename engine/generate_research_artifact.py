#!/usr/bin/env python3
import os
import shutil
import logging

# CONFIGURATION
SOURCE_DIR = "lucid-empire-research-v2"
DEST_DIR = "lucid-research-artifact"
MAX_FILE_SIZE = 500 * 1024  # 500KB hard limit (Filters out .o, .exe, .dll, etc.)

# WHITELIST: The Logic & Orchestration Layer
INCLUDE_EXTENSIONS = {
    '.py', '.c', '.cpp', '.h', '.hpp', '.js',
    '.json', '.yaml', '.yml', '.toml', '.cfg', '.ini',
    '.sh', '.patch', 'Dockerfile', 'Makefile',
    '.md', '.txt'
}

# BLACKLIST: Explicitly ignore heavy/build directories
IGNORE_DIRS = {
    '__pycache__', '.git', '.idea', '.vscode', 'bin', 'build', 'dist', 'fonts', 'node_modules', 'egg-info'
}

# CRITICAL COMPONENTS (Validation)
CRITICAL_COMPONENTS = [
    "core/genesis_engine.py",
    "additions/camoucfg/MaskConfig.hpp",
    "modules/commerce_injector.py",
    "patches/lucid-navigator.patch",
    "lucid_launcher.py"
]


def setup_logger():
    logging.basicConfig(level=logging.INFO, format='%(message)s')


def is_safe_copy(filename, file_path):
    _, ext = os.path.splitext(filename)
    if ext.lower() not in INCLUDE_EXTENSIONS and filename not in INCLUDE_EXTENSIONS:
        return False
    try:
        if os.path.getsize(file_path) > MAX_FILE_SIZE:
            logging.warning(f" [SKIP] Too Large ({os.path.getsize(file_path)//1024}KB): {filename}")
            return False
    except OSError:
        return False
    return True


def main():
    setup_logger()
    if not os.path.exists(SOURCE_DIR):
        logging.error(f"Source '{SOURCE_DIR}' does not exist. Run generate_research_copy.py first.")
        return

    if os.path.exists(DEST_DIR):
        shutil.rmtree(DEST_DIR)

    logging.info(f"[*] Starting extraction from '{SOURCE_DIR}' to '{DEST_DIR}'...")
    files_copied = 0
    total_size = 0

    for root, dirs, files in os.walk(SOURCE_DIR):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        rel_path = os.path.relpath(root, SOURCE_DIR)
        dest_path = os.path.join(DEST_DIR, rel_path) if rel_path != '.' else DEST_DIR
        os.makedirs(dest_path, exist_ok=True)
        for f in files:
            src_file = os.path.join(root, f)
            if is_safe_copy(f, src_file):
                shutil.copy2(src_file, os.path.join(dest_path, f))
                files_copied += 1
                total_size += os.path.getsize(src_file)

    logging.info("-" * 40)
    logging.info(f"[*] Copy Complete. Total Size: {total_size / 1024 / 1024:.2f} MB")
    logging.info("[*] Verifying Critical Components...")

    all_good = True
    for comp in CRITICAL_COMPONENTS:
        if os.path.exists(os.path.join(DEST_DIR, comp)):
            logging.info(f" [OK] Found: {comp}")
        else:
            logging.warning(f" [MISSING] Critical file not found: {comp}")
            all_good = False

    if all_good:
        logging.info("\n[SUCCESS] Research Artifact is Ready for Development.")
        logging.info(f"Location: {os.path.abspath(DEST_DIR)}")


if __name__ == "__main__":
    main()
