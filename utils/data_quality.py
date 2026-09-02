from __future__ import annotations

import pandas as pd

from utils.config import HEALTH_THRESHOLDS, REVIEW_DATE


def data_quality_summary(model: dict[str, pd.DataFrame]) -> tuple[pd.DataFrame, pd.DataFrame]:
    milestones = model["milestones"]
    suppliers = model["suppliers"]
    health = model["health"]

    checks = []
    checks.append(("Missing Forecast Dates", int(milestones["current_forecast_date"].isna().sum())))
    checks.append(("Missing Owners", int((milestones["owner"].isna() | (milestones["owner"] == "")).sum())))
    stale = int(((pd.Timestamp(REVIEW_DATE) - suppliers["last_supplier_update"]).dt.days > HEALTH_THRESHOLDS["supplier_stale_days"]).sum())
    checks.append(("Stale Supplier Updates", stale))
    checks.append(("Status Conflicts", int(suppliers["status_conflict"].sum())))
    checks.append(("Missing Need-By Dates", int(milestones["need_by_date"].isna().sum())))
    checks.append(("Forecast Later Than Need-By", int((milestones["current_forecast_date"] > milestones["need_by_date"]).sum())))
    checks.append(("Reported vs Calculated Site Mismatch", int((health["Reported Health"] != health["Overall Health"]).sum())))

    detail_rows = []
    for _, row in milestones[milestones["current_forecast_date"] > milestones["need_by_date"]].iterrows():
        detail_rows.append(
            {
                "Rule": "Forecast later than need-by",
                "Site": row["site"],
                "Item": row["milestone"],
                "Owner": row["owner"],
                "Severity": "High",
            }
        )
    for _, row in suppliers[suppliers["status_conflict"]].iterrows():
        detail_rows.append(
            {
                "Rule": "Reported Green conflicts with calculated risk",
                "Site": row["site"],
                "Item": row["equipment"],
                "Owner": row["owner"],
                "Severity": "Medium",
            }
        )
    for _, row in suppliers[(pd.Timestamp(REVIEW_DATE) - suppliers["last_supplier_update"]).dt.days > HEALTH_THRESHOLDS["supplier_stale_days"]].iterrows():
        detail_rows.append(
            {
                "Rule": "Supplier update older than 7 days",
                "Site": row["site"],
                "Item": row["equipment"],
                "Owner": row["owner"],
                "Severity": "Medium",
            }
        )

    summary = pd.DataFrame(checks, columns=["Check", "Value"])
    total_checks = len(milestones) * 4 + len(suppliers) * 2
    exception_count = int(summary["Value"].sum())
    completeness = max(0, 1 - exception_count / total_checks)
    summary.loc[len(summary)] = ["Data Completeness %", f"{completeness:.0%}"]
    summary["Value"] = summary["Value"].astype(str)
    return summary, pd.DataFrame(detail_rows)
