"""
Revenue Analytics

Monthly revenue, latest-month growth and the top customers by revenue.
Uses pandas for the aggregation.
"""
from __future__ import annotations

import pandas as pd

from ._utils import pct_change, round2


def revenue_summary(invoices: list) -> dict:
    if not invoices:
        return {"total_revenue": 0.0, "monthly": [], "latest_month_growth_pct": 0.0,
                "top_customers": []}

    df = pd.DataFrame(invoices)
    df["month"] = df["issue_date"].str[:7]
    total = float(df["amount"].sum())

    by_month = df.groupby("month")["amount"].sum().sort_index()
    monthly = [{"month": m, "revenue": round2(a)} for m, a in by_month.items()]

    growth = 0.0
    if len(by_month) >= 2:
        growth = pct_change(float(by_month.iloc[-2]), float(by_month.iloc[-1]))

    by_customer = df.groupby("customer")["amount"].sum().sort_values(ascending=False)
    top_customers = [{"customer": c, "revenue": round2(a)}
                     for c, a in by_customer.head(5).items()]

    return {
        "total_revenue": round2(total),
        "monthly": monthly,
        "latest_month_growth_pct": growth,
        "top_customers": top_customers,
    }
