import os
import time
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [TIME_MACHINE] - %(message)s')

def backdate_filesystem(target_path: str, days_ago: int = 90):
    """
    Traverses the target path and updates the access and modification times 
    of all files and directories to simulate history.
    """
    target_dir = Path(target_path)
    if not target_dir.exists():
        logging.error(f"Target path {target_path} does not exist.")
        return False

    # Calculate target timestamp
    target_timestamp = time.time() - (days_ago * 86400)
    
    count = 0
    try:
        # Update root directory first
        os.utime(target_dir, (target_timestamp, target_timestamp))
        
        for root, dirs, files in os.walk(target_dir):
            for d in dirs:
                dir_path = os.path.join(root, d)
                os.utime(dir_path, (target_timestamp, target_timestamp))
                count += 1
            for f in files:
                file_path = os.path.join(root, f)
                # Randomize slightly to avoid suspiciously identical timestamps
                random_offset = target_timestamp + (os.urandom(1)[0] % 3600) 
                os.utime(file_path, (random_offset, random_offset))
                count += 1
        
        logging.info(f"Successfully backdated {count} items in {target_path} to {days_ago} days ago.")
        return True
    except Exception as e:
        logging.error(f"Failed to backdate filesystem: {e}")
        return False

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        backdate_filesystem(sys.argv[1])
    else:
        print("Usage: python time_displacement.py <path>")
