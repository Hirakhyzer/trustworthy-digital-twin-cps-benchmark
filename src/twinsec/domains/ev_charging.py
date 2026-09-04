from __future__ import annotations
from .registry import make_domain

def build(seed: int = 7):
    """Build the ev_charging benchmark adapter."""
    return make_domain("ev_charging", seed=seed)
