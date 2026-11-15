"""Command line: run the example pack and variance check.

Usage:
    python -m ai_cfo_toolkit.cli --example
    python -m ai_cfo_toolkit.cli --csv examples/sample_budget_actual.csv
"""

from __future__ import annotations

import argparse
import csv
import json
import sys

from .commentary import draft_variance_commentary
from .forecast import months_runway, run_rate_forecast, scenario_forecast
from .pack import monthly_pack
from .variance import compute_variance


def _example():
    rows = [
        {"line": "Revenue", "actual": 118000, "budget": 110000, "kind": "revenue"},
        {"line": "Payroll", "actual": 62000, "budget": 58000, "kind": "expense"},
        {"line": "Software", "actual": 8400, "budget": 8000, "kind": "expense"},
        {"line": "Marketing", "actual": 9200, "budget": 12000, "kind": "expense"},
    ]
    print("Budget vs actual")
    for row in rows:
        v = compute_variance(row["line"], row["actual"], row["budget"], kind=row["kind"])
        print(f"  {v.line}: ${v.actual:,.0f} vs ${v.budget:,.0f} "
              f"({v.amount:+,.0f}, {v.pct:+.1%}) favourable={v.favourable} breach={v.breach}")
        print(f"    {draft_variance_commentary(v)}")
    pack = monthly_pack(118000, 110000, 79600, 78000, cash=420000, monthly_burn=35000, budget_rows=rows)
    print("\nMonthly pack")
    print(json.dumps(pack, indent=2))
    base = run_rate_forecast([98000, 105000, 118000], months_remaining=3)
    print("\nRun-rate revenue forecast, next 3 months:", f"${base:,.0f}")
    print("Scenarios:", {k: f"${x:,.0f}" for k, x in scenario_forecast(base).items()})
    print("Runway:", months_runway(420000, 35000), "months")


def _from_csv(path: str):
    with open(path, newline="") as f:
        rows = list(csv.DictReader(f))
    for row in rows:
        v = compute_variance(row["line"], float(row["actual"]), float(row["budget"]),
                             kind=row.get("kind", "expense"))
        print(f"{v.line}: ${v.actual:,.0f} vs ${v.budget:,.0f} "
              f"({v.amount:+,.0f}, {v.pct:+.1%}) favourable={v.favourable} breach={v.breach}")


def main(argv=None):
    p = argparse.ArgumentParser(description="AI CFO Toolkit")
    p.add_argument("--example", action="store_true", help="Run the built-in example")
    p.add_argument("--csv", help="Path to a budget-vs-actual CSV (line,actual,budget,kind)")
    args = p.parse_args(argv)
    if args.example:
        _example()
        return 0
    if args.csv:
        _from_csv(args.csv)
        return 0
    p.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
