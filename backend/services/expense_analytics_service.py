"""
Expense Analytics

Breaks spending down by category, tracks the monthly trend and flags the
fastest-growing category. Uses pandas for the aggregation.
"""
from __future__ import annotations

import pandas as pd

from ._utils import pct_change, round2


def expense_breakdown(expenses: list) -> dict:
    if not expenses:
        return {"total_expenses": 0.0, "by_category": [], "monthly_trend": [],
                "fastest_growing": None}

    df = pd.DataFrame(expenses)
    df["month"] = df["date"].str[:7]
    total = float(df["amount"].sum())

    by_cat = df.groupby("category")["amount"].sum().sort_values(ascending=False)
    by_category = [
        {"category": cat, "amount": round2(amt), "share_pct": round2(amt / total * 100)}
        for cat, amt in by_cat.items()
    ]

    by_month = df.groupby("month")["amount"].sum().sort_index()
    monthly_trend = [{"month": m, "amount": round2(a)} for m, a in by_month.items()]

    fastest_growing = None
    months = sorted(df["month"].unique())
    if len(months) >= 2:
        pivot = df.pivot_table(index="category", columns="month", values="amount",
                               aggfunc="sum", fill_value=0)
        first, last = months[0], months[-1]
        changes = [(cat, pct_change(pivot.loc[cat, first], pivot.loc[cat, last]))
                   for cat in pivot.index]
        changes.sort(key=lambda x: -x[1])
        if changes:
            fastest_growing = {"category": changes[0][0], "change_pct": changes[0][1]}

    return {
        "total_expenses": round2(total),
        "by_category": by_category,
        "monthly_trend": monthly_trend,
        "fastest_growing": fastest_growing,
    }
