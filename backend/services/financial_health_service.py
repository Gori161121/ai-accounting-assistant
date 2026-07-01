"""
Financial Health Score

A single composite 0-100 score combining profitability, cash-flow risk,
receivables health and cash runway — the platform's headline metric.
"""
from __future__ import annotations

from ._utils import round2

RISK_POINTS = {"LOW": 100, "MEDIUM": 60, "HIGH": 20}


def _margin_score(net_margin_pct: float) -> float:
    # 20%+ margin -> full marks; scales down to 0 at -10%.
    return max(0.0, min(100.0, (net_margin_pct + 10) / 30 * 100))


def _runway_score(runway_months: float) -> float:
    # 6+ months runway -> full marks.
    return max(0.0, min(100.0, runway_months / 6 * 100))


def financial_health_score(profitability: dict, cashflow: dict,
                           invoice_risk: dict) -> dict:
    margin = _margin_score(profitability.get("net_margin_pct", 0.0))
    cash = RISK_POINTS.get(cashflow.get("cash_flow_risk", "HIGH"), 20)
    receivables = RISK_POINTS.get(invoice_risk.get("receivables_risk", "HIGH"), 20)
    runway = _runway_score(cashflow.get("estimated_runway_months", 0.0))

    # Weighted composite.
    score = (margin * 0.35 + cash * 0.25 + receivables * 0.20 + runway * 0.20)
    score = round2(score)

    if score >= 75:
        rating = "STRONG"
    elif score >= 50:
        rating = "STABLE"
    elif score >= 30:
        rating = "AT_RISK"
    else:
        rating = "CRITICAL"

    return {
        "financial_health_score": score,
        "rating": rating,
        "components": {
            "profitability": round2(margin),
            "cash_flow": cash,
            "receivables": receivables,
            "runway": round2(runway),
        },
    }
