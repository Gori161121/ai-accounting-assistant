"""
Deterministic sample-data generator for the Financial Intelligence Platform.

Produces six months of realistic invoices, bank transactions, expenses and
payroll as JSON scenario datasets under backend/data/. Uses a fixed seed so
the numbers are reproducible in CI, tests and screenshots.

Run:  python backend/data_generator.py
"""
from __future__ import annotations

import json
import random
from datetime import date, timedelta
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "data"

CUSTOMERS = ["Northwind Ltd", "Globex Corp", "Umbrella Inc", "Initech",
             "Soylent Co", "Hooli", "Acme Retail", "Stark Industries"]

EXPENSE_CATEGORIES = {
    "Rent": ["City Offices Ltd"],
    "Software & SaaS": ["Atlassian", "Adobe", "AWS", "Microsoft"],
    "Marketing": ["Google Ads", "Meta Ads", "SEO Agency"],
    "Utilities": ["PowerGrid", "AquaCorp", "Telco"],
    "Travel": ["SkyLine Air", "CityCabs", "StayInn"],
    "Office Supplies": ["OfficeMart", "PaperCo"],
    "Professional Services": ["LegalPartners", "AuditFirm"],
    "Bank Fees": ["First National Bank"],
}

START = date(2026, 1, 1)
MONTHS = 6


def _month_range():
    d = START
    for _ in range(MONTHS):
        yield d
        # advance one month
        if d.month == 12:
            d = date(d.year + 1, 1, 1)
        else:
            d = date(d.year, d.month + 1, 1)


def generate(seed: int = 7) -> dict:
    rng = random.Random(seed)

    invoices = []
    transactions = []
    expenses = []
    payroll = []

    inv_id = tx_id = exp_id = pay_id = 1
    revenue_trend = 1.0

    for m in _month_range():
        # --- Invoices (revenue), slight upward trend + noise ---
        revenue_trend *= rng.uniform(1.02, 1.09)
        n_invoices = rng.randint(6, 10)
        for _ in range(n_invoices):
            issue = m + timedelta(days=rng.randint(0, 27))
            due = issue + timedelta(days=30)
            base = rng.uniform(800, 6000) * revenue_trend
            amount = round(base, 2)
            # payment behaviour
            roll = rng.random()
            if roll < 0.7:
                status = "paid"
                paid = issue + timedelta(days=rng.randint(3, 28))
            elif roll < 0.85:
                status = "paid"
                paid = due + timedelta(days=rng.randint(1, 20))  # late but paid
            else:
                status = "pending"
                paid = None
            customer = rng.choice(CUSTOMERS)
            invoices.append({
                "id": inv_id,
                "customer": customer,
                "amount": amount,
                "currency": "USD",
                "issue_date": issue.isoformat(),
                "due_date": due.isoformat(),
                "paid_date": paid.isoformat() if paid else None,
                "status": status,
            })
            if paid:
                transactions.append({
                    "id": tx_id, "date": paid.isoformat(), "type": "inflow",
                    "amount": amount, "category": "Revenue",
                    "description": f"Invoice payment - {customer}",
                    "counterparty": customer,
                })
                tx_id += 1
            inv_id += 1

        # --- Expenses (outflow) ---
        for category, suppliers in EXPENSE_CATEGORIES.items():
            if category == "Rent":
                amount = 3500.0
            elif category == "Marketing":
                amount = round(rng.uniform(1500, 4200) * revenue_trend, 2)
            else:
                amount = round(rng.uniform(150, 1800), 2)
            supplier = rng.choice(suppliers)
            d = m + timedelta(days=rng.randint(1, 27))
            expenses.append({
                "id": exp_id, "date": d.isoformat(), "category": category,
                "amount": amount, "supplier": supplier,
            })
            transactions.append({
                "id": tx_id, "date": d.isoformat(), "type": "outflow",
                "amount": amount, "category": category,
                "description": f"{category} - {supplier}", "counterparty": supplier,
            })
            exp_id += 1
            tx_id += 1

        # --- Payroll (monthly outflow) ---
        headcount = 8
        gross = round(headcount * rng.uniform(3200, 4200), 2)
        net = round(gross * 0.78, 2)
        pay_day = m + timedelta(days=27)
        payroll.append({
            "id": pay_id, "month": m.strftime("%Y-%m"),
            "employee_count": headcount, "gross": gross, "net": net,
        })
        transactions.append({
            "id": tx_id, "date": pay_day.isoformat(), "type": "outflow",
            "amount": net, "category": "Payroll",
            "description": "Monthly payroll", "counterparty": "Employees",
        })
        pay_id += 1
        tx_id += 1

    return {
        "invoices": invoices,
        "transactions": transactions,
        "expenses": expenses,
        "payroll": payroll,
    }


def write_datasets() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    data = generate()
    for name, rows in data.items():
        (DATA_DIR / f"{name}.json").write_text(json.dumps(rows, indent=2))
    print(f"Wrote {sum(len(v) for v in data.values())} records to {DATA_DIR}")


if __name__ == "__main__":
    write_datasets()
