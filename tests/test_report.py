import os

from backend.services import (
    cashflow_service,
    financial_health_service,
    invoice_risk_service,
    kpi_service,
    profitability_service,
    report_generator,
)


def test_financial_health_range(data):
    prof = profitability_service.profitability(
        data["invoices"], data["expenses"], data["payroll"])
    cash = cashflow_service.cash_flow_summary(data["transactions"])
    risk = invoice_risk_service.invoice_risk(data["invoices"])
    health = financial_health_service.financial_health_score(prof, cash, risk)
    assert 0 <= health["financial_health_score"] <= 100
    assert health["rating"] in {"STRONG", "STABLE", "AT_RISK", "CRITICAL"}


def test_kpis_keys(data):
    kpis = kpi_service.build_kpis(data)
    for key in ("total_revenue", "net_profit", "financial_health_score", "rating"):
        assert key in kpis


def test_executive_report_sections(data):
    os.environ.pop("OPENAI_API_KEY", None)  # force deterministic AI fallback
    report = report_generator.build_executive_report(data)
    for section in ("financial_health", "kpis", "profitability", "cash_flow",
                    "revenue", "expenses", "receivables", "tax_estimate",
                    "customer_profitability", "supplier_costs", "forecast",
                    "ai_executive_summary"):
        assert section in report
    ai = report["ai_executive_summary"]
    assert ai["generated_with"] == "rule-based-fallback"
    assert ai["summary"]
    assert len(ai["recommendations"]) >= 1
