import pandas as pd
import streamlit as st

from utils.config import HEALTH_LOGIC_TEXT, REVIEW_DATE, STATUS_COLORS
from utils.data_loader import load_model
from utils.data_quality import data_quality_summary
from utils.executive_summary import portfolio_summary

st.set_page_config(
    page_title="AI Infrastructure Program Control Tower",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)


def inject_css() -> None:
    st.markdown(
        """
        <style>
        .block-container {padding-top: 1.5rem; padding-bottom: 2rem; max-width: 1440px;}
        h1, h2, h3 {letter-spacing: 0;}
        h1 {font-size: 2.1rem; margin-bottom: .2rem;}
        h2 {font-size: 1.35rem; margin-top: 1.4rem;}
        h3 {font-size: 1rem;}
        [data-testid="stMetricValue"] {font-size: 1.65rem;}
        [data-testid="stMetricLabel"] {font-size: .78rem; color: #475569;}
        .status-pill {padding: .18rem .55rem; border-radius: 999px; color: white; font-weight: 700; font-size: .78rem;}
        .brief-note {border-left: 4px solid #334155; padding: .7rem .9rem; background: #f8fafc; color: #1e293b;}
        .caption-box {font-size: .88rem; color: #475569; line-height: 1.4;}
        .stDataFrame {border: 1px solid #e2e8f0; border-radius: 6px;}
        </style>
        """,
        unsafe_allow_html=True,
    )


def status_badge(status: str) -> str:
    return f'<span class="status-pill" style="background:{STATUS_COLORS.get(status, "#475569")}">{status}</span>'


def money(value: float) -> str:
    return f"${value / 1_000_000:.1f}M"


def executive_brief() -> None:
    model = load_model()
    health = model["health"]
    risks = model["risks"]
    suppliers = model["suppliers"]
    costs = model["costs"]
    decisions = model["decisions"]
    milestones = model["milestones"]

    st.title("AI Infrastructure Program Control Tower")
    st.caption("Integrated schedule, cost, supply-chain, risk, and decision intelligence for concurrent AI infrastructure builds.")
    st.markdown(
        "<div class='brief-note'><b>Operating principle:</b> do not wait for the final milestone to turn Red. "
        "This prototype separates reported status from calculated program health using transparent leading indicators.</div>",
        unsafe_allow_html=True,
    )

    at_risk = health[health["Overall Health"].isin(["YELLOW", "RED"])]
    critical_at_risk = milestones[(milestones["critical_path"] == "Yes") & (milestones["calculated_status"].isin(["YELLOW", "RED"]))]
    supplier_risks = suppliers[suppliers["calculated_risk"].isin(["YELLOW", "RED"])]
    cost_exposure = (costs["pending_change_orders"] + costs["expedite_exposure"] + costs["potential_schedule_exposure"]).sum()
    open_decisions = decisions[decisions["status"] == "Open"]

    kpis = [
        ("ACTIVE SITES", len(health), None),
        ("SITES AT RISK", len(at_risk), None),
        ("CRITICAL-PATH ITEMS AT RISK", len(critical_at_risk), None),
        ("SUPPLIER RISKS", len(supplier_risks), None),
        ("FORECAST COST EXPOSURE", money(cost_exposure), None),
        ("DECISIONS REQUIRED", len(open_decisions), None),
    ]
    cols = st.columns(6)
    for col, (label, value, delta) in zip(cols, kpis):
        col.metric(label, value, delta)

    st.subheader("Portfolio Scorecard")
    scorecard = health.merge(
        decisions[decisions["status"] == "Open"][["site", "decision_required"]],
        how="left",
        left_on="Site",
        right_on="site",
    )
    scorecard["Decision Required"] = scorecard["decision_required"].fillna("No executive decision this cycle")
    scorecard = scorecard[
        ["Site", "Target Launch", "Schedule", "Cost", "Supply Chain", "Overall Health", "Primary Driver", "Decision Required"]
    ]
    st.dataframe(scorecard, hide_index=True, width="stretch")

    st.subheader("Portfolio Narrative")
    st.write(portfolio_summary(model))

    left, middle, right = st.columns([1.1, 1, 1.2])
    with left:
        st.subheader("Top Risks")
        top_risks = risks.sort_values("risk_score", ascending=False).head(4)
        st.dataframe(
            top_risks[["risk_id", "site", "type", "category", "description", "risk_score", "status"]],
            hide_index=True,
            width="stretch",
        )
    with middle:
        st.subheader("Early Warning Signals")
        warnings = suppliers[suppliers["status_conflict"] | (suppliers["float_remaining"] <= 7)][
            ["site", "equipment", "supplier_reported_status", "calculated_risk", "float_remaining", "risk_drivers"]
        ]
        st.dataframe(warnings, hide_index=True, width="stretch")
    with right:
        st.subheader("Decisions Required")
        st.dataframe(
            open_decisions[
                ["decision_id", "site", "decision_required", "recommended_action", "decision_owner", "decision_deadline"]
            ],
            hide_index=True,
            width="stretch",
        )

    with st.expander("Why the health labels are explainable"):
        st.write(HEALTH_LOGIC_TEXT)
        st.write("Thresholds are centralized in `utils/config.py`; the labels are not manually entered presentation statuses.")

    st.subheader("Data Quality / Trust")
    summary, details = data_quality_summary(model)
    c1, c2 = st.columns([0.8, 1.2])
    c1.dataframe(summary, hide_index=True, width="stretch")
    c2.dataframe(details, hide_index=True, width="stretch")


inject_css()
executive_brief()
