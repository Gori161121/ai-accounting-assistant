# Accounting Intelligence Platform

![CI](https://github.com/Gori161121/ai-accounting-assistant/actions/workflows/ci.yml/badge.svg)
![License: MIT](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.11-blue)

A financial intelligence platform for small and medium businesses. It unifies
invoices, bank transactions, expenses and payroll, then continuously analyses
them to answer the questions an owner actually cares about — not just "what are
the numbers" but "what do they mean and what should I do".

It is deliberately **not** a bookkeeping CRUD app. The value is in the
intelligence layer: each service takes financial data and returns a decision.

Questions it answers:

- Where is the company losing money?
- Which expenses are increasing, and which supplier got more expensive?
- Is cash flow becoming risky? How many months of runway are left?
- Which customers are the most profitable?
- Which invoices are overdue, and how late do customers usually pay?
- What taxes should be set aside?
- What should management pay attention to next?

## Architecture

```
Data sources (invoices, transactions, expenses, payroll)
        ↓
Data loader / validation
        ↓
Intelligence services  (one service per business problem)
        ↓
Financial Intelligence Engine (report generator)
        ↓
API  ·  Dashboard
```

## Intelligence services

| Service | Question it answers |
| --- | --- |
| Transaction Categorization | What kind of spending is this? |
| Cash Flow Intelligence | Is cash flow healthy? What's the runway? |
| Expense Analytics | Where does the money go? What's growing? |
| Revenue Analytics | How is revenue trending? Who are the top customers? |
| Profitability Analysis | Are we actually profitable? |
| Customer Profitability | Which customers make us money? |
| Supplier Cost Intelligence | Which suppliers got more expensive? |
| Invoice Risk & Late Payment | What's overdue? What's our DSO? |
| Tax Estimation | What tax should we expect? |
| Financial Forecasting | Where is cash heading next quarter? |
| Financial Health Score | One number for overall health |
| KPI Engine | The metrics owners watch |
| AI Executive Summary | Plain-language explanation + recommendations |
| Report Generator | Combined executive report |

## Running it

```bash
cd backend
pip install -r requirements.txt
uvicorn backend.main:app --reload      # run from the repo root
```

API at `http://localhost:8000`, interactive docs at `http://localhost:8000/docs`.

With Docker:

```bash
docker compose up --build
```

Dashboard:

```bash
pip install -r dashboard/requirements.txt
streamlit run dashboard/app.py
```

Regenerate the sample datasets (deterministic):

```bash
python backend/data_generator.py
```

## Key endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/kpis` | Headline KPIs |
| GET | `/intelligence/financial-health` | Composite health score |
| GET | `/intelligence/cash-flow` | Cash-flow intelligence |
| GET | `/intelligence/profitability` | Profit & margins |
| GET | `/intelligence/revenue` | Revenue analytics |
| GET | `/intelligence/expenses` | Expense analytics |
| GET | `/intelligence/customer-profitability` | Profit per customer |
| GET | `/intelligence/supplier-costs` | Supplier cost intelligence |
| GET | `/intelligence/invoice-risk` | Overdue + late-payment analysis |
| GET | `/intelligence/tax-estimate` | VAT & income-tax estimate |
| GET | `/intelligence/forecast` | Cash-flow forecast |
| GET | `/reports/executive` | Full executive report + AI summary |

Example — `/kpis`:

```json
{
  "total_revenue": 203945.74,
  "net_profit": -9314.06,
  "net_margin_pct": -4.57,
  "net_cash_flow": -55127.36,
  "dso_days": 17.63,
  "overdue_amount": 34812.59,
  "financial_health_score": 43.34,
  "rating": "AT_RISK"
}
```

(The sample dataset intentionally models a business under pressure, so the
risk-detection features are visible.)

## Project layout

```
backend/
  main.py               FastAPI app — one endpoint per service
  data_loader.py        single data boundary
  data_generator.py     deterministic sample-data generator
  data/                 JSON scenario datasets
  services/             the intelligence services (one problem each)
dashboard/              Streamlit executive dashboard
tests/                  pytest
database/               SQL schema + ERD (persistence roadmap)
```

## Tests

```bash
PYTHONPATH=. pytest -q
```

## Roadmap

- Persist data in PostgreSQL via SQLAlchemy (schema already in `database/`)
- Budget monitoring & variance analysis
- Multi-currency support
- Scheduled report delivery (weekly / monthly)

## License

MIT — see [LICENSE](LICENSE).
