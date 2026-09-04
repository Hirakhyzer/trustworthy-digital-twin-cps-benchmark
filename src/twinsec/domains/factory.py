from __future__ import annotations
from .registry import make_domain

def build(seed: int = 7):
    """Build the factory benchmark adapter."""
    return make_domain("factory", seed=seed)
