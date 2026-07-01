"""
AI Insight Service

Generates an executive summary and recommendations from the computed financial
context. Uses OpenAI (gpt-4o-mini) when OPENAI_API_KEY is set, otherwise a
rule-based fallback so the platform runs without any API key.

AI here assists decision-making — it does not replace accounting.
"""
from __future__ import annotations

import json
import os


def _rule_based_summary(context: dict) -> dict:
    health = context.get("health", {})
    cashflow = context.get("cashflow", {})
    profitability = context.get("profitability", {})
    expenses = context.get("expenses", {})
    receivables = context.get("invoice_risk", {})

    score = health.get("financial_health_score", "n/a")
    rating = health.get("rating", "n/a")
    net_profit = profitability.get("net_profit", 0)
    margin = profitability.get("net_margin_pct", 0)

    recommendations = []
    if cashflow.get("cash_flow_risk") in ("MEDIUM", "HIGH"):
        recommendations.append(
            f"Cash flow risk is {cashflow.get('cash_flow_risk')} — tighten spending "
            "and accelerate collections."
        )
    growing = expenses.get("fastest_growing")
    if growing and growing.get("change_pct", 0) > 0:
        recommendations.append(
            f"'{growing['category']}' expenses rose {growing['change_pct']}% — review this category."
        )
    if receivables.get("overdue_amount", 0) > 0:
        recommendations.append(
            f"{receivables.get('overdue_count', 0)} overdue invoices "
            f"({receivables.get('overdue_amount', 0)}) — follow up on collections."
        )
    if margin < 10:
        recommendations.append(
            f"Net margin is {margin}% — look for pricing or cost improvements."
        )
    if not recommendations:
        recommendations.append("Financials look healthy — maintain current controls.")

    summary = (
        f"Financial health score is {score}/100 ({rating}). "
        f"Net profit is {net_profit} at a {margin}% margin. "
        f"Cash-flow risk: {cashflow.get('cash_flow_risk', 'n/a')}; "
        f"receivables risk: {receivables.get('receivables_risk', 'n/a')}."
    )

    return {
        "summary": summary,
        "recommendations": recommendations,
        "generated_with": "rule-based-fallback",
    }


def _openai_summary(context: dict) -> dict:
    from openai import OpenAI

    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    prompt = (
        "You are a finance analyst assisting a business owner. Given this JSON "
        "financial context, return JSON with keys 'summary' (3-4 sentences in "
        "plain language) and 'recommendations' (array of 3-5 concrete actions).\n\n"
        f"{json.dumps(context)}"
    )
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        temperature=0.4,
    )
    result = json.loads(response.choices[0].message.content)
    result["generated_with"] = "openai"
    return result


def executive_summary(context: dict) -> dict:
    if os.getenv("OPENAI_API_KEY"):
        try:
            return _openai_summary(context)
        except Exception:
            return _rule_based_summary(context)
    return _rule_based_summary(context)
