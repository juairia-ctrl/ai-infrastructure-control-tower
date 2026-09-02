from __future__ import annotations

import pandas as pd

from utils.calculations import cost_variance_pct
from utils.config import HEALTH_THRESHOLDS, REVIEW_DATE, STATUS_ORDER


def worst_status(statuses) -> str:
    valid = [status for status in statuses if status in STATUS_ORDER]
    if not valid:
        return "GREEN"
    return max(valid, key=lambda status: STATUS_ORDER[status])


def classify_schedule_row(row: pd.Series) -> tuple[str, list[str]]:
    reasons: list[str] = []
    critical = str(row.get("critical_path", "")).lower() == "yes"
    remaining_float = int(row.get("remaining_float", 0))
    variance = int(row.get("variance_days", 0))
    consumed = float(row.get("float_consumed_pct", 0))

    if critical and remaining_float < HEALTH_THRESHOLDS["schedule_red_float_days"]:
        reasons.append(f"Critical-path forecast is {abs(remaining_float)} days beyond need-by.")
    if critical and row.get("milestone") in ["Commissioning Start", "Commissioning Complete", "Ready for Service"] and remaining_float < 0:
        reasons.append("Commissioning or launch milestone has no usable float.")
    if variance >= HEALTH_THRESHOLDS["variance_red_days"]:
        reasons.append(f"Forecast variance is {variance} days against baseline.")
    if reasons:
        return "RED", reasons

    if (
        remaining_float <= HEALTH_THRESHOLDS["schedule_yellow_float_days"]
        and (variance > 0 or row.get("forecast_moved_days", 0) > 0 or consumed >= HEALTH_THRESHOLDS["float_consumed_yellow_pct"])
        and row.get("milestone") != "Ready for Service"
    ):
        reasons.append(f"Only {remaining_float} days of float remain.")
    if consumed >= HEALTH_THRESHOLDS["float_consumed_yellow_pct"]:
        reasons.append(f"{consumed:.0%} of available float has been consumed.")
    if variance >= HEALTH_THRESHOLDS["variance_yellow_days"]:
        reasons.append(f"Forecast variance is {variance} days against baseline.")
    if row.get("forecast_moved_days", 0) >= 5:
        reasons.append(f"Forecast moved {int(row.get('forecast_moved_days'))} days since last review.")
    if reasons:
        return "YELLOW", reasons

    return "GREEN", ["Forecast is within variance tolerance and adequate float remains."]


def classify_schedule(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    classified = out.apply(classify_schedule_row, axis=1, result_type="expand")
    out["calculated_status"] = classified[0]
    out["status_drivers"] = classified[1].apply(lambda reasons: " ".join(reasons))
    return out


def classify_supplier_row(row: pd.Series) -> tuple[str, list[str]]:
    reasons: list[str] = []
    stale_days = (pd.Timestamp(REVIEW_DATE) - row["last_supplier_update"]).days
    if row["float_remaining"] < 0:
        reasons.append(f"Delivery forecast is {abs(int(row['float_remaining']))} days beyond site need-by.")
    if row["delivery_variance"] >= 14:
        reasons.append(f"Delivery variance is {int(row['delivery_variance'])} days.")
    if row["capacity_risk"] == "High":
        reasons.append("Supplier capacity risk is High.")
    if row["critical_input_status"] == "Change order required":
        reasons.append("Critical input requires a supplier change order.")
    if reasons:
        return "RED", reasons

    if row["float_remaining"] < HEALTH_THRESHOLDS["schedule_yellow_float_days"]:
        reasons.append(f"Only {int(row['float_remaining'])} days of delivery float remain.")
    if row["forecast_moved_days"] >= 5:
        reasons.append(f"Forecast delivery moved {int(row['forecast_moved_days'])} days since last review.")
    if row["production_slot_confirmed"] == "No":
        reasons.append("Production slot is not confirmed.")
    if stale_days > HEALTH_THRESHOLDS["supplier_stale_days"]:
        reasons.append(f"Supplier update is {stale_days} days old.")
    if row["recovery_plan_reliability"] == "Low":
        reasons.append("Recovery plan reliability is Low.")
    if reasons:
        return "YELLOW", reasons

    return "GREEN", ["Supplier milestones and delivery float remain within tolerance."]


def classify_suppliers(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    classified = out.apply(classify_supplier_row, axis=1, result_type="expand")
    out["calculated_risk"] = classified[0]
    out["risk_drivers"] = classified[1].apply(lambda reasons: " ".join(reasons))
    out["status_conflict"] = (
        (out["supplier_reported_status"] == "GREEN")
        & (out["calculated_risk"].isin(["YELLOW", "RED"]))
    )
    return out


def classify_cost_row(row: pd.Series) -> tuple[str, list[str]]:
    pct = cost_variance_pct(row["estimate_at_completion"], row["approved_budget"])
    exposure = row["pending_change_orders"] + row["expedite_exposure"] + row["potential_schedule_exposure"]
    if pct >= HEALTH_THRESHOLDS["cost_red_variance_pct"]:
        return "RED", [f"EAC is {pct:.1%} above approved budget.", f"Known exposure totals ${exposure:,.0f}."]
    if pct >= HEALTH_THRESHOLDS["cost_yellow_variance_pct"] or exposure >= 1_000_000:
        return "YELLOW", [f"Known exposure totals ${exposure:,.0f}.", f"EAC variance is {pct:.1%}."]
    return "GREEN", ["EAC remains within budget tolerance and exposure is limited."]


def classify_costs(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    classified = out.apply(classify_cost_row, axis=1, result_type="expand")
    out["cost_health"] = classified[0]
    out["cost_drivers"] = classified[1].apply(lambda reasons: " ".join(reasons))
    out["forecast_variance"] = out["estimate_at_completion"] - out["approved_budget"]
    return out


def site_health(sites: pd.DataFrame, milestones: pd.DataFrame, suppliers: pd.DataFrame, costs: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, site_row in sites.iterrows():
        site = site_row["site"]
        site_milestones = milestones[milestones["site"] == site]
        site_suppliers = suppliers[suppliers["site"] == site]
        site_costs = costs[costs["site"] == site]
        schedule_health = worst_status(site_milestones["calculated_status"].tolist())
        supply_health = worst_status(site_suppliers["calculated_risk"].tolist())
        cost_health = worst_status(site_costs["cost_health"].tolist())
        overall = worst_status([schedule_health, supply_health, cost_health])

        drivers = []
        for frame, status_col, driver_col in [
            (site_milestones, "calculated_status", "status_drivers"),
            (site_suppliers, "calculated_risk", "risk_drivers"),
            (site_costs, "cost_health", "cost_drivers"),
        ]:
            flagged = frame[frame[status_col] == overall] if overall != "GREEN" else frame
            if not flagged.empty:
                drivers.append(str(flagged.iloc[0][driver_col]))
        rows.append(
            {
                "Site": site,
                "Target Launch": site_row["target_launch"],
                "Reported Health": site_row["reported_health"],
                "Schedule": schedule_health,
                "Cost": cost_health,
                "Supply Chain": supply_health,
                "Overall Health": overall,
                "Primary Driver": drivers[0] if drivers else "No significant exception.",
                "Remaining Critical-Path Float": site_milestones["remaining_float"].min(),
                "Business Priority": site_row["business_priority"],
            }
        )
    return pd.DataFrame(rows)
