import sys
import os
import time
import json
import random
from typing import Any


# Fix imports to allow running from root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Mock orjson before importing core modules
import json
from unittest.mock import MagicMock
mock_orjson = MagicMock()
mock_orjson.loads = json.loads
mock_orjson.dumps = lambda x, **kwargs: json.dumps(x).encode()
mock_orjson.JSONEncodeError = json.JSONDecodeError # Close enough
sys.modules["orjson"] = mock_orjson

# Mock browserforge
mock_browserforge = MagicMock()
sys.modules["browserforge"] = mock_browserforge

# Create real classes for mocks to satisfy dataclass inheritance
from dataclasses import dataclass, field
@dataclass
class MockFingerprint:
    screen: Any = field(default_factory=lambda: MockScreenFingerprint())
    headers: dict = field(default_factory=dict)
@dataclass
class MockScreenFingerprint:
    screenX: int = 0
    availHeight: int = 1080
    outerHeight: int = 1000
    width: int = 1920
    height: int = 1080
    innerWidth: int = 1920
    innerHeight: int = 1000
    outerWidth: int = 1920
class MockFingerprintGenerator: 
    def __init__(self, *args, **kwargs): pass
    def generate(self, **kwargs): return MockFingerprint()

mock_bf_fp = MagicMock()
mock_bf_fp.Fingerprint = MockFingerprint
mock_bf_fp.FingerprintGenerator = MockFingerprintGenerator
mock_bf_fp.ScreenFingerprint = MockScreenFingerprint
sys.modules["browserforge.fingerprints"] = mock_bf_fp
sys.modules["browserforge.download"] = MagicMock()

# Mock other common missing modules
sys.modules["ua_parser"] = MagicMock()
sys.modules["onnxruntime"] = MagicMock()

try:
    from core.genesis_engine import GenesisEngine
    from core.time_machine import TimeMachine
    from modules.commerce_injector import CommerceInjector
    from modules.humanization import curve_mouse
except ImportError as e:
    print(f"[!] CRITICAL: Core modules missing: {e}")
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
    
    # 3. Behavioral Injection (Ghost Driver)
    print("  -> [BEHAVE] Injecting humanization.curve_mouse() into driver stream...")
    # In a real run, this would be: await curve_mouse(page)
    
    # Simulate browser process
    # os.system(f"./start_lucid.sh {pid}")
    print("\n\033[92m[SUCCESS] BROWSER ACTIVE. READY FOR CHECKOUT.\033[0m")


if __name__ == "__main__":
    print("=== LUCID EMPIRE v5: SIMULATION START ===")
    tier = step_a_analysis()
    pid = step_b_genesis(tier)
    step_c_fabrication(pid)
    step_d_launch(pid)
