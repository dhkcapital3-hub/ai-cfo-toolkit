# AI CFO Toolkit

Small, auditable FP&A helpers for startups and fractional CFOs.

No API keys. No network calls. No black box. Every number can be
traced back to its inputs, and every draft commentary is marked
for human review before it goes to a board or investor.

Built by Diana Kwon.

## What it does

- **Budget vs actual variance** — with favourability done right:
  revenue over budget is favourable, expenses over budget are not.
  Breaches are flagged only when they exceed *both* a % and a $ threshold.
- **Bear / base / bull forecasts** — run-rate forecast from recent
  months, with explicit scenario adjustments.
- **Cash runway** — months of cash left at the current burn rate.
- **Monthly CFO pack** — revenue, expenses, net, cash, runway,
  and flagged breaches in one dict, ready for a deck.
- **Draft variance commentary** — deterministic first-draft text
  with the exact numbers filled in. It never invents a cause.

## Quick start

```bash
python -m ai_cfo_toolkit.cli --example
```

Or with your own CSV (`line,actual,budget,kind`):

```bash
python -m ai_cfo_toolkit.cli --csv examples/sample_budget_actual.csv
```

In Python:

```python
from ai_cfo_toolkit import compute_variance, monthly_pack, scenario_forecast

v = compute_variance("Payroll", 62000, 58000, kind="expense")
print(v.amount, v.pct, v.favourable, v.breach)  # 4000 0.0689... False False

pack = monthly_pack(
    revenue_actual=118000, revenue_budget=110000,
    expense_actual=79600, expense_budget=78000,
    cash=420000, monthly_burn=35000,
)
print(pack["runway_months"])  # 12.0
print(scenario_forecast(300000))  # {'bear': 270000.0, 'base': 300000, 'bull': 330000.0}
```

## Tests

```bash
python -m pytest tests -q
```

## Status

v0.1.0 — early, focused, and intentionally small. The next steps
are real-world use: try it on a real month, file issues for the
lines and thresholds your close actually needs, and tell us what
the pack is missing.

## License

MIT — see `LICENSE`.
