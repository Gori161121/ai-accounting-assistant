"""
Customer Profitability Engine

Ranks customers by profit. Costs are allocated to each customer in proportion
to their share of total revenue (a common first-order allocation model).
"""
from __future__ import annotations

from collections import defaultdict

from ._utils import round2


def customer_profitability(invoices: list, expenses: list) -> dict:
    revenue: dict[str, float] = defaultdict(float)
    for i in invoices:
        revenue[i["customer"]] += i["amount"]

    total_revenue = sum(revenue.values())
    total_cost = sum(e["amount"] for e in expenses)

    rows = []
    for customer, rev in revenue.items():
        share = rev / total_revenue if total_revenue else 0.0
        allocated = total_cost * share
        profit = rev - allocated
        rows.append({
            "customer": customer,
            "revenue": round2(rev),
            "allocated_cost": round2(allocated),
            "profit": round2(profit),
            "margin_pct": round2(profit / rev * 100) if rev else 0.0,
        })

    rows.sort(key=lambda r: -r["profit"])
    return {
        "customers": rows,
        "most_profitable": rows[0]["customer"] if rows else None,
        "least_profitable": rows[-1]["customer"] if rows else None,
    }
