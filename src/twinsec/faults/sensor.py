from __future__ import annotations
from twinsec.attacks.manipulations import bias


def sensor_offset(record, key, amount):
    return bias(record, key, amount)
