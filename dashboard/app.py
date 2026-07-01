"""Accounting Intelligence Platform — executive dashboard.

Reads from the FastAPI backend and renders KPIs, financial health, revenue and
expense trends, cash-flow forecast and the AI executive summary.

Run:  streamlit run dashboard/app.py
Env:  API_URL (default http://localhost:8000)
"""
from __future__ import annotations

import os

import httpx
import pandas as pd
import streamlit as st

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="Accounting Intelligence", page_icon="📊", layout="wide")


@st.cache_data(ttl=30)
def get(path: str):
    r = httpx.get(f"{API_URL}{path}", timeout=20)
    r.raise_for_status()
    return r.json()


st.title("📊 Accounting Intelligence Platform")
st.caption("Cash flow · Profitability · Receivables · Tax · Forecasting · AI insight")

try:
    report = get("/reports/executive")
except Exception as exc:  # noqa: BLE001
    st.error(f"Cannot reach the API at {API_URL}. Is the backend running?\n\n{exc}")
    st.stop()

kpis = report["kpis"]
health = report["financial_health"]

# --- Headline KPIs ---
c1, c2, c3, c4 = st.columns(4)
c1.metric("Health score", f"{health['financial_health_score']}", health["rating"])
c2.metric("Net profit", f"{kpis['net_profit']:,.0f}", f"{kpis['net_margin_pct']}%")
c3.metric("Net cash flow", f"{kpis['net_cash_flow']:,.0f}")
c4.metric("Overdue receivables", f"{kpis['overdue_amount']:,.0f}", f"DSO {kpis['dso_days']}d")

st.divider()
st.subheader("🤖 AI Executive Summary")
ai = report["ai_executive_summary"]
st.write(ai["summary"])
for rec in ai["recommendations"]:
    st.markdown(f"- {rec}")
st.caption(f"Generated with: {ai['generated_with']}")

st.divider()
left, right = st.columns(2)

with left:
    st.subheader("Revenue by month")
    rev = pd.DataFrame(report["revenue"]["monthly"])
    if not rev.empty:
        st.bar_chart(rev.set_index("month")["revenue"])

    st.subheader("Cash flow forecast")
    fc = report["forecast"]
    hist = pd.DataFrame(fc["history"]).assign(kind="actual")
    fut = pd.DataFrame(fc["forecast"]).assign(kind="forecast")
    combined = pd.concat([hist, fut], ignore_index=True)
    if not combined.empty:
        st.line_chart(combined.set_index("month")["net_cash"])
        st.caption(f"Trend: {fc['trend']}")

with right:
    st.subheader("Expenses by category")
    exp = pd.DataFrame(report["expenses"]["by_category"])
    if not exp.empty:
        st.bar_chart(exp.set_index("category")["amount"])

    st.subheader("Customer profitability")
    cust = pd.DataFrame(report["customer_profitability"]["customers"])
    if not cust.empty:
        st.dataframe(cust[["customer", "revenue", "profit", "margin_pct"]],
                     use_container_width=True, hide_index=True)

st.divider()
st.subheader("Tax estimate")
tax = report["tax_estimate"]
t1, t2, t3 = st.columns(3)
t1.metric("Net VAT", f"{tax['estimated_net_vat']:,.0f}")
t2.metric("Income tax", f"{tax['estimated_income_tax']:,.0f}")
t3.metric("Total", f"{tax['estimated_total_tax']:,.0f}")
st.caption(tax["note"])
