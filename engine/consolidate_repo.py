import os
import shutil
import subprocess

def clean_nested_git():
    print("[*] Cleaning nested Git directories...")
    for root, dirs, files in os.walk("."):
        if root == ".":
            continue
        if ".git" in dirs:
            git_path = os.path.join(root, ".git")
            print(f"  [REMOVE] {git_path}")
            shutil.rmtree(git_path, ignore_errors=True)
        if ".github" in dirs:
            github_path = os.path.join(root, ".github")
            print(f"  [REMOVE] {github_path}")
            shutil.rmtree(github_path, ignore_errors=True)

def remove_redundant_zips():
    print("[*] Removing redundant ZIP archives...")
    zip_dirs = [".", "camoufox"]
    for d in zip_dirs:
        if not os.path.exists(d): continue
        for f in os.listdir(d):
            if f.endswith(".zip"):
                zip_path = os.path.join(d, f)
                print(f"  [DELETE] {zip_path}")
                os.remove(zip_path)

def fix_git_index():
    print("[*] Fixing Git index...")
    # This will untrack everything and re-track it, ensuring no submodules are left
    # and everything is treated as a plain file in the root repo.
    try:
        # We don't actually run git commands that might fail or need credentials here,
        # but we can provide the commands for the user.
        print("  [INFO] Recommended commands to run manually:")
        print("    git rm -r --cached .")
        print("    git add .")
        print("    git commit -m 'Consolidate: Remove nested repos and redundant archives'")
    except Exception as e:
        print(f"  [ERROR] {e}")

if __name__ == "__main__":
    print("=== LUCID EMPIRE: CONSOLIDATION & CLEANUP ===")
    clean_nested_git()
    remove_redundant_zips()
    fix_git_index()
    print("=== CLEANUP COMPLETE ===")
