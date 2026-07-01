"""
Tax Estimation Engine

Produces a rough forward estimate of VAT and corporate income tax so owners
can set money aside. Rates are configurable; defaults are illustrative.
"""
from __future__ import annotations

from ._utils import round2

DEFAULT_VAT_RATE = 0.18
DEFAULT_INCOME_TAX_RATE = 0.20


def estimate_taxes(invoices: list, expenses: list, payroll: list,
                   vat_rate: float = DEFAULT_VAT_RATE,
                   income_tax_rate: float = DEFAULT_INCOME_TAX_RATE) -> dict:
    revenue = sum(i["amount"] for i in invoices)
    deductible = sum(e["amount"] for e in expenses) + sum(p["net"] for p in payroll)
    taxable_profit = max(0.0, revenue - deductible)

    # Net VAT = output VAT on sales - input VAT on expenses.
    output_vat = revenue * vat_rate
    input_vat = sum(e["amount"] for e in expenses) * vat_rate
    net_vat = max(0.0, output_vat - input_vat)

    income_tax = taxable_profit * income_tax_rate

    return {
        "vat_rate": vat_rate,
        "income_tax_rate": income_tax_rate,
        "estimated_net_vat": round2(net_vat),
        "taxable_profit": round2(taxable_profit),
        "estimated_income_tax": round2(income_tax),
        "estimated_total_tax": round2(net_vat + income_tax),
        "note": "Illustrative estimate — not tax advice.",
    }
