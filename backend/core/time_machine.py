# LUCID EMPIRE :: TIME MACHINE
# Purpose: Advanced temporal manipulation and system time spoofing

import time
import logging
from datetime import datetime, timedelta
from typing import Optional

class TimeMachine:
    """Advanced temporal manipulation system"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.virtual_time = None
        self.time_scale = 1.0  # Normal speed by default
    
    def set_virtual_time(self, timestamp: float) -> None:
        """Set virtual system time"""
        self.virtual_time = timestamp
        self.logger.info(f"Virtual time set to {datetime.fromtimestamp(timestamp)}")
    
    def get_virtual_time(self) -> float:
        """Get current virtual time"""
        if self.virtual_time is None:
            return time.time()
        
        elapsed_real = time.time() - self._real_time_baseline
        elapsed_virtual = elapsed_real * self.time_scale
        return self.virtual_time + elapsed_virtual
    
    def set_time_scale(self, scale: float) -> None:
        """Set time acceleration/deceleration"""
        self._real_time_baseline = time.time()
        self.time_scale = scale
        self.logger.info(f"Time scale set to {scale}x")
    
    def advance_time(self, seconds: float) -> None:
        """Advance virtual time by seconds"""
        if self.virtual_time is not None:
            self.virtual_time += seconds
