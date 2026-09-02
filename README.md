# AI Infrastructure Program Control Tower

**Integrated schedule, cost, supply-chain, risk, and decision intelligence for concurrent AI infrastructure builds.**

This is a lightweight Streamlit portfolio prototype built with Python, pandas, Plotly, and synthetic CSV data. It is designed to show how program-control principles can connect schedule, supplier, cost, risk, change, and leadership decisions for fast-moving AI infrastructure programs.

## Why I Built This

I built this to show how transferable program-management and analytics strengths can be applied to a new, physical-infrastructure problem space without overstating direct construction-domain ownership.

## Problem

Large infrastructure portfolios often have schedule, supplier, cost, risk, and change information distributed across separate mechanisms. Leadership needs integrated visibility before problems hit final milestones.

## Approach

The prototype connects:

**Schedule + Cost + Supply Chain + Risk + Change + Decisions**

The default Executive Brief focuses on exceptions, exposure, and decisions. It separates reported status from calculated program health and flags early warning signals before final launch milestones fail.

## Core Principles

1. Work backward from need-by dates.
2. Manage the integrated schedule, not isolated milestones.
3. Monitor leading indicators.
4. Track float consumption.
5. Do not rely solely on supplier-reported status.
6. Connect design changes to cost and schedule exposure.
7. Compare mitigation cost with total cost of delay.
8. Manage portfolio tradeoffs rather than optimizing each site independently.
9. Segment forward demand by confidence.
10. Surface decisions, not just status.
11. Establish trustworthy data definitions and ownership.

## What This Demonstrates

- Program-controls thinking
- Schedule and dependency management
- Supply-chain risk reasoning
- Cost and schedule tradeoff analysis
- Portfolio prioritization
- Executive reporting
- Data-quality governance
- Analytics
- Dashboard development
- Structured decision-making

## Demo Story

1. Start on **Executive Brief** and show the calculated portfolio health.
2. Open **Site Detail** for Site Beta and show the supplier-reported Green status versus calculated Yellow health.
3. Open **Leadership Decisions** and discuss the mitigation decision for Beta.
4. Open **Site Detail** or **Cost Controls** for Site Gamma and trace engineering change to change order, cost exposure, schedule delay, float consumption, and commissioning risk.
5. Close by showing how the same mechanism rolls Schedule + Cost + Supply Chain + Risk + Change + Decisions into one control tower.

## Health Logic

Schedule health is calculated from current forecast variance, remaining float, critical-path exposure, and float consumption. Supplier risk is calculated from delivery variance, float, stale updates, production-slot confirmation, critical inputs, and recovery-plan reliability. Cost health is calculated from EAC variance and known exposure.

Thresholds live in `utils/config.py` so they are visible and easy to explain.

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Test

```bash
pytest
```

## Professional Context

This project was built as a synthetic portfolio exercise to explore how large-scale program-management, capacity-planning, analytics, and executive-reporting practices can be applied to complex AI infrastructure delivery.

## Disclaimer

This project uses entirely synthetic data and is an independent portfolio exercise. It does not contain or represent confidential information from any employer, interview target, customer, supplier, or other company. The data-center scenarios and simplified calculations are illustrative and are not intended to represent engineering, construction, financial, or procurement guidance.
