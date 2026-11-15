import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from ai_cfo_toolkit import (
    compute_variance,
    draft_variance_commentary,
    flag_breaches,
    monthly_pack,
    months_runway,
    run_rate_forecast,
    scenario_forecast,
)


def test_revenue_over_budget_is_favourable():
    v = compute_variance("Revenue", 118000, 110000, kind="revenue")
    assert v.amount == 8000
    assert v.favourable is True
    assert v.breach is False


def test_expense_over_budget_is_unfavourable_and_breaches():
    v = compute_variance("Payroll", 62000, 58000, kind="expense")
    assert v.amount == 4000
    assert v.favourable is False
    assert v.breach is False  # 6.9% is under the 10% threshold
    v2 = compute_variance("Payroll", 70000, 58000, kind="expense")
    assert v2.breach is True


def test_zero_budget_gives_none_pct():
    v = compute_variance("New line", 500, 0, kind="expense")
    assert v.pct is None


def test_flag_breaches_sorts_worst_first():
    rows = [
        {"line": "A", "actual": 12000, "budget": 10000, "kind": "expense"},
        {"line": "B", "actual": 20000, "budget": 10000, "kind": "expense"},
    ]
    out = flag_breaches(rows)
    assert [v.line for v in out] == ["B", "A"]


def test_run_rate_and_scenarios():
    assert run_rate_forecast([100, 110, 120], 2) == 220.0
    s = scenario_forecast(1000)
    assert s == {"bear": 900.0, "base": 1000, "bull": 1100.0}


def test_runway():
    assert months_runway(420000, 35000) == 12.0
    assert months_runway(100000, 0) is None


def test_commentary_does_not_invent_a_cause():
    v = compute_variance("Payroll", 70000, 58000, kind="expense")
    text = draft_variance_commentary(v)
    assert "DRAFT" in text
    assert "$70,000" in text
    assert "hiring" not in text.lower()


def test_monthly_pack():
    pack = monthly_pack(118000, 110000, 79600, 78000, cash=420000, monthly_burn=35000)
    assert pack["net"]["actual"] == 38400
    assert pack["runway_months"] == 12.0
