import plotly.express as px
import streamlit as st

from utils.data_loader import load_model

st.set_page_config(page_title="Portfolio", layout="wide")
model = load_model()

st.title("Portfolio Control View")
st.caption("Portfolio health is calculated from schedule, cost, and supply-chain indicators.")

health = model["health"]
costs = model["costs"]
milestones = model["milestones"]

left, right = st.columns([1.1, 1])
with left:
    st.subheader("Calculated Health by Site")
    st.dataframe(health, hide_index=True, width="stretch")
with right:
    st.subheader("Critical Float Consumption")
    critical = milestones[milestones["critical_path"] == "Yes"].copy()
    fig = px.bar(
        critical.sort_values("float_consumed_pct", ascending=False).head(12),
        x="float_consumed_pct",
        y="milestone",
        color="site",
        orientation="h",
        hover_data=["remaining_float", "variance_days", "need_by_date"],
        labels={"float_consumed_pct": "Float Consumed", "milestone": "Milestone"},
    )
    fig.update_layout(height=420, xaxis_tickformat=".0%", margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig, width="stretch")

st.subheader("Float Model")
st.write("Float = the amount of schedule movement available before a downstream required milestone is affected.")
st.dataframe(
    milestones[
        [
            "site",
            "milestone",
            "baseline_date",
            "current_forecast_date",
            "variance_days",
            "need_by_date",
            "remaining_float",
            "calculated_status",
            "status_drivers",
        ]
    ],
    hide_index=True,
    width="stretch",
)

st.subheader("Cost Exposure by Origin")
cost_view = costs.copy()
cost_view["known_exposure"] = (
    cost_view["pending_change_orders"] + cost_view["expedite_exposure"] + cost_view["potential_schedule_exposure"]
)
st.dataframe(
    cost_view[
        [
            "site",
            "approved_budget",
            "estimate_at_completion",
            "forecast_variance",
            "known_exposure",
            "originating_risk_or_change",
            "cost_health",
        ]
    ],
    hide_index=True,
    width="stretch",
)
