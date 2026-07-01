"""
Invoice Risk Detection & Late Payment Analysis

Finds overdue invoices, measures how often customers pay late, and computes
DSO (Days Sales Outstanding) — a core accounts-receivable health metric.
"""
from __future__ import annotations

from datetime import date

from ._utils import parse_date, round2


def invoice_risk(invoices: list, as_of: date | None = None) -> dict:
    as_of = as_of or date.today()

    overdue = []
    late_paid = 0
    paid_count = 0
    dso_days = []

    for inv in invoices:
        due = parse_date(inv["due_date"])
        issue = parse_date(inv["issue_date"])

        if inv["status"] != "paid":
            if due < as_of:
                overdue.append({
                    "id": inv["id"],
                    "customer": inv["customer"],
                    "amount": round2(inv["amount"]),
                    "days_overdue": (as_of - due).days,
                })
        else:
            paid_count += 1
            paid = parse_date(inv["paid_date"])
            dso_days.append((paid - issue).days)
            if paid > due:
                late_paid += 1

    overdue.sort(key=lambda r: -r["days_overdue"])
    dso = round2(sum(dso_days) / len(dso_days)) if dso_days else 0.0
    late_rate = round2(late_paid / paid_count * 100) if paid_count else 0.0
    overdue_amount = round2(sum(o["amount"] for o in overdue))

    if overdue_amount > 0 and late_rate > 20:
        risk = "HIGH"
    elif overdue_amount > 0 or late_rate > 10:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    return {
        "as_of": as_of.isoformat(),
        "overdue_count": len(overdue),
        "overdue_amount": overdue_amount,
        "overdue_invoices": overdue,
        "dso_days": dso,
        "late_payment_rate_pct": late_rate,
        "receivables_risk": risk,
    }
