"""AI CFO Toolkit — small, auditable FP&A helpers for startups.

Built for fractional CFOs and founders who need a fast, explainable
monthly close: budget-vs-actual variance, bear/base/bull forecasts,
cash runway, and a draft CFO pack summary.

No API keys, no network calls, no black box. Every number can be
traced back to its inputs, and every draft commentary is marked
for human review before it goes to a board or investor.
"""

from .commentary import draft_variance_commentary
from .forecast import months_runway, run_rate_forecast, scenario_forecast
from .pack import monthly_pack
from .variance import compute_variance, flag_breaches

__all__ = [
    "compute_variance",
    "flag_breaches",
    "months_runway",
    "run_rate_forecast",
    "scenario_forecast",
    "draft_variance_commentary",
    "monthly_pack",
]

__version__ = "0.1.0"
