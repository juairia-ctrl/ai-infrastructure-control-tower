import streamlit as st

from utils.data_loader import load_model

st.set_page_config(page_title="Cost Controls", layout="wide")
model = load_model()
costs = model["costs"].copy()
changes = model["changes"]

st.title("Cost Controls")
st.caption("Cost risk surfaces when exposure becomes known, not when the invoice arrives.")

st.info(
    "Committed Cost = contractual commitments already made. Actual Cost = cost incurred. "
    "Estimate at Completion = current forecast of final program cost."
)

costs["known_exposure"] = costs["pending_change_orders"] + costs["expedite_exposure"] + costs["potential_schedule_exposure"]
st.dataframe(
    costs[
        [
            "site",
            "approved_budget",
            "committed_cost",
            "actual_cost",
            "forecast_remaining",
            "estimate_at_completion",
            "forecast_variance",
            "approved_changes",
            "pending_change_orders",
            "expedite_exposure",
            "potential_schedule_exposure",
            "known_exposure",
            "originating_risk_or_change",
            "cost_health",
            "cost_drivers",
        ]
    ],
    hide_index=True,
    width="stretch",
)

st.subheader("Change Control Trace")
st.dataframe(changes, hide_index=True, width="stretch")

st.subheader("Total Cost of Delay Scenario")
c1, c2, c3 = st.columns(3)
mitigation_cost = c1.number_input("Mitigation / expedite cost", min_value=0, value=500000, step=50000)
weekly_delay_cost = c2.number_input("Estimated weekly cost of delay", min_value=0, value=700000, step=50000)
weeks_at_risk = c3.number_input("Weeks at risk", min_value=0.0, value=3.0, step=0.5)
delay_exposure = weekly_delay_cost * weeks_at_risk

left, right = st.columns(2)
left.metric("Estimated Delay Exposure", f"${delay_exposure:,.0f}")
right.metric("Mitigation Cost", f"${mitigation_cost:,.0f}", f"${delay_exposure - mitigation_cost:,.0f} exposure difference")
st.warning(
    "Decision requires consideration of schedule, customer commitments, technical risk, and strategic impact "
    "in addition to this simplified financial comparison."
)
