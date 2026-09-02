import pandas as pd
import plotly.express as px
import streamlit as st

from utils.data_loader import load_model

st.set_page_config(page_title="Supply Chain", layout="wide")
model = load_model()
suppliers = model["suppliers"]

st.title("Supply-Chain Control Tower")
st.caption("Leading indicators flag supplier risk before final delivery is missed.")

site_filter = st.multiselect("Sites", sorted(suppliers["site"].unique()), default=sorted(suppliers["site"].unique()))
filtered = suppliers[suppliers["site"].isin(site_filter)]

conflicts = filtered[filtered["status_conflict"]]
c1, c2, c3, c4 = st.columns(4)
c1.metric("Supplier Risks", int(filtered["calculated_risk"].isin(["YELLOW", "RED"]).sum()))
c2.metric("Status Conflicts", int(filtered["status_conflict"].sum()))
c3.metric("Negative Float Items", int((filtered["float_remaining"] < 0).sum()))
c4.metric("Stale Updates", int(((pd.Timestamp("2026-09-02") - filtered["last_supplier_update"]).dt.days > 7).sum()))

st.subheader("Status Conflict")
st.dataframe(
    conflicts[["site", "equipment", "supplier", "supplier_reported_status", "calculated_risk", "risk_drivers"]],
    hide_index=True,
    width="stretch",
)

st.subheader("Supplier Execution Detail")
st.dataframe(
    filtered[
        [
            "site",
            "equipment",
            "supplier",
            "supplier_tier",
            "manufacturing_start",
            "current_manufacturing_milestone",
            "factory_test_date",
            "committed_delivery",
            "current_forecast_delivery",
            "site_need_by_date",
            "delivery_variance",
            "float_remaining",
            "supplier_reported_status",
            "calculated_risk",
            "root_cause",
            "recovery_plan",
            "alternate_source_available",
            "owner",
            "last_supplier_update",
        ]
    ],
    hide_index=True,
    width="stretch",
)

st.subheader("Supplier Scorecard")
scorecard = (
    suppliers.groupby("supplier")
    .agg(
        deliveries=("equipment", "count"),
        on_time_delivery_pct=("float_remaining", lambda s: (s >= 0).mean()),
        milestone_adherence=("delivery_variance", lambda s: (s <= 3).mean()),
        average_schedule_variance=("delivery_variance", "mean"),
        quality_rework_incidents=("quality_rework_incidents", "sum"),
        lead_time_trend=("lead_time_trend_days", "mean"),
        capacity_risk=("capacity_risk", lambda s: ", ".join(sorted(set(s)))),
        recovery_plan_reliability=("recovery_plan_reliability", lambda s: ", ".join(sorted(set(s)))),
    )
    .reset_index()
)
st.dataframe(scorecard, hide_index=True, width="stretch")

fig = px.scatter(
    filtered,
    x="delivery_variance",
    y="float_remaining",
    color="calculated_risk",
    size="lead_time_trend_days",
    hover_name="equipment",
    hover_data=["site", "supplier", "supplier_reported_status"],
    labels={"delivery_variance": "Delivery Variance (days)", "float_remaining": "Float Remaining (days)"},
)
fig.add_hline(y=0, line_dash="dash", line_color="#c53030")
st.plotly_chart(fig, width="stretch")
