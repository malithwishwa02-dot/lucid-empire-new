import os
import sys

# Ensure tests can import the internal `core` package (camoufox/core)
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'camoufox'))
sys.path.insert(0, ROOT)
