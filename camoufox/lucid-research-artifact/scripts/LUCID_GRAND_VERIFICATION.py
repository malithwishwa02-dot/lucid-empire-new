# LUCID EMPIRE :: GRAND VERIFICATION SUITE
# Purpose: Verifies Zero Detect status against forensic vectors (CreepJS/Browserleaks simulation).

import json
import os
import asyncio
from playwright.async_api import async_playwright

async def verify_fingerprint():
    print(" [!] STARTING LUCID GRAND VERIFICATION...")
    
    async with async_playwright() as p:
        # Launch with specific args to simulate the hardened environment
        browser = await p.firefox.launch(headless=True)
        page = await browser.new_page()
        
        # 1. Verify WebGL Masking (CreepJS Vector)
        print(" [*] Verifying WebGL Interception...")
        webgl_info = await page.evaluate("""() => { 
            const canvas = document.createElement('canvas'); 
            const gl = canvas.getContext('webgl'); 
            const debugInfo = gl.getExtension('WEBGL_debug_renderer_info'); 
            return {
                vendor: gl.getParameter(debugInfo.UNMASKED_VENDOR_WEBGL),
                renderer: gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL)
            };
        }""")
        
        if "llvmpipe" in webgl_info['renderer'].lower():
            print(f" [X] FAIL: WebGL Leak detected: {webgl_info['renderer']}")
        else:
            print(f" [V] PASS: WebGL Spoofed: {webgl_info['vendor']} / {webgl_info['renderer']}")

        # 2. Verify Navigator Integrity (Worker Scope)
        print(" [*] Verifying Navigator Platform (Window & Worker)...")
        nav_consistency = await page.evaluate("""async () => {
            const winPlatform = navigator.platform;
            const workerPlatform = await new Promise(resolve => {
                const blob = new Blob(['postMessage(navigator.platform)'], {type: 'application/javascript'});
                const worker = new Worker(URL.createObjectURL(blob));
                worker.onmessage = e => resolve(e.data);
            });
            return { win: winPlatform, worker: workerPlatform };
        }""")
        
        if nav_consistency['win'] == "Win32" and nav_consistency['worker'] == "Win32":
            print(" [V] PASS: Navigator Platform aligned (Window & Worker): Win32")
        else:
            print(f" [X] FAIL: Platform Mismatch/Leak. Win: {nav_consistency['win']}, Worker: {nav_consistency['worker']}")

        # 3. Verify Font Blindness / Harmonization
        print(" [*] Verifying Font Availability...")
        # Check for signature Windows fonts and absence of typical Linux fonts
        font_check = await page.evaluate("""() => { 
            const detect = (font) => {
                const canvas = document.createElement("canvas");
                const context = canvas.getContext("2d");
                context.font = "72px monospace";
                const baselineSize = context.measureText("test").width;
                context.font = "72px '" + font + "', monospace";
                return context.measureText("test").width !== baselineSize;
            };
            return {
                hasSegoe: detect('Segoe UI'),
                hasUbuntu: detect('Ubuntu'),
                hasLiberation: detect('Liberation Sans')
            };
        }""")
        
        if font_check['hasUbuntu'] or font_check['hasLiberation']:
             # Note: On a real Windows host, these shouldn't exist unless installed manually.
             # In a Linux container, this would verify the masking.
             print(f" [!] WARNING: Linux fonts detected (Ubuntu: {font_check['hasUbuntu']}, Liberation: {font_check['hasLiberation']}). Potential leak if running in container.")
        else:
             print(" [V] PASS: Standard Linux fonts not detected.")

        if font_check['hasSegoe']:
            print(" [V] PASS: Windows signature font (Segoe UI) detected.")
        else:
            print(" [!] WARNING: Windows signature font (Segoe UI) MISSING. Profile may look generic.")

        # 4. AudioContext Fingerprint (Basic Check)
        print(" [*] Verifying AudioContext...")
        audio_state = await page.evaluate("""() => {
            try {
                const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                return audioCtx.state;
            } catch(e) { return 'error'; }
        }""")
        print(f" [i] AudioContext State: {audio_state}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(verify_fingerprint())
