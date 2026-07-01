"""
Data loader — reads the JSON scenario datasets that stand in for the various
financial data sources (invoices, bank transactions, expenses, payroll).

In production these would come from accounting integrations / a database; the
loader is the single boundary the rest of the app depends on.
"""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "data"
DATASETS = ("invoices", "transactions", "expenses", "payroll")


def _load(name: str) -> list:
    path = DATA_DIR / f"{name}.json"
    return json.loads(path.read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def load_data() -> dict:
    return {name: _load(name) for name in DATASETS}
