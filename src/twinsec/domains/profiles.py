from __future__ import annotations

from twinsec.core.models import DomainProfile


def _p(name, signals, base, noise, unc, desc, weights=(1.0, -0.55, 0.22), tol=2.0):
    return DomainProfile(
        name=name,
        signals=signals,
        base=base,
        decay=(0.055, 0.085, 0.10),
        control_gain=(0.90, 0.55, 0.35),
        coupling=(0.0, 0.035, -0.020),
        noise=noise,
        uncertainty=unc,
        plausible_min=tuple(v - 8 * max(abs(v) * 0.25, 1.0) for v in base),
        plausible_max=tuple(v + 8 * max(abs(v) * 0.25, 1.0) for v in base),
        invariant_weights=weights,
        invariant_tolerance=tol,
        description=desc,
    )


DOMAIN_PROFILES = {
    "battery": _p(
        "battery",
        ("soc_pct", "voltage_v", "temperature_c"),
        (62.0, 380.0, 29.0),
        (0.18, 0.55, 0.10),
        (0.80, 2.0, 0.55),
        "Reduced-order battery management CPS profile.",
        (0.08, -0.012, 0.06), 2.8,
    ),
    "water": _p(
        "water",
        ("level_m", "flow_m3s", "pressure_bar"),
        (4.2, 1.7, 3.4),
        (0.015, 0.012, 0.012),
        (0.08, 0.07, 0.07),
        "Reduced-order water-treatment CPS profile.",
        (0.9, -1.4, 0.35), 0.45,
    ),
    "robot": _p(
        "robot",
        ("position_m", "velocity_ms", "range_m"),
        (12.0, 1.2, 8.0),
        (0.05, 0.025, 0.04),
        (0.32, 0.15, 0.28),
        "Planar autonomous robot CPS profile.",
        (0.12, -0.8, 0.09), 1.0,
    ),
    "microgrid": _p(
        "microgrid",
        ("frequency_hz", "voltage_pu", "power_balance_kw"),
        (50.0, 1.0, 0.0),
        (0.012, 0.002, 0.08),
        (0.08, 0.015, 0.65),
        "Smart microgrid CPS profile.",
        (0.04, 2.0, 0.01), 0.9,
    ),
    "factory": _p(
        "factory",
        ("temperature_c", "vibration_mms", "current_a"),
        (48.0, 2.1, 18.0),
        (0.10, 0.025, 0.08),
        (0.60, 0.16, 0.45),
        "Smart manufacturing CPS profile.",
        (0.04, -0.7, 0.08), 1.5,
    ),
    "ev_charging": _p(
        "ev_charging",
        ("soc_pct", "power_kw", "meter_energy_kwh"),
        (44.0, 11.0, 22.0),
        (0.15, 0.06, 0.08),
        (0.75, 0.40, 0.45),
        "EV charging and V2G CPS profile.",
        (0.08, -0.18, 0.06), 1.9,
    ),
    "railway": _p(
        "railway",
        ("position_m", "velocity_ms", "occupancy_score"),
        (120.0, 14.0, 0.8),
        (0.12, 0.06, 0.008),
        (0.70, 0.35, 0.08),
        "Abstract railway signaling CPS profile.",
        (0.006, -0.05, 1.0), 0.8,
    ),
}
