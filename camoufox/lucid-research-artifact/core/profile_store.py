import json
import os
import uuid
import time

DB_FILE = "lucid_profiles.json"

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
        profile_id = str(uuid.uuid4())[:8]
        profile_path = os.path.join("lucid_profile_data", profile_id)
        os.makedirs(profile_path, exist_ok=True)

        new_profile = {
            "id": profile_id,
            "created_at": time.time(),
            "last_launched": None,
            "path": profile_path,
            "genesis_complete": False,
            **data 
        }
        
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
