"""
Report Generator (Financial Intelligence Engine)

Orchestrates every intelligence service into a single executive report and
attaches an AI-generated summary. This is the layer that turns accounting data
into a decision-ready document.
"""
from __future__ import annotations

from . import (
    ai_insight_service,
    cashflow_service,
    customer_profitability_service,
    expense_analytics_service,
    financial_health_service,
    forecasting_service,
    invoice_risk_service,
    kpi_service,
    profitability_service,
    revenue_analytics_service,
    supplier_cost_service,
    tax_estimation_service,
)


def build_executive_report(data: dict) -> dict:
    invoices = data["invoices"]
    transactions = data["transactions"]
    expenses = data["expenses"]
    payroll = data["payroll"]

    prof = profitability_service.profitability(invoices, expenses, payroll)
    cash = cashflow_service.cash_flow_summary(transactions)
    rev = revenue_analytics_service.revenue_summary(invoices)
    exp = expense_analytics_service.expense_breakdown(expenses)
    risk = invoice_risk_service.invoice_risk(invoices)
    health = financial_health_service.financial_health_score(prof, cash, risk)
    tax = tax_estimation_service.estimate_taxes(invoices, expenses, payroll)
    customers = customer_profitability_service.customer_profitability(invoices, expenses)
    suppliers = supplier_cost_service.supplier_costs(expenses)
    forecast = forecasting_service.forecast_cash(transactions)

    context = {
        "health": health,
        "cashflow": cash,
        "profitability": prof,
        "expenses": exp,
        "invoice_risk": risk,
    }
    ai = ai_insight_service.executive_summary(context)

    return {
        "report_type": "Monthly Executive Report",
        "financial_health": health,
        "kpis": kpi_service.build_kpis(data),
        "profitability": prof,
        "cash_flow": cash,
        "revenue": rev,
        "expenses": exp,
        "receivables": risk,
        "tax_estimate": tax,
        "customer_profitability": customers,
        "supplier_costs": suppliers,
        "forecast": forecast,
        "ai_executive_summary": ai,
    }
