# LUCID COMMANDER v1.0 UI UPGRADE PLAN

## Objective
Replace the legacy CLI launcher with a PyQt6-based “Lucid Commander” dashboard that covers the Fabrication → Genesis → Takeover lifecycle, mirrors the backend profile store, and surfaces the Manual Takeover Protocol controls for immediate human intervention.

## Deliverables
1. `lucid_commander.py`: Industrial-dark PyQt6 dashboard with:
   - Sidebar navigation, profile table, toolbar actions.
   - Identity Wizard (Fullz, Financial, Network, Narrative vectors).
   - Action buttons for launching and deleting identities.
2. `gui_requirements.txt`: PyQt6 + qt-material dependency manifest.
3. Documentation of installation/run steps in this plan.

## Installation & Execution
1. Create a virtual environment (recommended).
2. Install dependencies:
   ```bash
   pip install -r gui_requirements.txt
   ```
3. Launch the dashboard:
   ```bash
   python lucid_commander.py
   ```
4. Use the + CREATE IDENTITY wizard to capture Fullz / CC / Proxy / Narrative data.
5. Click ▶ to initiate the Manual Takeover Protocol (handled by `lucid_launcher.py` in the backend).

## Notes for Integration
- The current `LucidManager` class wraps `core.profile_store.ProfileStore`; feel free to swap in the production manager from `lucid_launcher.py` when ready.
- `launch_profile` currently displays a confirmation dialog; replace it with the subprocess call (`python lucid_launcher.py --mode takeover --profile_id <uuid>`) once the backend and GUI share a runtime environment.
- This dashboard is stylized with `qt_material` when available; otherwise, it falls back to Fusion styling.
