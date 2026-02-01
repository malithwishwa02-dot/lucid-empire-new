import json
import os
import uuid
import time
import shutil
from typing import Dict, Optional, List

DB_FILE = "lucid_profiles.json"
TEMPLATES_DIR = os.path.join("assets", "templates", "golden")
PROFILE_DATA_DIR = "lucid_profile_data"

class IntegrityError(Exception):
    pass

class ProfileFactory:
    """
    Sovereign Factory Pattern for creating hardware-consistent profiles.
    """
    @staticmethod
    def create(seed: Dict) -> Dict:
        os_target = seed.get('os', 'Windows').lower()
        template_path = os.path.join(TEMPLATES_DIR, "golden_template.json")
        
        # Pattern 1: Deterministic Output via seed hashing
        import hashlib
        profile_seed_hash = hashlib.sha256(seed.get('name', 'default').encode()).hexdigest()
        
        if not os.path.exists(template_path):
            # Fallback if template missing
            template = {
                "navigator": {"userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:134.0) Gecko/20100101 Firefox/134.0"},
                "webgl": {"vendor": "Google Inc. (NVIDIA)", "renderer": "ANGLE (NVIDIA, NVIDIA GeForce RTX 3060, OpenGL 4.5)"}
            }
        else:
            with open(template_path, 'r') as f:
                template = json.load(f)

        profile_id = str(uuid.uuid4())
        name = seed.get('name', f"profile_{profile_id[:8]}")
        
        profile_path = os.path.join(PROFILE_DATA_DIR, name)
        os.makedirs(profile_path, exist_ok=True)

        # Pattern Requirement 5: Copy uBOAssets.json and default user.js
        assets_src = os.path.join("assets", "uBOAssets.json")
        if os.path.exists(assets_src):
            shutil.copy(assets_src, os.path.join(profile_path, "uBOAssets.json"))
        
        # Validation: Pattern Requirement 6
        ProfileFactory.validate_consistency(seed, template)

        profile = {
            "id": profile_id,
            "name": name,
            "path": profile_path,
            "created_at": time.time(),
            "last_launched": None,
            "genesis_complete": False,
            "seed_hash": profile_seed_hash,
            "hardware": {
                "ua": template["navigator"]["userAgent"],
                "webgl_vendor": template["webgl"]["vendor"],
                "webgl_renderer": template["webgl"]["renderer"]
            },
            **seed
        }
        return profile

    @staticmethod
    def validate_consistency(seed: Dict, template: Dict):
        ua = template["navigator"]["userAgent"]
        vendor = template["webgl"]["vendor"]
        
        is_windows_ua = "Windows" in ua
        is_apple_vendor = "Apple" in vendor
        
        if is_windows_ua and is_apple_vendor:
            raise IntegrityError("Hardware Clash: Windows User-Agent with Apple WebGL Vendor")
        
        if "iPhone" in ua and "NVIDIA" in vendor:
            raise IntegrityError("Hardware Clash: iPhone User-Agent with NVIDIA WebGL Vendor")

class ProfileStore:
    def __init__(self):
        self._load_db()

    def _load_db(self):
        if not os.path.exists(DB_FILE):
            self.profiles = []
            self._save_db()
        else:
            with open(DB_FILE, 'r') as f:
                try:
                    self.profiles = json.load(f)
                except json.JSONDecodeError:
                    self.profiles = []

    def _save_db(self):
        with open(DB_FILE, 'w') as f:
            json.dump(self.profiles, f, indent=4)

    def create_profile(self, data):
        new_profile = ProfileFactory.create(data)
        self.profiles.append(new_profile)
        self._save_db()
        return new_profile

    def get_all(self):
        return self.profiles

    def get_profile(self, profile_id):
        return next((p for p in self.profiles if p['id'] == profile_id), None)

    def update_status(self, profile_id, key, value):
        for p in self.profiles:
            if p['id'] == profile_id:
                p[key] = value
        self._save_db()
        
    def delete_profile(self, profile_id):
        self.profiles = [p for p in self.profiles if p['id'] != profile_id]
        self._save_db()
