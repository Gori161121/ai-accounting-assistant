"""
Cash Flow Intelligence

Turns the transaction ledger into inflow/outflow, monthly net cash, an
estimated runway and a risk assessment.
"""
from __future__ import annotations

from collections import defaultdict

from ._utils import month_key, round2


def cash_flow_summary(transactions: list) -> dict:
    inflow = sum(t["amount"] for t in transactions if t["type"] == "inflow")
    outflow = sum(t["amount"] for t in transactions if t["type"] == "outflow")

    monthly = defaultdict(lambda: {"inflow": 0.0, "outflow": 0.0})
    for t in transactions:
        monthly[month_key(t["date"])][t["type"]] += t["amount"]

    monthly_net = []
    for m in sorted(monthly):
        row = monthly[m]
        monthly_net.append({
            "month": m,
            "inflow": round2(row["inflow"]),
            "outflow": round2(row["outflow"]),
            "net": round2(row["inflow"] - row["outflow"]),
        })

    net = inflow - outflow
    avg_monthly_outflow = outflow / len(monthly) if monthly else 0.0
    # Simple runway: current net cash / average monthly burn (if burning).
    recent_net = monthly_net[-1]["net"] if monthly_net else 0.0
    runway_months = round2(net / avg_monthly_outflow) if avg_monthly_outflow and net > 0 else 0.0

    if net < 0 and recent_net < 0:
        risk = "HIGH"
    elif net < 0 or recent_net < 0:
        risk = "MEDIUM"
    elif runway_months and runway_months < 3:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    return {
        "total_inflow": round2(inflow),
        "total_outflow": round2(outflow),
        "net_cash_flow": round2(net),
        "avg_monthly_outflow": round2(avg_monthly_outflow),
        "estimated_runway_months": runway_months,
        "cash_flow_risk": risk,
        "monthly": monthly_net,
    }
