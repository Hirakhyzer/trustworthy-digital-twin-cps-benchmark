from __future__ import annotations

from .base import GenericDomain
from .profiles import DOMAIN_PROFILES


def make_domain(name: str, seed: int = 7) -> GenericDomain:
    if name not in DOMAIN_PROFILES:
        raise KeyError(f"Unknown domain: {name}")
    return GenericDomain(DOMAIN_PROFILES[name], seed=seed)
