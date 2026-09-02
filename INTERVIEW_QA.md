# Interview Q&A

## Why did you build this?

I wanted to demonstrate how my program-management, analytics, capacity-planning, and executive-reporting experience can transfer into infrastructure program controls. I used a synthetic prototype so I could show the operating mechanism without implying I have owned production data-center construction programs.

## Why these metrics?

The metrics are designed around executive action: site health, critical-path float, supplier risk, cost exposure, and open decisions. I avoided routine activity metrics because they do not help leadership decide where to intervene.

## How is program health calculated?

Health is calculated from underlying rows, not manually entered dashboard labels. Schedule health uses variance, remaining float, critical-path exposure, and float consumption. Supplier risk uses delivery variance, float, stale updates, production-slot confirmation, critical inputs, and recovery-plan reliability. Cost health uses EAC variance and known exposure.

## How would you integrate real data?

I would start by defining authoritative source fields, metric owners, refresh cadence, and data-quality rules. Then I would connect scheduling, procurement, cost, risk, and change-control sources into a controlled data model with clear ownership for exceptions.

## How would this scale to 20 sites?

The same model would need stronger data governance, role-based views, automated refresh, exception routing, and trend history. The Executive Brief should still stay exception-based so leaders are not forced to scan 20 detailed project reports.

## How would you validate supplier data?

I would compare supplier-reported status against objective milestone evidence: manufacturing start, production gates, factory test readiness, delivery forecast movement, capacity confirmation, and update freshness. Reported Green would not override deteriorating leading indicators.

## How do you determine Yellow vs Red?

Yellow means leading indicators are deteriorating but the team still has credible options. Red means a critical need-by date, commissioning milestone, launch milestone, or credible mitigation path is exposed. In a real environment, I would calibrate thresholds with the construction, supply-chain, finance, and commissioning owners.

## How would this integrate with P6 or an enterprise scheduling system?

I would not try to replace P6. I would treat it as an authoritative scheduling source and extract the milestones, dependencies, need-by dates, baseline dates, current forecasts, and critical-path indicators needed for executive program control.

## How would you avoid executives distrusting the dashboard?

I would make every status explainable, keep definitions visible, show source ownership, track stale and conflicting data, and make it easy to trace a red or yellow label back to the underlying milestone, supplier, change, risk, or decision.

## What would you change after learning the target company's actual processes?

I would adapt the data model to their actual delivery lifecycle, decision forums, supplier categories, approval gates, schedule tools, and leadership operating rhythm. The current version is an illustrative framework, not a claim about their internal process.

## Which parts are based on your professional experience?

The program-control pattern is based on my experience with cross-functional planning, capacity planning, executive reporting, risk management, requirements development, SQL, dashboards, automated reporting, and process improvement.

## Which parts are concepts you learned while preparing?

The data-center-specific examples, such as long-lead equipment milestones, supplier change-order flow, and commissioning exposure, are illustrative concepts I used to understand how my existing strengths could map into the AI infrastructure domain.

## What assumptions did you make?

I assumed three synthetic sites, simplified critical-path logic, simplified cost controls, illustrative risk scoring, and high-level equipment categories. I did not model real engineering quantities, procurement terms, or construction sequencing.

## What are the limitations of this prototype?

It is a local Streamlit prototype with synthetic CSV data. It does not replace a scheduling system, ERP, procurement platform, cost-control system, or construction-management tool. The value is in the program-control logic and executive operating mechanism, not production-grade system integration.
