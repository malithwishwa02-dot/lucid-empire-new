# LUCID EMPIRE v5.0 DEPLOYMENT MANUAL (Release Candidate v1.4)

## System Architecture
- GUI (Host): `lucid_commander.py` (PyQt6 + qt-material) with live log console, platform-aware launch.
- Transmission: `start_lucid.bat` (Windows) / `start_lucid.sh` (Linux) for elevation + handoff.
- Engine: `lucid_launcher.py` with cross-platform guards, profile normalization, and takeover/genesis modes.

## Installation
1) Python deps:
```bash
pip install -r gui_requirements.txt
```
2) Place hardened Firefox binary:
- Linux: `./bin/firefox/firefox`
- Windows: `./bin/firefox/firefox.exe`
  - Or set `LUCID_FIREFOX_BIN` env var to an absolute path.

## Launch
```bash
python lucid_commander.py
```
- Windows: Commander will call `start_lucid.bat` and request UAC via PowerShell RunAs.
- Linux: Commander will call `start_lucid.sh` and request sudo for eBPF/Docker if present.

## Operational Modes
- Linux: HARD (eBPF) path available externally; launcher skips eBPF hooks on Windows.
- Windows: SOFT (native) path; container/eBPF steps skipped by design.

## Troubleshooting
- "Sovereign binary missing": Ensure the Firefox binary path exists or export `LUCID_FIREFOX_BIN`.
- "Elevation denied": Approve UAC (Windows) or provide sudo (Linux).
- Logs: The Commander log pane streams stdout/stderr from the launcher in real time.

## Notes
- Profile schema is normalized in the launcher (proxy/template/financial/mission.target_site/mission.aging_days) to match Commander output.
- Override binary path via `LUCID_FIREFOX_BIN` when packaging custom builds.
