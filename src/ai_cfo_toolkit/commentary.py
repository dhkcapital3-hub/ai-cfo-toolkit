"""Draft variance commentary — deterministic templates, not AI output.

The point is speed for a first draft, with the numbers filled in
exactly. A human must still review it: every draft is labelled
as a draft, and it never invents a cause (hiring, churn, pricing)
that is not in the inputs.
"""

from __future__ import annotations

from .variance import Variance


def draft_variance_commentary(v: Variance) -> str:
    """Return a one-paragraph draft for one Variance."""
    direction = "favourable" if v.favourable else "unfavourable"
    pct_text = f"{v.pct:+.1%}" if v.pct is not None else "n/a (budget was $0)"
    amount_text = f"${v.amount:,.0f}"
    if v.kind == "revenue":
        what = "Revenue"
    else:
        what = "Spend"
    flag = " — FLAGGED: exceeds the variance threshold, review before the pack goes out." if v.breach else ""
    return (
        f"DRAFT — human review required. {what} on '{v.line}' was "
        f"${v.actual:,.0f} vs. a budget of ${v.budget:,.0f} "
        f"({amount_text}, {pct_text}), which is {direction}.{flag}"
    )
