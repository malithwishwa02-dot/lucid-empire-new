"""
LUCID EMPIRE :: Fingerprint Handling
Legacy file retained for API compatibility but gutted of probabilistic logic.
"""

from dataclasses import dataclass
from typing import Any, Dict, Optional, Tuple

@dataclass
class ScreenFingerprint:
    """
    Stub for legacy compatibility.
    """
    pass

@dataclass
class Fingerprint:
    """
    Stub for legacy compatibility.
    """
    pass

def from_template_stub(fingerprint: Any, ff_version: Optional[str] = None) -> Dict[str, Any]:
    """
    Legacy stub. Returns empty dict.
    """
    return {}

def generate_fingerprint(window: Optional[Tuple[int, int]] = None, **config) -> Any:
    """
    Legacy stub. Raises error to enforce Golden Templates.
    """
    raise NotImplementedError(
        "LUCID PANIC: Probabilistic fingerprint generation is DISABLED. "
        "You must use a Golden Template."
    )
