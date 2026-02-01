# LUCID EMPIRE :: TIME DISPLACEMENT
# Temporal offset management for profile aging

import os
import datetime

class TimeDisplacement:
    """Manages temporal offsets for profile anti-detection."""
    
    def __init__(self, days_offset=0):
        self.days_offset = days_offset
    
    def get_displaced_time(self):
        """Get current time with displacement applied."""
        now = datetime.datetime.now()
        return now - datetime.timedelta(days=self.days_offset)
    
    def set_environment(self):
        """Set environment for libfaketime."""
        env = os.environ.copy()
        if self.days_offset > 0:
            env["FAKETIME"] = f"-{self.days_offset}d"
        return env
