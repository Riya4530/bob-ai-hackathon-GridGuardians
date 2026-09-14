# Grid Guardian: Power Outage Prediction & Equipment Failure Advisor

## Team

- **Track:** AI
- **Lead:** Om Patel — [REPLACE_WITH_LEAD_EMAIL]
- **Members:** [REPLACE_WITH_MEMBER_NAMES]

## Problem Statement

Power transformer and substation failures cause blackouts costing utilities
$1M+/hour and affecting millions of people. Most utilities still rely on
calendar-based maintenance even though sensors already measuring
temperature, vibration, partial discharge, and oil quality show failure
signatures weeks in advance — and weather forecasts, which compound that
risk, are never combined with sensor data in time to act.

## Solution

Grid Guardian combines live asset sensor readings, regional weather
forecasts, and historical outage records into one explainable **composite
risk score** per asset. Assets are then ranked by **grid impact severity**
(customers served x criticality), which drives an auto-generated,
prioritised **maintenance plan** and a **crew pre-positioning plan**. IBM
Bob can query the exact same live logic through an MCP server — not a
static summary of it.

## Key Features

- Composite risk scoring fusing sensor health + weather + historical incident data
- Grid-impact-severity ranking so prioritisation reflects real-world consequence, not just failure probability
- Explainable, prioritised maintenance plan with a recommended action and urgency window per asset
- Crew pre-positioning plan that matches available crews to at-risk regions ahead of forecasted weather
- Live IBM Bob (MCP) integration — Bob calls the same risk engine the dashboard uses
- Interactive dashboard (risk chart + table, maintenance plan, crew plan) served directly by the backend

## Tech Stack

- **Backend:** Python, FastAPI, Pydantic, pytest
- **IBM technology:** IBM Bob (built with, and integrated via MCP at runtime)
- **Integration:** Model Context Protocol (`mcp` Python SDK, `FastMCP`)
- **Frontend:** Vanilla HTML/CSS/JS + Chart.js (no build step required)
- **Data:** JSON fixtures standing in for SCADA/IoT sensor feeds, a weather API, and an incident database

## How to Run

```bash
cd src/backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Then open http://localhost:8000/. Full instructions, environment variables,
and troubleshooting are in [`docs/setup-guide.md`](docs/setup-guide.md).

## Demo

- Demo video: see [`demo/demo-video-link.txt`](demo/demo-video-link.txt) — **replace with your real recording before submitting**
- Live demo: see [`demo/live-demo-url.txt`](demo/live-demo-url.txt)
- Screenshots: [`demo/screenshots/`](demo/screenshots/) — **add at least 3 before submitting**

## Known Limitations

- Sensor, weather, incident, and crew data are realistic JSON fixtures, not
  a live SCADA/weather API integration — `data_loader.py` is the single
  seam where real feeds would be plugged in.
- The risk-scoring weights and thresholds are reasonable engineering
  defaults, not calibrated against a real utility's historical failure
  data.
- Crew pre-positioning assumes straight region-to-region matching; it does
  not currently account for real road-network travel time.
- No authentication/authorization layer — out of scope for this hackathon
  submission.

## What We're Most Proud Of

The risk engine keeps sensor health, weather risk, and historical risk as
separately-inspectable sub-scores rather than collapsing everything into one
opaque number — and the IBM Bob MCP server calls that exact same engine
live, so a question answered through Bob and a number shown on the
dashboard can never disagree.
