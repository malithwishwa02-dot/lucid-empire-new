import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VENV = ROOT / "venv"
REQ = ROOT / "requirements.txt"
GUI_REQ = ROOT / "gui_requirements.txt"


def run(cmd):
    print(f"[+] {' '.join(map(str, cmd))}")
    subprocess.check_call(cmd)


def ensure_venv():
    if not VENV.exists():
        print("[*] Creating venv...")
        run([sys.executable, "-m", "venv", str(VENV)])


def pip_path():
    if sys.platform == "win32":
        return VENV / "Scripts" / "pip.exe"
    return VENV / "bin" / "pip"


def install_reqs():
    pip = str(pip_path())
    run([pip, "install", "--upgrade", "pip"])
    if REQ.exists():
        run([pip, "install", "-r", str(REQ)])
    if GUI_REQ.exists():
        run([pip, "install", "-r", str(GUI_REQ)])


def main():
    ensure_venv()
    install_reqs()
    print("[OK] Environment ready. Activate with: source venv/bin/activate (Linux) or venv\\Scripts\\activate (Windows)")


if __name__ == "__main__":
    main()
