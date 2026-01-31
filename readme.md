"""
LUCID EMPIRE API BRIDGE (v5.0.0)
--------------------------------
AUTHORITY: Dva.12
PURPOSE: Exposes Lucid Core logic to the Tauri GUI via localhost REST API.
LOCATION: Place this file in the root directory.

DEPENDENCIES:
  pip install fastapi uvicorn pydantic python-multipart
"""

import os
import sys
import time
import json
import asyncio
import threading
from typing import List, Optional
from pathlib import Path
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# --- IMPORT EXISTING LUCID CORE ---
# We wrap imports in try/except to prevent crashing if run outside the full env
try:
    # Adjust paths based on the new unified structure
    sys.path.append(os.path.dirname(__file__))
    # Assuming the purge left 'core' in the root
    from core.genesis_engine import GenesisEngine 
    # from core.profile_store import ProfileStore # Uncomment if store is verified
except ImportError:
    print("[!] WARNING: Lucid Core not found. Running in MOCK MODE.")
    class ProfileStore:
        def list_profiles(self): return []
    class GenesisEngine:
        pass

# Mock Manager for now as the original was purged or is legacy
class LucidManager:
    def create_profile(self, name, config): return f"profile_{int(time.time())}"
    def launch_profile(self, pid): return True

app = FastAPI(title="Lucid Empire API")

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
# store = ProfileStore() # Uncomment when store is verified

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
        # Heuristic: Gold/Platinum BINs (Simplified for demo)
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
    
    # 1. Temporal Displacement (File Aging)
    target_dir = Path(f"./lucid_profile_data/{profile_id}")
    if target_dir.exists():
        past_time = time.time() - (90 * 86400) # 90 days ago
        for root, dirs, files in os.walk(target_dir):
            for f in files:
                try:
                    os.utime(os.path.join(root, f), (past_time, past_time))
                except: pass
    
    # 2. Commerce Injection (Mock Delay)
    time.sleep(2) 
    
    print(f"[OBLIVION] Trust Generation Complete for {profile_id}")

# --- API ENDPOINTS ---

@app.get("/status")
def health_check():
    return {"system": "LUCID_TITAN", "status": "ONLINE", "mode": "UNRESTRICTED"}

@app.get("/profiles", response_model=List[ProfileStatus])
def get_profiles():
    """Lists all profiles with their calculated trust scores."""
    # In a real scenario, map this from store.list_profiles()
    # MOCK DATA for GUI dev
    return [
        {"id": "p1", "name": "Op_Blackbriar", "tier": "Wealthy", "trust_score": 98, "status": "READY", "proxy": "192.168.1.1"},
        {"id": "p2", "name": "Op_Treadstone", "tier": "Standard", "trust_score": 12, "status": "AGING", "proxy": "10.0.0.5"},
    ]

@app.post("/genesis")
async def create_identity(asset: RawAsset, background_tasks: BackgroundTasks):
    """
    Triggers the creation of a 'Digital Ghost'.
    1. Parses Identity
    2. Selects Golden Template
    3. Initiates Time Travel & Injection
    """
    data = parse_fullz(asset.raw_paste)
    
    # Config for Lucid Manager
    profile_config = {
        "name": f"{data['name']}_{int(time.time())}",
        "tier": data['tier'],
        "proxy": asset.proxy_url,
        "notes": "Generated via Lucid Commander"
    }
    
    # Create Profile
    pid = manager.create_profile(profile_config['name'], profile_config)
    
    # Schedule 'The Warm-Up' in background
    background_tasks.add_task(_background_trust_generation, pid)
    
    return {"id": pid, "tier_assigned": data['tier'], "message": "Genesis sequence initiated."}

@app.post("/launch/{profile_id}")
def launch(profile_id: str):
    """Executes the browser with XDP masking active."""
    success = manager.launch_profile(profile_id)
    if not success:
        raise HTTPException(status_code=500, detail="Launch Sequence Failed")
    return {"status": "LAUNCHED"}

if __name__ == "__main__":
    import uvicorn
    # Run on localhost:13337 to avoid conflicts
    uvicorn.run(app, host="127.0.0.1", port=13337)

def initialize_time_warp(days_ago):
    """
    Set up the faketime environment. This function should be called once
    before any subprocesses are started that need to be time-warped.

    Args:
        days_ago (int): Number of days in the past to simulate.
    """
    os.environ["LD_PRELOAD"] = "/usr/local/lib/faketime/libfaketime.so.1"
    os.environ["FAKETIME"] = f"-{days_ago}d"
    os.environ["DONT_FAKE_MONOTONIC"] = "1"
    os.environ["FAKETIME_NO_CACHE"] = "1"

class PhaseExecutor:
    def __init__(self, persona, config, logger):
        self.persona = persona
        self.config = config
        self.logger = logger
        self.city = LocationInfo(
            config["city_name"],
            config["country_name"],
            config["latitude"],
            config["longitude"],
            )
        self.timezone = pytz.timezone(config["timezone"])
        self.persona_schedule = config["persona_schedule"]
        self.urls = config["urls"]
        self.form_history_data = config["form_history_data"]

    def get_local_solar_time(self, days_ago):
        """
        Calculates local time based on solar positioning, adjusted for a certain number of days ago.
        """
        today = datetime.today() - timedelta(days=days_ago)
        
        # Calculate the sunrise and sunset for the given day, accounting for timezone
        s = sun(self.city.observer, date=today)
        
        # Convert sunrise and sunset to the configured timezone
        sunrise_local = s["sunrise"].astimezone(self.timezone)
        sunset_local = s["sunset"].astimezone(self.timezone)

        # Get the current local time
        now_local = datetime.now(self.timezone)
        
        self.logger.debug(f" > Time Warp: Sunrise: {sunrise_local.strftime('%H:%M')}, Sunset: {sunset_local.strftime('%H:%M')}, Current: {now_local.strftime('%H:%M')}")
        
        return now_local
    
    def is_persona_active(self, target_time):
        """
        Check if the persona should be active based on the current time.
        """
        current_time = target_time.strftime("%H:%M")
        if self.persona_schedule["start"] <= current_time <= self.persona_schedule["end"]:
            return True
        return False
    
    def get_persona_urls(self, phase_name):
        """
        Get URLs specific to the persona and phase.
        """
        return self.urls.get(self.persona, {}).get(phase_name, [])
    
    async def populate_form_history(self, page):
        """
        Populates form history based on the config.
        """
        data = self.form_history_data.get(self.persona, {})
        if not data:
            self.logger.info(" No form history data for persona.")
            return
        
        for selector, value in data.items():
            try:
                await page.fill(selector, value)
                self.logger.info(f" Filled {selector} with {value[:5]}...")
            except Exception as e:
                self.logger.warning(f" Could not fill {selector}: {e}")

    async def trigger_ga_mp(self, page):
        """
        Triggers a Google Analytics Measurement Protocol event.
        """
        # Placeholder for GA MP trigger logic
        self.logger.info(" Triggering Google Analytics Measurement Protocol (GA MP)...")
        await asyncio.sleep(random.randint(1, 3)) # Simulate network latency
        self.logger.info(" GA MP event triggered.")
    
    def set_time_warp(self, days_ago):
        """
        Configures libfaketime environment variables for the subprocess.
        """
        env = os.environ.copy()
        # Path to the library in the Linux container environment
        env["LD_PRELOAD"] = "/usr/local/lib/faketime/libfaketime.so.1"
        env["FAKETIME"] = f"-{days_ago}d"
        # Critical stability flags to prevent Firefox hangs (Plan 3.2.1)
        env["DONT_FAKE_MONOTONIC"] = "1"
        env["FAKETIME_NO_CACHE"] = "1"
        return env

    async def run_phase(self, phase_name, days_ago):
        target_time = self.get_local_solar_time(days_ago)
        
        if not self.is_persona_active(target_time):
            self.logger.info(f" Persona {self.persona} is SLEEPING at local time {target_time}. Skipping phase.")
            return

        self.logger.info(f" [>] TIME WARP: T-{days_ago} DAYS | PHASE: {phase_name} | PERSONA: {self.persona}")
        
        initialize_time_warp(days_ago)
        
        env = self.set_time_warp(days_ago)
        
        # [LUCID] VASCULAR CONNECTION: Using Sovereign Wrapper
        # We assume a default template for headless ops, or one passed via config
        template_path = "assets/templates/golden_iphone13.json" 
        
        async with AsyncLucidEmpire(
            fingerprint=template_path,
            user_data_dir=PROFILE_DIR,
            env=env,
            headless=True,
            viewport={"width": 1920, "height": 1080}
        ) as context:
            
            # Since AsyncLucidEmpire returns a context, we get the page from it
            if not context.pages:
                page = await context.new_page()
            else:
                page = context.pages[0]
                
            mimicry = BiometricMimicry(page)
            
            # Phase 1 specific: GA MP
            if phase_name == "INCEPTION":
                await self.trigger_ga_mp(page)

            urls = self.get_persona_urls(phase_name)
            for url in urls:
                try:
                    self.logger.info(f" Visiting {url}...")
                    await page.goto(url, wait_until="domcontentloaded")
                    await mimicry.human_scroll()
                    
                    # [LUCID] VASCULAR INTERVENTION POINT
                    current_url = page.url
                    if "amazon" in current_url or "apple" in current_url:
                        self.logger.info(f"[*] DETECTED COMMERCE NODE: {current_url}")
                        
                        # 1. Populate Form History (If applicable)
                        if phase_name == "WARMING":
                             await self.populate_form_history(page)
                             await mimicry.human_move(random.randint(100, 500), random.randint(100, 500))

                        # 2. IN
