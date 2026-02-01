# LUCID EMPIRE :: BACKEND API
# Purpose: Main API interface for backend operations

import logging
from typing import Dict, Optional
from backend.core import ProfileFactory, ProfileStore, CoreOrchestrator
from backend.modules import CommerceInjector, BiometricMimicry, HumanizationEngine

class LucidAPI:
    """Main API for Lucid Empire backend"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.profile_store = ProfileStore()
        self.orchestrator = CoreOrchestrator()
        self.setup_modules()
    
    def setup_modules(self) -> None:
        """Register operational modules"""
        self.orchestrator.register_module('commerce', CommerceInjector())
        self.orchestrator.register_module('biometric', BiometricMimicry())
        self.orchestrator.register_module('humanizer', HumanizationEngine())
    
    def create_profile(self, seed: Dict) -> Dict:
        """Create new profile"""
        return self.profile_store.create_profile(seed)
    
    def get_profile(self, profile_id: str) -> Optional[Dict]:
        """Retrieve profile"""
        return self.profile_store.get_profile(profile_id)
    
    def list_profiles(self) -> list:
        """List all profiles"""
        return self.profile_store.get_all()
    
    def delete_profile(self, profile_id: str) -> None:
        """Delete profile"""
        self.profile_store.delete_profile(profile_id)
