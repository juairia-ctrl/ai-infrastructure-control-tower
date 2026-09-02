from datetime import date

REVIEW_DATE = date(2026, 9, 2)

HEALTH_THRESHOLDS = {
    "schedule_yellow_float_days": 5,
    "schedule_red_float_days": 0,
    "float_consumed_yellow_pct": 0.70,
    "variance_yellow_days": 7,
    "variance_red_days": 14,
    "supplier_stale_days": 7,
    "cost_yellow_variance_pct": 0.02,
    "cost_red_variance_pct": 0.05,
}

STATUS_ORDER = {"GREEN": 1, "YELLOW": 2, "RED": 3}
STATUS_COLORS = {"GREEN": "#147d64", "YELLOW": "#b7791f", "RED": "#c53030"}

HEALTH_LOGIC_TEXT = """
Schedule health is calculated from forecast variance, remaining float, critical-path exposure,
and float consumption. Yellow means the team still has options but leading indicators are
deteriorating. Red means a critical need-by date, commissioning milestone, launch milestone,
or credible mitigation path is exposed.
"""
