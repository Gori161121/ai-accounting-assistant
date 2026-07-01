"""
Financial Forecasting

Projects net cash flow for the next N months using a least-squares linear
trend over historical monthly net cash. Dependency-free (no numpy).
"""
from __future__ import annotations

from collections import defaultdict

from ._utils import month_key, round2


def _linear_fit(y: list[float]) -> tuple[float, float]:
    """Return (slope, intercept) of a best-fit line y = slope*x + intercept."""
    n = len(y)
    xs = list(range(n))
    mean_x = sum(xs) / n
    mean_y = sum(y) / n
    denom = sum((x - mean_x) ** 2 for x in xs)
    if denom == 0:
        return 0.0, mean_y
    slope = sum((xs[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / denom
    intercept = mean_y - slope * mean_x
    return slope, intercept


def forecast_cash(transactions: list, months_ahead: int = 3) -> dict:
    monthly = defaultdict(float)
    for t in transactions:
        sign = 1 if t["type"] == "inflow" else -1
        monthly[month_key(t["date"])] += sign * t["amount"]

    ordered_months = sorted(monthly)
    history = [round2(monthly[m]) for m in ordered_months]

    if len(history) < 2:
        return {"history": [{"month": m, "net_cash": monthly[m]} for m in ordered_months],
                "forecast": [], "trend": "insufficient_data"}

    slope, intercept = _linear_fit(history)
    n = len(history)

    # Generate future month labels
    last = ordered_months[-1]
    year, month = int(last[:4]), int(last[5:7])
    forecast = []
    for k in range(1, months_ahead + 1):
        month += 1
        if month > 12:
            month = 1
            year += 1
        predicted = slope * (n - 1 + k) + intercept
        forecast.append({"month": f"{year:04d}-{month:02d}", "net_cash": round2(predicted)})

    trend = "improving" if slope > 0 else "declining" if slope < 0 else "flat"

    return {
        "history": [{"month": m, "net_cash": round2(monthly[m])} for m in ordered_months],
        "forecast": forecast,
        "monthly_trend_slope": round2(slope),
        "trend": trend,
    }
