import os
import time
import random
from pathlib import Path

class TimeMachine:
    def __init__(self, profile_root: str):
        self.profile_root = Path(profile_root)

    def warp(self, days: int = 90, variance: int = 5):
        """
        Displaces the profile's filesystem timeline into the past.
        :param days: How many days back to shift creation time.
        :param variance: Random +/- days to add for realism.
        """
        if not self.profile_root.exists():
            print(f"[TIME] Error: Profile {self.profile_root} does not exist.")
            return

        # Calculate target timestamp
        target_shift = days + random.randint(-variance, variance)
        target_time = time.time() - (target_shift * 86400)
        
        print(f"[TIME] Warping filesystem back {target_shift} days...")

        count = 0
        for root, dirs, files in os.walk(self.profile_root):
            for name in files + dirs:
                full_path = os.path.join(root, name)
                
                # Add micro-jitter so files don't all have exact same millisecond
                jitter = random.randint(0, 3600) 
                file_time = target_time + jitter
                
                try:
                    # Modify Access and Modify times
                    os.utime(full_path, (file_time, file_time))
                    count += 1
                except Exception as e:
                    pass

        print(f"[TIME] Displacement Complete. {count} artifacts aged.")
        self._touch_critical_dbs(target_time)

    def _touch_critical_dbs(self, timestamp):
        """Specifically targets browser databases checked by fraud scripts."""
        critical_files = [
            "places.sqlite",
            "cookies.sqlite",
            "formhistory.sqlite",
            "cert9.db",
            "key4.db"
        ]
        
        for f in critical_files:
            p = self.profile_root / f
            if p.exists():
                os.utime(p, (timestamp, timestamp))

if __name__ == "__main__":
    # Test execution
    tm = TimeMachine("./lucid_profile_data/default")
    tm.warp()
