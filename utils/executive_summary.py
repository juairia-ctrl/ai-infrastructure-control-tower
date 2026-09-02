from __future__ import annotations

import pandas as pd


def site_summary(site: str, model: dict[str, pd.DataFrame]) -> str:
    health = model["health"].set_index("Site").loc[site]
    suppliers = model["suppliers"][model["suppliers"]["site"] == site]
    risks = model["risks"][model["risks"]["site"] == site].sort_values("risk_score", ascending=False)
    decisions = model["decisions"][(model["decisions"]["site"] == site) & (model["decisions"]["status"] == "Open")]

    if health["Overall Health"] == "GREEN":
        return (
            f"{site} remains calculated Green for its target launch. Critical-path float is adequate, "
            "cost remains within forecast tolerance, and only low-level execution risks require monitoring."
        )

    top_risk = risks.iloc[0] if not risks.empty else None
    decision_text = ""
    if not decisions.empty:
        decision = decisions.iloc[0]
        decision_text = f" A leadership decision is required by {decision['decision_deadline']}: {decision['decision_required']}."

    if site == "Site Beta":
        supplier = suppliers[suppliers["equipment"] == "Transformer"].iloc[0]
        return (
            "Site Beta remains forecast for its target launch, but calculated health is Yellow because transformer "
            f"delivery has only {int(supplier['float_remaining'])} days of float remaining while the supplier still reports Green. "
            f"{supplier['risk_drivers']} Recovery is active, but the team should decide before alternate mitigation paths disappear."
            f"{decision_text}"
        )

    if site == "Site Gamma":
        return (
            "Site Gamma is calculated Red because an engineering change after PO release triggered a supplier change order, "
            "cost exposure, delivery delay, float consumption, and downstream commissioning risk. "
            f"{top_risk['description'] if top_risk is not None else 'The integrated exposure requires leadership attention.'}"
            f"{decision_text}"
        )

    return f"{site} is calculated {health['Overall Health']}. Primary driver: {health['Primary Driver']}{decision_text}"


def portfolio_summary(model: dict[str, pd.DataFrame]) -> str:
    health = model["health"]
    at_risk = health[health["Overall Health"].isin(["YELLOW", "RED"])]
    red_sites = health[health["Overall Health"] == "RED"]["Site"].tolist()
    yellow_sites = health[health["Overall Health"] == "YELLOW"]["Site"].tolist()
    return (
        f"The portfolio has {len(at_risk)} of {len(health)} active sites at calculated risk. "
        f"Red exposure is concentrated in {', '.join(red_sites) if red_sites else 'no site'}; "
        f"Yellow early-warning exposure is concentrated in {', '.join(yellow_sites) if yellow_sites else 'no site'}. "
        "The primary leadership focus is supplier-led float consumption at Site Beta and the integrated design-change impact at Site Gamma."
    )
