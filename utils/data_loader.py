from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from utils.calculations import add_schedule_fields, add_supplier_fields, quarter_label
from utils.health_engine import classify_costs, classify_schedule, classify_suppliers, site_health

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"


@st.cache_data
def load_csv(name: str) -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / name)


@st.cache_data
def load_model() -> dict[str, pd.DataFrame]:
    sites = load_csv("sites.csv")
    milestones = classify_schedule(add_schedule_fields(load_csv("milestones.csv")))
    suppliers = classify_suppliers(add_supplier_fields(load_csv("suppliers.csv")))
    costs = classify_costs(load_csv("costs.csv"))
    risks = load_csv("risks.csv")
    risks["risk_score"] = risks["probability"] * risks["impact"]
    changes = load_csv("changes.csv")
    decisions = load_csv("decisions.csv")
    pipeline = load_csv("forward_pipeline.csv")
    pipeline["need_by_quarter"] = pd.to_datetime(pipeline["need_by_date"]).apply(quarter_label)
    definitions = load_csv("data_definitions.csv")
    changed = load_csv("changes_since_last_review.csv")
    tradeoffs = load_csv("tradeoffs.csv")
    health = site_health(sites, milestones, suppliers, costs)
    return {
        "sites": sites,
        "milestones": milestones,
        "suppliers": suppliers,
        "costs": costs,
        "risks": risks,
        "changes": changes,
        "decisions": decisions,
        "pipeline": pipeline,
        "definitions": definitions,
        "changed": changed,
        "tradeoffs": tradeoffs,
        "health": health,
    }
