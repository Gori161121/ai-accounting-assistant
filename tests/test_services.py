from backend.services import (
    cashflow_service,
    categorization_service,
    customer_profitability_service,
    expense_analytics_service,
    forecasting_service,
    invoice_risk_service,
    profitability_service,
    revenue_analytics_service,
    supplier_cost_service,
    tax_estimation_service,
)


def test_categorization_covers_all(data):
    result = categorization_service.categorize_transactions(data["transactions"])
    assert result["total_transactions"] == len(data["transactions"])
    assert result["categories"]


def test_categorize_transaction_rules():
    assert categorization_service.categorize_transaction("Monthly payroll") == "Payroll"
    assert categorization_service.categorize_transaction("AWS subscription") == "Software & SaaS"
    assert categorization_service.categorize_transaction("???") == "Uncategorized"


def test_cash_flow_identity(data):
    cf = cashflow_service.cash_flow_summary(data["transactions"])
    assert round(cf["total_inflow"] - cf["total_outflow"], 2) == cf["net_cash_flow"]
    assert cf["cash_flow_risk"] in {"LOW", "MEDIUM", "HIGH"}
    assert cf["monthly"]


def test_expense_shares_sum_to_100(data):
    exp = expense_analytics_service.expense_breakdown(data["expenses"])
    assert exp["total_expenses"] > 0
    share = sum(c["share_pct"] for c in exp["by_category"])
    assert abs(share - 100) < 1.0


def test_revenue_top_customers(data):
    rev = revenue_analytics_service.revenue_summary(data["invoices"])
    assert rev["total_revenue"] > 0
    assert len(rev["top_customers"]) <= 5


def test_profitability_identity(data):
    p = profitability_service.profitability(
        data["invoices"], data["expenses"], data["payroll"])
    assert round(p["total_revenue"] - p["total_cost"], 2) == p["net_profit"]
    assert round(p["operating_expenses"] + p["payroll"], 2) == p["total_cost"]


def test_customer_profit_allocation(data):
    cp = customer_profitability_service.customer_profitability(
        data["invoices"], data["expenses"])
    total_cost = sum(e["amount"] for e in data["expenses"])
    allocated = sum(c["allocated_cost"] for c in cp["customers"])
    # Allocated cost should sum to (approximately) total cost.
    assert abs(allocated - total_cost) < 1.0
    assert cp["most_profitable"]


def test_supplier_costs_sorted(data):
    sc = supplier_cost_service.supplier_costs(data["expenses"])
    spends = [s["total_spend"] for s in sc["suppliers"]]
    assert spends == sorted(spends, reverse=True)


def test_invoice_risk_structure(data):
    from datetime import date
    risk = invoice_risk_service.invoice_risk(data["invoices"], as_of=date(2026, 7, 1))
    assert risk["dso_days"] >= 0
    assert risk["receivables_risk"] in {"LOW", "MEDIUM", "HIGH"}
    assert risk["overdue_count"] == len(risk["overdue_invoices"])


def test_tax_estimate_totals(data):
    tax = tax_estimation_service.estimate_taxes(
        data["invoices"], data["expenses"], data["payroll"])
    assert round(tax["estimated_net_vat"] + tax["estimated_income_tax"], 2) == \
        tax["estimated_total_tax"]


def test_forecast_shape(data):
    fc = forecasting_service.forecast_cash(data["transactions"], months_ahead=3)
    assert len(fc["forecast"]) == 3
    assert fc["trend"] in {"improving", "declining", "flat", "insufficient_data"}
