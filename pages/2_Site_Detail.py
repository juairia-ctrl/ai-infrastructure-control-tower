import streamlit as st

from utils.data_loader import load_model
from utils.executive_summary import site_summary

st.set_page_config(page_title="Site Detail", layout="wide")
model = load_model()

st.title("Site Detail")
site = st.selectbox("Select site", model["sites"]["site"].tolist(), index=1)

health = model["health"].set_index("Site").loc[site]
milestones = model["milestones"][model["milestones"]["site"] == site]
suppliers = model["suppliers"][model["suppliers"]["site"] == site]
costs = model["costs"][model["costs"]["site"] == site]
risks = model["risks"][model["risks"]["site"] == site].sort_values("risk_score", ascending=False)
changes = model["changes"][model["changes"]["site"] == site]
decisions = model["decisions"][model["decisions"]["site"].isin([site, "Portfolio"])]

cols = st.columns(7)
cols[0].metric("Target Launch", str(health["Target Launch"]))
cols[1].metric("Calculated Health", health["Overall Health"])
cols[2].metric("Reported Health", health["Reported Health"])
cols[3].metric("Schedule", health["Schedule"])
cols[4].metric("Cost", health["Cost"])
cols[5].metric("Supply Chain", health["Supply Chain"])
cols[6].metric("Min CP Float", f"{int(health['Remaining Critical-Path Float'])} days")

st.subheader("Rule-Based Executive Summary")
st.write(site_summary(site, model))

tab_schedule, tab_supplier, tab_cost, tab_risk, tab_decision = st.tabs(
    ["Schedule", "Supplier Risks", "Cost / Change", "Risks", "Decisions"]
)
with tab_schedule:
    st.dataframe(
        milestones[
            [
                "workstream",
                "milestone",
                "baseline_date",
                "current_forecast_date",
                "need_by_date",
                "remaining_float",
                "reported_status",
                "calculated_status",
                "status_drivers",
            ]
        ],
        hide_index=True,
        width="stretch",
    )
with tab_supplier:
    st.dataframe(
        suppliers[
            [
                "equipment",
                "supplier",
                "supplier_reported_status",
                "calculated_risk",
                "status_conflict",
                "float_remaining",
                "root_cause",
                "recovery_plan",
                "risk_drivers",
            ]
        ],
        hide_index=True,
        width="stretch",
    )
with tab_cost:
    st.dataframe(
        costs[
            [
                "approved_budget",
                "committed_cost",
                "actual_cost",
                "forecast_remaining",
                "estimate_at_completion",
                "forecast_variance",
                "pending_change_orders",
                "expedite_exposure",
                "potential_schedule_exposure",
                "originating_risk_or_change",
            ]
        ],
        hide_index=True,
        width="stretch",
    )
    st.dataframe(changes, hide_index=True, width="stretch")
with tab_risk:
    st.write("Risk = potential future event. Issue = problem that has already occurred.")
    st.dataframe(risks, hide_index=True, width="stretch")
with tab_decision:
    st.dataframe(decisions, hide_index=True, width="stretch")
