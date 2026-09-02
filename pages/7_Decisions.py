import streamlit as st

from utils.data_loader import load_model

st.set_page_config(page_title="Leadership Decisions", layout="wide")
model = load_model()
decisions = model["decisions"]
changed = model["changed"]
definitions = model["definitions"]

st.title("Leadership Decisions")
st.caption("The control tower is designed to surface decisions, not just status.")

status = st.multiselect("Decision status", sorted(decisions["status"].unique()), default=sorted(decisions["status"].unique()))
filtered = decisions[decisions["status"].isin(status)]

st.dataframe(
    filtered[
        [
            "decision_id",
            "site",
            "issue",
            "decision_required",
            "option_a",
            "option_b",
            "option_c",
            "schedule_impact",
            "cost_impact",
            "risk_tradeoff",
            "recommended_action",
            "decision_owner",
            "decision_deadline",
            "status",
        ]
    ],
    hide_index=True,
    width="stretch",
)

st.subheader("Changes Since Last Review")
st.dataframe(changed, hide_index=True, width="stretch")

st.subheader("Single Source of Truth")
st.write(
    "A dashboard is only trustworthy if the underlying definitions, ownership, and data quality are trustworthy."
)
st.dataframe(definitions, hide_index=True, width="stretch")
