# LUCID EMPIRE :: TEMPORAL DISPLACEMENT ENGINE
# Purpose: Manage temporal offset and timing masking

import time
import random
from typing import Optional

class TemporalDisplacement:
    """Manage system temporal offset for anti-forensics"""
    
    def __init__(self):
        self.offset = 0  # Seconds offset from real time
        self.jitter = (0, 60)  # Jitter range in seconds
        self.active = False
    
    def set_offset(self, seconds: int) -> None:
        """Set temporal offset in seconds"""
        self.offset = seconds
        self.active = True
    
    def get_displaced_time(self) -> float:
        """Get current time with displacement and jitter"""
        real_time = time.time()
        jitter = random.uniform(self.jitter[0], self.jitter[1])
        return real_time + self.offset + jitter
    
    def get_displaced_timestamp(self) -> str:
        """Get displaced timestamp as ISO string"""
        import datetime
        displaced = datetime.datetime.fromtimestamp(self.get_displaced_time())
        return displaced.isoformat()
    
    def reset(self) -> None:
        """Reset temporal displacement"""
        self.offset = 0
        self.active = False
    
    def get_status(self) -> dict:
        """Get current displacement status"""
        return {
            'offset_seconds': self.offset,
            'active': self.active,
            'displaced_time': self.get_displaced_timestamp()
        }
