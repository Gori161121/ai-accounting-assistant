"""Small shared helpers for the intelligence services."""
from __future__ import annotations

from datetime import date, datetime


def parse_date(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


def month_key(value: str) -> str:
    """'2026-03-14' -> '2026-03'."""
    return value[:7]


def round2(x: float) -> float:
    return round(float(x or 0.0), 2)


def pct_change(old: float, new: float) -> float:
    if not old:
        return 0.0
    return round2((new - old) / old * 100)
