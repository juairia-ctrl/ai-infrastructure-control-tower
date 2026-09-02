# 60-90 Second Interview Talk Track

As I prepared for this conversation, I wanted to go beyond reading about program controls and actually think through how I would structure the information. So I built a small synthetic prototype for an AI infrastructure program control tower.

The first screen is the Executive Brief. The goal is that a leader can understand the portfolio in about 30 seconds: which sites are at risk, why, what cost exposure exists, and what decision is required.

The main design principle is that I do not want leadership learning about a problem only when the final milestone turns red. For Site Beta, the transformer supplier still reports Green, but the calculated health is Yellow because manufacturing started late, an intermediate milestone slipped, factory testing moved, and most of the available float has been consumed. That creates an early decision point: continue relying on supplier recovery, pay for mitigation, or validate whether compatible equipment can be reallocated.

Site Gamma shows the integrated version of the same thinking. A design change after the long-lead PO creates a supplier change order, cost exposure, delivery delay, float consumption, and downstream commissioning risk. The point is that schedule, cost, supply chain, and risk should not be treated as disconnected reporting systems.

This is intentionally not a production data-center management system. The data and calculations are synthetic and simplified. What I wanted to demonstrate is how I think as a program manager: work backward from need-by dates, connect leading indicators, make assumptions visible, and turn status into decisions while the team still has options.
