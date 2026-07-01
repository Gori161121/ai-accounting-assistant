"""
KPI Engine

Rolls the individual intelligence services up into the handful of numbers a
business owner actually watches.
"""
from __future__ import annotations

from . import (
    cashflow_service,
    financial_health_service,
    invoice_risk_service,
    profitability_service,
    revenue_analytics_service,
)


def build_kpis(data: dict) -> dict:
    prof = profitability_service.profitability(
        data["invoices"], data["expenses"], data["payroll"])
    cash = cashflow_service.cash_flow_summary(data["transactions"])
    rev = revenue_analytics_service.revenue_summary(data["invoices"])
    risk = invoice_risk_service.invoice_risk(data["invoices"])
    health = financial_health_service.financial_health_score(prof, cash, risk)

    return {
        "total_revenue": prof["total_revenue"],
        "net_profit": prof["net_profit"],
        "net_margin_pct": prof["net_margin_pct"],
        "net_cash_flow": cash["net_cash_flow"],
        "estimated_runway_months": cash["estimated_runway_months"],
        "revenue_growth_pct": rev["latest_month_growth_pct"],
        "dso_days": risk["dso_days"],
        "overdue_amount": risk["overdue_amount"],
        "financial_health_score": health["financial_health_score"],
        "rating": health["rating"],
    }
