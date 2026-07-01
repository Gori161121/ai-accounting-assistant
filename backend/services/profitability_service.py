"""
Profitability Analysis

Revenue vs. total cost (operating expenses + payroll), net profit and margin,
overall and per month.
"""
from __future__ import annotations

from collections import defaultdict

from ._utils import round2


def profitability(invoices: list, expenses: list, payroll: list) -> dict:
    revenue = sum(i["amount"] for i in invoices)
    opex = sum(e["amount"] for e in expenses)
    payroll_total = sum(p["net"] for p in payroll)
    total_cost = opex + payroll_total
    net = revenue - total_cost
    net_margin = round2(net / revenue * 100) if revenue else 0.0

    rev_m: dict[str, float] = defaultdict(float)
    cost_m: dict[str, float] = defaultdict(float)
    for i in invoices:
        rev_m[i["issue_date"][:7]] += i["amount"]
    for e in expenses:
        cost_m[e["date"][:7]] += e["amount"]
    for p in payroll:
        cost_m[p["month"]] += p["net"]

    months = sorted(set(list(rev_m) + list(cost_m)))
    monthly = [{
        "month": m,
        "revenue": round2(rev_m[m]),
        "cost": round2(cost_m[m]),
        "profit": round2(rev_m[m] - cost_m[m]),
    } for m in months]

    return {
        "total_revenue": round2(revenue),
        "operating_expenses": round2(opex),
        "payroll": round2(payroll_total),
        "total_cost": round2(total_cost),
        "net_profit": round2(net),
        "net_margin_pct": net_margin,
        "monthly": monthly,
    }
