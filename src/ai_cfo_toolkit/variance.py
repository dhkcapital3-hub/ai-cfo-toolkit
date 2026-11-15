"""Budget-vs-actual variance.

Favourability depends on the line type, which is the mistake most
quick spreadsheets make:
- revenue: actual above budget is favourable
- expense: actual above budget is unfavourable
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Variance:
    line: str
    kind: str  # "revenue" or "expense"
    actual: float
    budget: float
    amount: float
    pct: float | None  # None when budget is 0
    favourable: bool
    breach: bool = False


def compute_variance(
    line: str,
    actual: float,
    budget: float,
    kind: str = "expense",
    threshold_pct: float = 0.10,
    threshold_abs: float = 1000.0,
) -> Variance:
    """Return the variance for one budget line.

    amount = actual - budget.
    pct = amount / budget, or None when budget is 0.
    A line breaches when it is unfavourable AND it exceeds both
    the percentage threshold and the absolute-dollar threshold.
    """
    if kind not in {"revenue", "expense"}:
        raise ValueError("kind must be 'revenue' or 'expense'")
    amount = actual - budget
    pct = (amount / budget) if budget != 0 else None
    if kind == "revenue":
        favourable = amount >= 0
    else:
        favourable = amount <= 0
    breach = False
    if not favourable and pct is not None:
        breach = abs(pct) >= threshold_pct and abs(amount) >= threshold_abs
    elif not favourable and budget == 0:
        breach = abs(amount) >= threshold_abs
    return Variance(
        line=line,
        kind=kind,
        actual=actual,
        budget=budget,
        amount=amount,
        pct=pct,
        favourable=favourable,
        breach=breach,
    )


def flag_breaches(rows, threshold_pct: float = 0.10, threshold_abs: float = 1000.0):
    """Flag unfavourable breaches from rows of dicts.

    Each row needs: line, actual, budget, and optionally kind.
    Returns only the breaching Variance objects, worst first.
    """
    out = []
    for row in rows:
        v = compute_variance(
            line=row["line"],
            actual=float(row["actual"]),
            budget=float(row["budget"]),
            kind=row.get("kind", "expense"),
            threshold_pct=threshold_pct,
            threshold_abs=threshold_abs,
        )
        if v.breach:
            out.append(v)
    out.sort(key=lambda v: abs(v.amount), reverse=True)
    return out
