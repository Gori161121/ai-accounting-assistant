-- AI Accounting Assistant
-- Financial Intelligence Database Schema v1

CREATE TABLE companies (
    id SERIAL PRIMARY KEY,
    company_name VARCHAR(120) NOT NULL,
    industry VARCHAR(80),
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE invoices (
    id SERIAL PRIMARY KEY,
    company_id INTEGER REFERENCES companies(id),
    invoice_number VARCHAR(50) NOT NULL,
    customer_name VARCHAR(120),
    amount DECIMAL(12,2) NOT NULL,
    status VARCHAR(30) DEFAULT 'pending',
    issued_date DATE,
    due_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE expenses (
    id SERIAL PRIMARY KEY,
    company_id INTEGER REFERENCES companies(id),
    category VARCHAR(80),
    amount DECIMAL(12,2) NOT NULL,
    expense_date DATE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE financial_reports (
    id SERIAL PRIMARY KEY,
    company_id INTEGER REFERENCES companies(id),
    report_type VARCHAR(80),
    reporting_period VARCHAR(50),
    revenue DECIMAL(12,2),
    expenses DECIMAL(12,2),
    profit DECIMAL(12,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE financial_insights (
    id SERIAL PRIMARY KEY,
    company_id INTEGER REFERENCES companies(id),
    insight_type VARCHAR(80),
    summary TEXT,
    recommendation TEXT,
    confidence_score DECIMAL(5,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_invoices_company ON invoices(company_id);
CREATE INDEX idx_expenses_company ON expenses(company_id);
CREATE INDEX idx_reports_company ON financial_reports(company_id);
CREATE INDEX idx_insights_company ON financial_insights(company_id);
