# LUCID EMPIRE :: FONT FINGERPRINTING CONFIGURATION
# Purpose: Manage font-based fingerprinting mitigation

import json
import os
from typing import Dict, List, Optional

class FontConfig:
    """Configure and manage font fingerprinting signatures"""
    
    def __init__(self):
        self.fonts = {}
        self.load_config()
    
    def load_config(self) -> None:
        """Load font configuration from assets"""
        config_path = os.path.join("assets", "fonts_config.json")
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                self.fonts = json.load(f)
    
    def get_common_fonts(self, os_type: str) -> List[str]:
        """Get list of common fonts for OS"""
        common_fonts = {
            'windows': [
                'Arial', 'Times New Roman', 'Courier New', 'Verdana',
                'Georgia', 'Trebuchet MS', 'Comic Sans MS'
            ],
            'macos': [
                'Helvetica', 'Times New Roman', 'Monaco', 'Menlo',
                'Courier New', 'Georgia'
            ],
            'linux': [
                'DejaVu Sans', 'DejaVu Serif', 'Courier',
                'Times', 'Liberation Sans', 'Liberation Serif'
            ]
        }
        return common_fonts.get(os_type.lower(), common_fonts['windows'])
    
    def get_font_metrics(self, font_name: str) -> Optional[Dict]:
        """Get font metrics if available"""
        return self.fonts.get(font_name, None)
    
    def inject_font_signature(self, profile: Dict, fonts: List[str]) -> None:
        """Inject font signature into profile"""
        profile['fonts'] = fonts
