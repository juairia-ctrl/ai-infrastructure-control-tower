import plotly.express as px
import streamlit as st

from utils.data_loader import load_model

st.set_page_config(page_title="Risk Register", layout="wide")
model = load_model()
risks = model["risks"]

st.title("Integrated Risk Register")
st.caption("Risk scoring is illustrative: probability x impact on a 1-5 scale.")
st.write("Risk = potential future event. Issue = problem that has already occurred.")

category = st.multiselect("Category", sorted(risks["category"].unique()), default=sorted(risks["category"].unique()))
filtered = risks[risks["category"].isin(category)]

fig = px.scatter(
    filtered,
    x="probability",
    y="impact",
    size="risk_score",
    color="site",
    hover_name="risk_id",
    hover_data=["type", "description", "schedule_exposure_days", "cost_exposure"],
)
fig.update_layout(xaxis=dict(dtick=1), yaxis=dict(dtick=1), height=380)
st.plotly_chart(fig, width="stretch")

st.dataframe(
    filtered[
        [
            "risk_id",
            "site",
            "type",
            "category",
            "description",
            "trigger_leading_indicator",
            "probability",
            "impact",
            "risk_score",
            "schedule_exposure_days",
            "cost_exposure",
            "critical_path_impact",
            "mitigation",
            "contingency",
            "owner",
            "decision_date",
            "status",
            "last_updated",
        ]
    ],
    hide_index=True,
    width="stretch",
)
