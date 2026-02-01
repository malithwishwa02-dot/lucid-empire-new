import sys
import os

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), 'camoufox', 'pythonlib'))

print("Testing core.genesis_engine...")
try:
    from core.genesis_engine import GenesisEngine
    print("SUCCESS: core.genesis_engine")
except Exception as e:
    print(f"FAILED: core.genesis_engine -> {e}")
    import traceback
    traceback.print_exc()

print("\nTesting core.time_machine...")
try:
    from core.time_machine import TimeMachine
    print("SUCCESS: core.time_machine")
except Exception as e:
    print(f"FAILED: core.time_machine -> {e}")

print("\nTesting modules.commerce_injector...")
try:
    from modules.commerce_injector import CommerceInjector
    print("SUCCESS: modules.commerce_injector")
except Exception as e:
    print(f"FAILED: modules.commerce_injector -> {e}")
