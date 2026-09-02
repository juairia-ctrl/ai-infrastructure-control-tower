from __future__ import annotations

import pandas as pd


def to_datetime(series: pd.Series) -> pd.Series:
    return pd.to_datetime(series, errors="coerce")


def variance_days(forecast, baseline) -> int:
    return int((pd.to_datetime(forecast) - pd.to_datetime(baseline)).days)


def remaining_float_days(need_by, forecast) -> int:
    return int((pd.to_datetime(need_by) - pd.to_datetime(forecast)).days)


def float_consumed_pct(baseline, forecast, need_by) -> float:
    baseline = pd.to_datetime(baseline)
    forecast = pd.to_datetime(forecast)
    need_by = pd.to_datetime(need_by)
    total_float = max((need_by - baseline).days, 0)
    if total_float == 0:
        return 1.0 if forecast > baseline else 0.0
    consumed = max((forecast - baseline).days, 0)
    return min(consumed / total_float, 1.5)


def risk_score(probability: int, impact: int) -> int:
    return int(probability) * int(impact)


def cost_variance(eac: float, approved_budget: float) -> float:
    return float(eac) - float(approved_budget)


def cost_variance_pct(eac: float, approved_budget: float) -> float:
    budget = float(approved_budget)
    if budget == 0:
        return 0.0
    return cost_variance(eac, approved_budget) / budget


def add_schedule_fields(milestones: pd.DataFrame) -> pd.DataFrame:
    df = milestones.copy()
    date_cols = ["baseline_date", "current_forecast_date", "need_by_date", "last_updated", "previous_forecast_date"]
    for col in date_cols:
        df[col] = to_datetime(df[col])
    df["variance_days"] = (df["current_forecast_date"] - df["baseline_date"]).dt.days
    df["remaining_float"] = (df["need_by_date"] - df["current_forecast_date"]).dt.days
    df["previous_remaining_float"] = (df["need_by_date"] - df["previous_forecast_date"]).dt.days
    df["float_consumed_pct"] = df.apply(
        lambda row: float_consumed_pct(row["baseline_date"], row["current_forecast_date"], row["need_by_date"]),
        axis=1,
    )
    df["forecast_moved_days"] = (df["current_forecast_date"] - df["previous_forecast_date"]).dt.days
    return df


def add_supplier_fields(suppliers: pd.DataFrame) -> pd.DataFrame:
    df = suppliers.copy()
    date_cols = [
        "po_date",
        "manufacturing_start",
        "factory_test_date",
        "committed_delivery",
        "current_forecast_delivery",
        "site_need_by_date",
        "last_supplier_update",
        "previous_forecast_delivery",
    ]
    for col in date_cols:
        df[col] = to_datetime(df[col])
    df["delivery_variance"] = (df["current_forecast_delivery"] - df["committed_delivery"]).dt.days
    df["float_remaining"] = (df["site_need_by_date"] - df["current_forecast_delivery"]).dt.days
    df["forecast_moved_days"] = (df["current_forecast_delivery"] - df["previous_forecast_delivery"]).dt.days
    return df


def quarter_label(date_value) -> str:
    dt = pd.to_datetime(date_value)
    return f"{dt.year} Q{((dt.month - 1) // 3) + 1}"
