"""Monthly CFO pack summary — one dict, ready to paste into a deck.

Inputs are plain numbers, outputs are plain numbers. No rounding
is hidden: amounts are rounded to whole dollars in the summary.
"""

from __future__ import annotations

from .forecast import months_runway
from .variance import compute_variance, flag_breaches


def monthly_pack(
    revenue_actual: float,
    revenue_budget: float,
    expense_actual: float,
    expense_budget: float,
    cash: float,
    monthly_burn: float,
    budget_rows=None,
    threshold_pct: float = 0.10,
    threshold_abs: float = 1000.0,
) -> dict:
    """Summarise a month for a board / investor update."""
    rev = compute_variance("Revenue", revenue_actual, revenue_budget, kind="revenue",
                            threshold_pct=threshold_pct, threshold_abs=threshold_abs)
    exp = compute_variance("Expenses", expense_actual, expense_budget, kind="expense",
                            threshold_pct=threshold_pct, threshold_abs=threshold_abs)
    net_actual = revenue_actual - expense_actual
    net_budget = revenue_budget - expense_budget
    breaches = []
    if budget_rows:
        breaches = [
            {"line": v.line, "amount": round(v.amount), "pct": v.pct}
            for v in flag_breaches(budget_rows, threshold_pct, threshold_abs)
        ]
    runway = months_runway(cash, monthly_burn)
    return {
        "revenue": {"actual": round(revenue_actual), "budget": round(revenue_budget),
                    "variance": round(rev.amount), "favourable": rev.favourable},
        "expenses": {"actual": round(expense_actual), "budget": round(expense_budget),
                     "variance": round(exp.amount), "favourable": exp.favourable},
        "net": {"actual": round(net_actual), "budget": round(net_budget),
                "variance": round(net_actual - net_budget)},
        "cash": round(cash),
        "monthly_burn": round(monthly_burn),
        "runway_months": round(runway, 1) if runway is not None else None,
        "breaches": breaches,
    }
