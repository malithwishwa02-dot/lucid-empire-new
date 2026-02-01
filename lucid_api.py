import os
import sys
import time
import json
import asyncio
import threading
import subprocess
from pathlib import Path
from typing import List, Optional
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# --- IMPORT EXISTING LUCID CORE ---
sys.path.append(os.path.dirname(__file__))
try:
    from core.genesis_engine import GenesisEngine 
    from core.profile_store import ProfileStore 
except ImportError:
    # Fallback for environments where core is missing
    print("[!] WARNING: Lucid Core not found. API functionality will be limited.")
    class ProfileStore:
        def get_all(self): return []
        def get_profile(self, pid): return None
        def create_profile(self, data): return {"id": "mock_id"}
        def update_status(self, pid, k, v): pass
    class GenesisEngine:
        pass

class LucidManager:
    def __init__(self):
        self.store = ProfileStore()

    def create_profile(self, name, config):
        data = {
            "name": name,
            "proxy": config.get("proxy"),
            "template": "golden_template.json",
            "tier": config.get("tier", "Standard"),
            "fullz": {},
            "mission": {"target_site": "google.com", "aging_days": 90},
            "strict_mode": True
        }
        profile = self.store.create_profile(data)
        return profile['id']

    def launch_profile(self, pid):
        try:
            # Execute the takeover via the dashboard orchestrator
            subprocess.Popen([sys.executable, "dashboard/main.py", "--mode", "takeover", "--profile_id", pid])
            return True
        except Exception as e:
            print(f"Launch error: {e}")
            return False

    def list_profiles(self):
        return self.store.get_all()

app = FastAPI(title="Lucid Empire API (PRODUCTION)")

# Allow CORS for the Tauri Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Core Systems
manager = LucidManager()

# --- DATA MODELS ---

class RawAsset(BaseModel):
    """Expectation S: [STEP A] Input Vector"""
    raw_paste: str  # Name|Address|CC|CVV|Exp
    proxy_url: str  # socks5://...

class ProfileStatus(BaseModel):
    id: str
    name: str
    tier: str
    trust_score: int
    status: str
    proxy: str

# --- CORE LOGIC ---

def parse_fullz(raw: str) -> dict:
    """Parses 'Name|Address|CC|CVV|Exp' into structured data."""
    try:
        parts = raw.split('|')
        if len(parts) < 3: return {"name": "Unknown", "tier": "Standard"}
        
        name = parts[0]
        cc_num = parts[2]
        
        # [STEP A] Tier Detection Logic
        tier = "Standard"
        if cc_num.startswith("37") or cc_num.startswith("4"): # Amex/Visa Infinite
            tier = "Wealthy"
            
        return {"name": name, "cc": cc_num, "tier": tier}
    except:
        return {"name": "Unknown", "tier": "Standard"}

def _background_trust_generation(profile_id: str):
    """
    Expectation S: [STEP C] The Warm-Up
    Simulates 90 days of history and commerce injection.
    """
    print(f"[OBLIVION] Starting Trust Generation for {profile_id}...")
    
    store = ProfileStore()
    profile = store.get_profile(profile_id)
    if not profile:
        print(f"[!] Profile {profile_id} not found.")
        return

    # 1. Temporal Displacement (File Aging)
    # Using the 'Time Machine' logic mentioned in the audit
    target_dir = Path(profile['path'])
    if target_dir.exists():
        past_time = time.time() - (90 * 86400) # 90 days ago
        for root, dirs, files in os.walk(target_dir):
            for f in files:
                try:
                    os.utime(os.path.join(root, f), (past_time, past_time))
                except: pass
    
    # 2. Genesis Engine Execution
    try:
        # We call the genesis sequence via dashboard/main.py
        subprocess.run([sys.executable, "dashboard/main.py", "--mode", "genesis", "--profile_id", profile_id], check=True)
    except Exception as e:
        print(f"Genesis sequence failed for {profile_id}: {e}")

    print(f"[OBLIVION] Trust Generation Complete for {profile_id}")
    store.update_status(profile_id, "genesis_complete", True)

# --- API ENDPOINTS ---

@app.get("/status")
def health_check():
    return {"system": "LUCID_TITAN", "status": "ONLINE", "mode": "UNRESTRICTED"}

@app.get("/profiles", response_model=List[ProfileStatus])
def get_profiles():
    """Lists all profiles with their calculated trust scores."""
    profiles = manager.list_profiles()
    results = []
    for p in profiles:
        results.append({
            "id": p['id'],
            "name": p['name'],
            "tier": p.get('tier', 'Standard'),
            "trust_score": 98 if p.get('genesis_complete') else 15,
            "status": "READY" if p.get('genesis_complete') else "AGING",
            "proxy": p.get('proxy', 'NONE')
        })
    return results

@app.post("/genesis")
async def create_identity(asset: RawAsset, background_tasks: BackgroundTasks):
    """
    Triggers the creation of a 'Digital Ghost'.
    1. Parses Identity
    2. Selects Golden Template
    3. Initiates Time Travel & Injection
    """
    data = parse_fullz(asset.raw_paste)
    
    profile_config = {
        "name": f"{data['name']}_{int(time.time())}",
        "tier": data['tier'],
        "proxy": asset.proxy_url,
    }
    
    # Create Profile
    pid = manager.create_profile(profile_config['name'], profile_config)
    
    # Schedule 'The Warm-Up' in background
    background_tasks.add_task(_background_trust_generation, pid)
    
    return {"id": pid, "tier_assigned": data['tier'], "message": "Genesis sequence initiated."}

@app.post("/launch/{profile_id}")
def launch(profile_id: str):
    """Executes the browser with XDP masking active."""
    # Attempt to load XDP mask if on Linux
    if sys.platform.startswith("linux"):
        try:
            subprocess.run(["bash", "network/xdp_loader.sh", "load"], check=False)
        except: pass

    success = manager.launch_profile(profile_id)
    if not success:
        raise HTTPException(status_code=500, detail="Launch Sequence Failed")
    return {"status": "LAUNCHED"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=13337)
