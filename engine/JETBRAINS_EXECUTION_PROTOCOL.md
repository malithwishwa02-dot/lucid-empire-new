OP-LUCID-TITAN: DEVELOPMENT & BUILD PROTOCOL
Authority: Dva.12
Environment: JetBrains (PyCharm/WebStorm/IntelliJ)
Objective: Compile unified .DEB installer for Lucid Empire v5.

1. INFRASTRUCTURE SETUP (IDE)
* [ ] Python Interpreter: Set Project Interpreter to venv (Python 3.10+).
* [ ] Node.js: Ensure Node 20+ is active for frontend/.
* [ ] Dependencies:
  ```bash
  pip install fastapi uvicorn requests packaging
  cd frontend && npm install
  ```

2. BACKEND INTEGRATION (Python)
* [ ] API Gateway: Verify backend/lucid_api.py imports core.genesis_engine.
* [ ] Time Machine: Ensure backend/core/time_machine.py has sudo permissions (requires os.utime).
* [ ] Network Shield: Check if engine/network/xdp_outbound.o exists. If not, add a "Before Launch" task in IDE to run:
  ```bash
  clang -O2 -target bpf -c engine/network/xdp_outbound.c -o engine/network/xdp_outbound.o
  ```

3. FRONTEND INTEGRATION (Tauri/React)
* [ ] API Endpoint: Check frontend/src/App.tsx. Ensure API_URL points to http://127.0.0.1:13337.
* [ ] Build Test: Run `npm run tauri build` in the terminal.
* Success Criteria: Output file `src-tauri/target/release/bundle/deb/lucid-empire_5.0.0_amd64.deb` generated.

4. BROWSER ENGINE (Camoufox)
* [ ] Patch Verification: Ensure engine/patches/ contains `timezone-spoofing.patch` and `fingerprint-injection.patch`.
* [ ] Binary Linking: The build script must fetch the pre-compiled Camoufox binary if local compilation is skipped to save time.

5. PACKAGING (The .DEB Artifact)
* [ ] Control File: Verify `packaging/debian/control` matches version 5.0.0.
* [ ] Post-Install: Check `packaging/debian/postinst` for `chmod +x` on the launcher script.

6. ZERO DETECT VALIDATION
* [ ] Run Simulation: Execute `backend/scripts/simulate_checkout.py`.
* [ ] Check Logs: Look for `[TIME] Displacement Complete` and `[NET] Shield Active`.
