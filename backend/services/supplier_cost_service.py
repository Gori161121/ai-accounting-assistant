"""
Supplier Cost Intelligence

Total spend per supplier and detection of suppliers whose cost is rising
(comparing their first vs. latest active month).
"""
from __future__ import annotations

from collections import defaultdict

from ._utils import pct_change, round2

COST_INCREASE_THRESHOLD_PCT = 15.0


def supplier_costs(expenses: list) -> dict:
    spend: dict[str, float] = defaultdict(float)
    by_supplier_month: dict[str, dict[str, float]] = defaultdict(lambda: defaultdict(float))

    for e in expenses:
        spend[e["supplier"]] += e["amount"]
        by_supplier_month[e["supplier"]][e["date"][:7]] += e["amount"]

    rows = []
    for supplier, total in spend.items():
        months = sorted(by_supplier_month[supplier])
        change = 0.0
        if len(months) >= 2:
            change = pct_change(by_supplier_month[supplier][months[0]],
                                by_supplier_month[supplier][months[-1]])
        rows.append({
            "supplier": supplier,
            "total_spend": round2(total),
            "cost_change_pct": change,
        })

    rows.sort(key=lambda r: -r["total_spend"])
    getting_expensive = [r for r in rows if r["cost_change_pct"] >= COST_INCREASE_THRESHOLD_PCT]

    return {
        "suppliers": rows,
        "suppliers_getting_more_expensive": getting_expensive,
    }
