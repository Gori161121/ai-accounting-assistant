from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI(
    title="AI Accounting Assistant API",
    description="Financial intelligence and accounting operations prototype API.",
    version="0.1.0"
)

class Invoice(BaseModel):
    id: int
    customer: str
    amount: float
    status: str

class Expense(BaseModel):
    id: int
    category: str
    amount: float

invoices = [
    Invoice(id=1, customer="ABC Company", amount=1250.00, status="paid"),
    Invoice(id=2, customer="XYZ Ltd", amount=890.00, status="pending")
]

expenses = [
    Expense(id=1, category="Marketing", amount=450.00),
    Expense(id=2, category="Operations", amount=620.00)
]

@app.get("/")
def root():
    return {
        "project": "AI Accounting Assistant",
        "status": "running"
    }

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/invoices", response_model=List[Invoice])
def get_invoices():
    return invoices

@app.get("/expenses", response_model=List[Expense])
def get_expenses():
    return expenses

@app.get("/reports/monthly")
def monthly_report():
    revenue = sum(i.amount for i in invoices)
    costs = sum(e.amount for e in expenses)

    return {
        "revenue": revenue,
        "expenses": costs,
        "profit": revenue - costs
    }

@app.get("/finance/summary")
def finance_summary():
    revenue = sum(i.amount for i in invoices)
    costs = sum(e.amount for e in expenses)

    return {
        "total_revenue": revenue,
        "total_expenses": costs,
        "profit": revenue - costs,
        "recommendation": "Monitor expense growth and improve invoice collection."
    }
