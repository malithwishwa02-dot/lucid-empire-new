# LUCID EMPIRE :: eBPF/XDP ORCHESTRATOR
# Purpose: Load and manage eBPF/XDP programs for kernel-level masking

import subprocess
import os
import logging

class eBPFLoader:
    """Orchestrate eBPF and XDP program loading"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.xdp_program = None
        self.interface = None
    
    def load_xdp_program(self, interface: str, program_path: str) -> bool:
        """Load XDP program on network interface"""
        try:
            self.interface = interface
            # Use ip link set to attach XDP program
            cmd = [
                'ip', 'link', 'set', 'dev', interface,
                'xdp', 'obj', program_path
            ]
            result = subprocess.run(cmd, capture_output=True)
            
            if result.returncode == 0:
                self.logger.info(f"XDP program loaded on {interface}")
                return True
            else:
                self.logger.error(f"Failed to load XDP: {result.stderr.decode()}")
                return False
        except Exception as e:
            self.logger.error(f"XDP loading error: {e}")
            return False
    
    def unload_xdp_program(self) -> bool:
        """Unload XDP program from interface"""
        if not self.interface:
            return False
        
        try:
            cmd = ['ip', 'link', 'set', 'dev', self.interface, 'xdp', 'off']
            result = subprocess.run(cmd, capture_output=True)
            return result.returncode == 0
        except Exception as e:
            self.logger.error(f"XDP unload error: {e}")
            return False
    
    def is_loaded(self) -> bool:
        """Check if XDP program is loaded"""
        if not self.interface:
            return False
        
        try:
            cmd = ['ip', 'link', 'show', 'dev', self.interface]
            result = subprocess.run(cmd, capture_output=True, text=True)
            return 'xdp' in result.stdout
        except:
            return False
