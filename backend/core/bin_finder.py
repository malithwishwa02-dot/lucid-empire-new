# LUCID EMPIRE :: BINARY FINDER
# Purpose: Locate and verify browser executables

import os
import subprocess
import logging
from typing import Optional, List

class BinaryFinder:
    """Locate and manage browser executable binaries"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.firefox_paths = [
            "/usr/bin/firefox",
            "/usr/local/bin/firefox",
            "C:\\Program Files\\Firefox\\firefox.exe",
            "C:\\Program Files (x86)\\Firefox\\firefox.exe"
        ]
    
    def find_firefox(self) -> Optional[str]:
        """Find Firefox executable"""
        for path in self.firefox_paths:
            if os.path.exists(path):
                self.logger.info(f"Found Firefox: {path}")
                return path
        
        # Try 'which' command on Unix
        try:
            result = subprocess.run(['which', 'firefox'], capture_output=True, text=True)
            if result.returncode == 0:
                path = result.stdout.strip()
                self.logger.info(f"Found Firefox via which: {path}")
                return path
        except:
            pass
        
        self.logger.warning("Firefox not found")
        return None
    
    def verify_binary(self, path: str) -> bool:
        """Verify binary exists and is executable"""
        return os.path.isfile(path) and os.access(path, os.X_OK)
    
    def get_version(self, binary_path: str) -> Optional[str]:
        """Get browser version"""
        try:
            result = subprocess.run(
                [binary_path, '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.stdout.strip()
        except Exception as e:
            self.logger.error(f"Failed to get version: {e}")
            return None
