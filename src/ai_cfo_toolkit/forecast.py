"""Bear / base / bull forecasts and cash runway.

Deliberately simple and explainable: a run-rate forecast is the
average of the last N months, annualised for the months that remain.
Scenarios are explicit percentage adjustments, not hidden assumptions.
"""

from __future__ import annotations


def run_rate_forecast(monthly_actuals, months_remaining: int) -> float:
    """Forecast the rest of the year from the recent run rate.

    monthly_actuals: list of actuals for completed months.
    months_remaining: months left in the period.
    Returns average(monthly_actuals) * months_remaining.
    """
    if not monthly_actuals:
        raise ValueError("monthly_actuals must not be empty")
    if months_remaining < 0:
        raise ValueError("months_remaining must be >= 0")
    avg = sum(monthly_actuals) / len(monthly_actuals)
    return avg * months_remaining


def scenario_forecast(base: float, bear_pct: float = -0.10, bull_pct: float = 0.10) -> dict:
    """Return bear / base / bull values for a base forecast.

    bear_pct and bull_pct are signed fractions, e.g. -0.10 / +0.10.
    """
    return {
        "bear": base * (1 + bear_pct),
        "base": base,
        "bull": base * (1 + bull_pct),
    }


def months_runway(cash: float, monthly_burn: float) -> float | None:
    """Months of cash left at the current burn rate.

    Returns None when monthly_burn <= 0 (cash is not shrinking).
    """
    if monthly_burn <= 0:
        return None
    if cash <= 0:
        return 0.0
    return cash / monthly_burn
