"""
Accounting Intelligence Platform — API.

Exposes each intelligence service as an endpoint, plus a combined executive
report. Data comes from the loader (JSON scenario datasets standing in for
accounting integrations).
"""
from __future__ import annotations

from fastapi import FastAPI

from backend.data_loader import load_data
from backend.services import (
    cashflow_service,
    categorization_service,
    customer_profitability_service,
    expense_analytics_service,
    financial_health_service,
    forecasting_service,
    invoice_risk_service,
    kpi_service,
    profitability_service,
    report_generator,
    revenue_analytics_service,
    supplier_cost_service,
    tax_estimation_service,
)

app = FastAPI(
    title="Accounting Intelligence Platform API",
    description=(
        "A financial intelligence platform that unifies invoices, transactions, "
        "expenses and payroll and turns them into decision-ready business "
        "intelligence: cash flow, profitability, customer/supplier analytics, "
        "tax estimates, receivables risk, forecasting and AI executive summaries."
    ),
    version="0.2.0",
)


def _data() -> dict:
    return load_data()


# --- Meta -----------------------------------------------------------------

@app.get("/")
def root():
    return {
        "project": "Accounting Intelligence Platform",
        "positioning": "Financial intelligence for small and medium businesses",
        "status": "running",
    }


@app.get("/health")
def health():
    return {"status": "ok"}


# --- Raw data sources -----------------------------------------------------

@app.get("/invoices")
def invoices():
    return _data()["invoices"]


@app.get("/transactions")
def transactions():
    return _data()["transactions"]


@app.get("/expenses")
def expenses():
    return _data()["expenses"]


@app.get("/payroll")
def payroll():
    return _data()["payroll"]


# --- Intelligence services ------------------------------------------------

@app.get("/intelligence/categorization")
def categorization():
    return categorization_service.categorize_transactions(_data()["transactions"])


@app.get("/intelligence/cash-flow")
def cash_flow():
    return cashflow_service.cash_flow_summary(_data()["transactions"])


@app.get("/intelligence/expenses")
def expense_analytics():
    return expense_analytics_service.expense_breakdown(_data()["expenses"])


@app.get("/intelligence/revenue")
def revenue_analytics():
    return revenue_analytics_service.revenue_summary(_data()["invoices"])


@app.get("/intelligence/profitability")
def profitability():
    d = _data()
    return profitability_service.profitability(d["invoices"], d["expenses"], d["payroll"])


@app.get("/intelligence/customer-profitability")
def customer_profitability():
    d = _data()
    return customer_profitability_service.customer_profitability(d["invoices"], d["expenses"])


@app.get("/intelligence/supplier-costs")
def supplier_costs():
    return supplier_cost_service.supplier_costs(_data()["expenses"])


@app.get("/intelligence/invoice-risk")
def invoice_risk():
    return invoice_risk_service.invoice_risk(_data()["invoices"])


@app.get("/intelligence/tax-estimate")
def tax_estimate():
    d = _data()
    return tax_estimation_service.estimate_taxes(d["invoices"], d["expenses"], d["payroll"])


@app.get("/intelligence/forecast")
def forecast():
    return forecasting_service.forecast_cash(_data()["transactions"])


@app.get("/intelligence/financial-health")
def financial_health():
    d = _data()
    prof = profitability_service.profitability(d["invoices"], d["expenses"], d["payroll"])
    cash = cashflow_service.cash_flow_summary(d["transactions"])
    risk = invoice_risk_service.invoice_risk(d["invoices"])
    return financial_health_service.financial_health_score(prof, cash, risk)


@app.get("/kpis")
def kpis():
    return kpi_service.build_kpis(_data())


# --- Reports --------------------------------------------------------------

@app.get("/reports/executive")
def executive_report():
    return report_generator.build_executive_report(_data())
