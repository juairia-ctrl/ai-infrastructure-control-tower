import pandas as pd

from utils.calculations import cost_variance, float_consumed_pct, remaining_float_days, risk_score, variance_days
from utils.health_engine import classify_schedule_row


def test_variance_days():
    assert variance_days("2027-01-08", "2027-01-01") == 7


def test_remaining_float_days():
    assert remaining_float_days("2027-01-15", "2027-01-10") == 5


def test_float_consumed_pct():
    assert float_consumed_pct("2027-01-01", "2027-01-08", "2027-01-11") == 0.7


def test_schedule_health_classification_yellow_from_float_consumption():
    row = pd.Series(
        {
            "critical_path": "Yes",
            "remaining_float": 3,
            "variance_days": 9,
            "float_consumed_pct": 0.8,
            "forecast_moved_days": 5,
            "milestone": "Factory Acceptance Test",
        }
    )
    status, reasons = classify_schedule_row(row)
    assert status == "YELLOW"
    assert any("float" in reason.lower() for reason in reasons)


def test_risk_score():
    assert risk_score(4, 5) == 20


def test_cost_variance():
    assert cost_variance(139_400_000, 132_000_000) == 7_400_000
