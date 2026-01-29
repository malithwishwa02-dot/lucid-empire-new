import os
import zipfile

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

if __name__ == "__main__":
    base_dir = os.getcwd()
    
    # 1. Generate Tree
    print("Generating repository tree...")
    tree_content = generate_tree(base_dir)
    with open("LUCID_REPO_TREE.txt", "w", encoding="utf-8") as f:
        f.write(tree_content)
    
    # 2. Define Modified Files
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
    
    # 3. Create Zip
    print("Creating archive...")
    create_zip("lucid_empire_modifications.zip", modified_files)
    print("Archive created: lucid_empire_modifications.zip")
