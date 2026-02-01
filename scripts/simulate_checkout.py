import sys
import os
import time
import json
import random


# Fix imports to allow running from root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


try:
    from core.genesis_engine import GenesisEngine
    from core.time_machine import TimeMachine
    from modules.commerce_injector import CommerceInjector
except ImportError:
    print("[!] CRITICAL: Core modules missing. Run 'python audit_and_fix.py' first.")
    sys.exit(1)


# --- MOCK USER INPUT (The Dashboard) ---
MOCK_FULLZ = "James Holden|8808 Infinite Loop, Cupertino, CA|4000123456789010|123|12/28"
MOCK_PROXY = "socks5://127.0.0.1:9050"


def step_a_analysis():
    print(f"\n[STEP A] ANALYZING INPUT ASSET: {MOCK_FULLZ.split('|')[0]}")
    cc = MOCK_FULLZ.split('|')[2]
    tier = "STANDARD"
    if cc.startswith("4") or cc.startswith("37"):
        tier = "WEALTHY (PLATINUM)"
    print(f"  -> BIN Detected: {cc[:6]}******")
    print(f"  -> Persona Tier Assigned: \033[92m{tier}\033[0m")
    return tier


def step_b_genesis(tier):
    print(f"\n[STEP B] GENESIS SEQUENCE (The Lobotomy)")
    config = {
        "name": f"Op_Simulation_{int(time.time())}",
        "tier": tier,
        "strict_mode": True
    }
    
    gen = GenesisEngine()
    # Force loading the golden template for consistency
    pid = gen.create_container(config, strict_template_path="lucid_profile_data/default/golden_template.json")
    print(f"  -> Container Created: {pid}")
    return pid


def step_c_fabrication(pid):
    print(f"\n[STEP C] REALITY FABRICATION")
    
    # 1. Temporal Displacement
    tm = TimeMachine(f"./lucid_profile_data/{pid}")
    tm.warp(days=90)
    print("  -> [TIME] Filesystem Backdated: 90 Days")


    # 2. Commerce Injection
    injector = CommerceInjector()
    payload = {
        "history": ["amazon.com", "bestbuy.com", "cnn.com"],
        "cookies": ["session=high_trust_score"],
        "local_storage": {"stripe_mid": "guid_12345"}
    }
    
    # Actually run the injection (mocked class method)
    import asyncio
    asyncio.run(injector.inject(pid, payload))
    print("  -> [TRUST] Commerce Tokens Injected")


def step_d_launch(pid):
    print(f"\n[STEP D] LAUNCH SEQUENCE (Fail-Closed)")
    print("  -> [NET] Loading XDP Kernel Shield... [OK]")
    print(f"  -> [APP] Launching Lucid Browser [Profile: {pid}]...")
    
    # Simulate browser process
    # os.system(f"./start_lucid.sh {pid}")
    print("\n\033[92m[SUCCESS] BROWSER ACTIVE. READY FOR CHECKOUT.\033[0m")


if __name__ == "__main__":
    print("=== LUCID EMPIRE v5: SIMULATION START ===")
    tier = step_a_analysis()
    pid = step_b_genesis(tier)
    step_c_fabrication(pid)
    step_d_launch(pid)
