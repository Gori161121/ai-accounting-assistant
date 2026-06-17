# Database Design

## Overview

The database serves as the central source of truth for all accounting operations, financial records, reports, and AI-powered analysis.

The design focuses on scalability, automation readiness, and financial visibility.

---

## Main Entities

### Companies

Fields:

- company_id
- company_name
- industry
- status

---

### Transactions

Fields:

- transaction_id
- company_id
- transaction_type
- amount
- date
- category

---

### Expenses

Fields:

- expense_id
- company_id
- category
- amount
- date
- notes

---

### Invoices

Fields:

- invoice_id
- company_id
- invoice_number
- amount
- due_date
- status

---

### Reports

Fields:

- report_id
- company_id
- report_type
- generated_date
- summary

---

### AI Insights

Fields:

- insight_id
- company_id
- generated_date
- recommendation
- confidence_score

---

## Database Relationships

Companies → Transactions

Companies → Expenses

Companies → Invoices

Companies → Reports

Companies → AI Insights

---

## Planned Technologies

- PostgreSQL
- SQL
- Supabase
- Airtable

---

## Future Improvements

- Financial forecasting
- Cash flow prediction
- Risk analysis
- AI financial advisor
- Executive dashboards
