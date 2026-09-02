import plotly.express as px
import streamlit as st

from utils.data_loader import load_model

st.set_page_config(page_title="Forward Capacity", layout="wide")
model = load_model()
pipeline = model["pipeline"]
tradeoffs = model["tradeoffs"]

st.title("Forward Supply / Capacity Forecast")
st.caption("Demand certainty must be balanced against supply certainty.")

st.write(
    "Forward Build Pipeline -> Capacity Requirement -> Equipment Demand -> Lead Time -> Need-By Date -> "
    "Order-By / Capacity Reservation Date"
)

confidence = st.multiselect(
    "Project confidence",
    ["COMMITTED", "PROBABLE", "EARLY PIPELINE"],
    default=["COMMITTED", "PROBABLE", "EARLY PIPELINE"],
)
filtered = pipeline[pipeline["project_confidence"].isin(confidence)]

agg = (
    filtered.groupby(["equipment_category", "need_by_quarter", "supplier", "project_confidence"], as_index=False)[
        "expected_quantity"
    ].sum()
)
fig = px.bar(
    agg,
    x="need_by_quarter",
    y="expected_quantity",
    color="project_confidence",
    facet_col="equipment_category",
    hover_data=["supplier"],
    labels={"expected_quantity": "Expected Quantity", "need_by_quarter": "Need-By Quarter"},
)
fig.update_layout(height=420, margin=dict(l=10, r=10, t=40, b=10))
st.plotly_chart(fig, width="stretch")

st.subheader("Forward Pipeline")
st.dataframe(filtered, hide_index=True, width="stretch")

st.subheader("Portfolio Tradeoff Scenario")
st.write(
    "Synthetic example: three sites require the same constrained equipment, but supplier capacity can support only two. "
    "The recommendation considers critical-path exposure, business impact, and alternatives."
)
st.dataframe(tradeoffs, hide_index=True, width="stretch")
