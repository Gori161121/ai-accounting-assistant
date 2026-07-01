"""
Transaction Categorization Engine

Assigns a business category to a raw bank transaction from its description,
using keyword rules. This is the normalisation step every downstream analytic
depends on.
"""
from __future__ import annotations

from collections import defaultdict

CATEGORY_RULES = {
    "Revenue": ["invoice payment", "sale", "stripe payout", "revenue"],
    "Payroll": ["payroll", "salary", "wages"],
    "Rent": ["rent", "office lease", "city offices"],
    "Software & SaaS": ["aws", "adobe", "atlassian", "microsoft", "saas", "subscription"],
    "Marketing": ["ads", "google ads", "meta", "seo", "marketing"],
    "Utilities": ["powergrid", "aquacorp", "telco", "electricity", "water", "internet"],
    "Travel": ["air", "cab", "hotel", "stayinn", "travel"],
    "Bank Fees": ["bank", "fee", "charge"],
    "Professional Services": ["legal", "audit", "consult"],
    "Office Supplies": ["officemart", "paperco", "supplies"],
}


def categorize_transaction(description: str) -> str:
    text = (description or "").lower()
    for category, keywords in CATEGORY_RULES.items():
        if any(kw in text for kw in keywords):
            return category
    return "Uncategorized"


def categorize_transactions(transactions: list) -> dict:
    """Return per-category counts and how many needed auto-categorisation."""
    counts: dict[str, int] = defaultdict(int)
    auto_assigned = 0

    for tx in transactions:
        category = tx.get("category")
        if not category:
            category = categorize_transaction(tx.get("description", ""))
            auto_assigned += 1
        counts[category] += 1

    return {
        "total_transactions": len(transactions),
        "auto_categorized": auto_assigned,
        "categories": dict(sorted(counts.items(), key=lambda kv: -kv[1])),
    }
