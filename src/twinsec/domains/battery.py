from __future__ import annotations
from .registry import make_domain

def build(seed: int = 7):
    """Build the battery benchmark adapter."""
    return make_domain("battery", seed=seed)
