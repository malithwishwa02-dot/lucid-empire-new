import os
import zipfile
import shutil
import subprocess
import argparse
from pathlib import Path
import tempfile


def generate_tree(startpath):
    tree_str = ""
    for root, dirs, files in os.walk(startpath):
        # Skip git and hidden directories for cleaner tree
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        tree_str += '{}{}/\n'.format(indent, os.path.basename(root))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            if not f.startswith('.'):
                tree_str += '{}{}\n'.format(subindent, f)
    return tree_str

def create_zip(zip_name, files_to_zip):
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in files_to_zip:
            if os.path.exists(file_path):
                zipf.write(file_path, arcname=file_path)
                print(f"Added: {file_path}")
            else:
                print(f"Warning: File not found: {file_path}")


def create_debian_package(build_dir='build/debian', version='2.0.0'):
    """Create a Debian package in-place under the repo for local testing.
    - Copies minimal required files into build_dir/opt/lucid-empire
    - Creates control file, maintainer scripts, desktop file, system launcher
    - Installs python requirements into pylibs if present
    - Creates a dummy firefox binary if a compiled build is unavailable
    - Runs dpkg-deb --build to create lucid-empire_{version}_amd64.deb
    """
    # Ensure version begins with a digit (dpkg requirement). If not, prefix with 0+
    if not str(version) or not str(version)[0].isdigit():
        version = f"0+{str(version)}"
    # sanitize characters not allowed in version
    version = str(version).replace('/', '-').replace(' ', '_')
    build_path = Path(build_dir)
    deb_opt = build_path / 'opt' / 'lucid-empire'
    deb_usr_bin = build_path / 'usr' / 'bin'
    deb_share_app = build_path / 'usr' / 'share' / 'applications'
    deb_icons = build_path / 'usr' / 'share' / 'icons' / 'hicolor' / '128x128' / 'apps'
    deb_debian = build_path / 'DEBIAN'

    # Clean and recreate
    if build_path.exists():
        shutil.rmtree(build_path)
    deb_debian.mkdir(parents=True, exist_ok=True)
    deb_debian.chmod(0o755)
    deb_opt.mkdir(parents=True, exist_ok=True)
    deb_usr_bin.mkdir(parents=True, exist_ok=True)
    deb_share_app.mkdir(parents=True, exist_ok=True)
    deb_icons.mkdir(parents=True, exist_ok=True)

    # Copy code
    src_base = Path('camoufox/lucid-empire-research-v2')
    for p in ['lucid_launcher.py', 'lucid_manager.py']:
        src = src_base / p
        if src.exists():
            shutil.copy(src, deb_opt)
    for folder in ['core', 'modules', 'jsonvv']:
        src = src_base / folder
        if src.exists():
            dst = deb_opt / folder
            shutil.copytree(src, dst)

    # Copy or create browser binary
    browser_src = src_base / 'dist' / 'firefox'
    browser_dst = deb_opt / 'browser'
    if browser_src.exists():
        shutil.copytree(browser_src, browser_dst)
    else:
        # Create dummy browser binary to let dpkg succeed during local testing
        browser_dst.mkdir(parents=True, exist_ok=True)
        dummy = browser_dst / 'firefox'
        with open(dummy, 'w') as f:
            f.write('#!/bin/sh\necho "Lucid Dummy Firefox"\nexit 0\n')
        dummy.chmod(0o755)

    # Install Python deps if requirements exist
    req = Path('camoufox/gui_requirements.txt')
    pylibs = deb_opt / 'pylibs'
    if req.exists():
        pylibs.mkdir(parents=True, exist_ok=True)
        subprocess.run(['pip3', 'install', '-r', str(req), '--target', str(pylibs)], check=False)

    # Create system launcher
    launcher = deb_usr_bin / 'lucid-browser'
    with open(launcher, 'w') as f:
        f.write('#!/bin/bash\n')
        f.write('export PYTHONPATH="/opt/lucid-empire/pylibs:${PYTHONPATH:-}"\n')
        f.write('cd /opt/lucid-empire\n')
        f.write('python3 lucid_launcher.py "$@"\n')
    launcher.chmod(0o755)

    # Desktop entry
    desktop = deb_share_app / 'lucid-empire.desktop'
    with open(desktop, 'w') as f:
        f.write('[Desktop Entry]\n')
        f.write('Name=Lucid Empire\n')
        f.write('Comment=Anti-Detect Research Browser\n')
        f.write('Exec=/usr/bin/lucid-browser\n')
        f.write('Icon=/usr/share/icons/hicolor/128x128/apps/lucid-empire.png\n')
        f.write('Type=Application\n')
        f.write('Categories=Network;WebBrowser;\n')

    # Copy icon if exists
    src_icon = src_base / 'dist' / 'firefox' / 'browser' / 'chrome' / 'icons' / 'default' / 'default128.png'
    if src_icon.exists():
        shutil.copy(src_icon, deb_icons / 'lucid-empire.png')

    # Control file
    control = deb_debian / 'control'
    with open(control, 'w') as f:
        f.write('Package: lucid-empire\n')
        f.write(f'Version: {version}\n')
        f.write('Section: web\n')
        f.write('Priority: optional\n')
        f.write('Architecture: amd64\n')
        f.write('Depends: python3, libgtk-3-0, libdbus-glib-1-2\n')
        f.write('Maintainer: Dva.12 <admin@lucidempire.ai>\n')
        f.write('Description: Lucid Empire Anti-Detect Browser\n')
        f.write(' PROMETHEUS-CORE INTEGRATED.\n')
        f.write(' Features biometric mimicry, commerce injection, and zero-refusal navigation.\n')

    # Maintainer scripts
    postinst = deb_debian / 'postinst'
    with open(postinst, 'w') as f:
        f.write('#!/bin/sh\nset -e\nchown -R root:root /opt/lucid-empire\nchmod -R 755 /opt/lucid-empire\nupdate-desktop-database || true\ngtk-update-icon-cache -f /usr/share/icons/hicolor 2>/dev/null || true\nexit 0\n')
    postinst.chmod(0o755)

    prerm = deb_debian / 'prerm'
    with open(prerm, 'w') as f:
        f.write('#!/bin/sh\nset -e\nupdate-desktop-database || true\ngtk-update-icon-cache -f /usr/share/icons/hicolor 2>/dev/null || true\nexit 0\n')
    prerm.chmod(0o755)

    # Build the .deb
    output_name = f'lucid-empire_{version}_amd64.deb'
    subprocess.run(['dpkg-deb', '--build', str(build_path), output_name], check=True)
    print(f"Created package: {output_name}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Lucid packaging helper')
    parser.add_argument('--create-deb', action='store_true', help='Create a local .deb for testing')
    parser.add_argument('--deb-version', default='2.0.0', help='Debian package version')
    args = parser.parse_args()

    base_dir = os.getcwd()
    # 1. Generate Tree
    print("Generating repository tree...")
    tree_content = generate_tree(base_dir)
    with open("LUCID_REPO_TREE.txt", "w", encoding="utf-8") as f:
        f.write(tree_content)

    # Preserve existing archive creation functionality
    print("Creating archive...")
    modified_files = [
        "pythonlib/lucid_browser/sync_api.py",
        "pythonlib/lucid_browser/async_api.py",
        "pythonlib/lucid_browser/utils.py",
        "pythonlib/lucid_browser/fingerprints.py",
        "pythonlib/lucid_browser/__main__.py",
        "pythonlib/lucid_browser/server.py",
        "pythonlib/lucid_browser/exceptions.py",
        "pythonlib/lucid_browser/warnings.yml",
        "pythonlib/pyproject.toml",
        "pythonlib/README.md",
        "core/genesis_engine.py",
        "core/profile_store.py",
        "core/__init__.py",
        "modules/commerce_injector.py",
        "modules/humanization.py",
        "modules/biometric_mimicry.py",
        "modules/__init__.py",
        "patches/webgl-spoofing.patch",
        "patches/lucid-navigator.patch",
        "patches/font-hijacker.patch",
        "additions/camoucfg/MaskConfig.hpp",
        "additions/camoucfg/MouseTrajectories.hpp",
        "network/xdp_outbound.c",
        ".github/workflows/lucid-build.yml",
        "docker-compose.yml",
        "Dockerfile",
        "lucid_launcher.py",
        "lucid_manager.py",
        "start_lucid.sh",
        "scripts/package_ghost.py",
        "scripts/setup_fonts.sh",
        "scripts/LUCID_GRAND_VERIFICATION.py",
        "lucid_profile_data/default/golden_template.json",
        "README_LUCID.md",
        "LUCID_TRANSFORMATION_REPORT.md",
        "LUCID_MODIFIED_FILES.txt",
        "LUCID_REPO_TREE.txt"
    ]
    create_zip("lucid_empire_modifications.zip", modified_files)
    print("Archive created: lucid_empire_modifications.zip")

    if args.create_deb:
        print("Creating local .deb for testing...")
        create_debian_package(version=args.deb_version)
        print("Local .deb created")

