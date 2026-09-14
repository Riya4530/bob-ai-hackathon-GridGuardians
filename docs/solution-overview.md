# Solution Overview

## Core mechanism

Grid Guardian computes one explainable **composite risk score** (0–100) per
monitored asset by combining three independently-scored signals:

1. **Sensor health score** — each of the four live readings (temperature,
   vibration, partial discharge, oil quality) is normalised against
   engineering warn/critical thresholds into a 0–100 "bad-ness" score, then
   averaged.
2. **Weather risk score** — forecasted wind speed and precipitation
   probability for the asset's region, boosted if a storm alert is active.
3. **Historical risk score** — the region's 5-year incident frequency, how
   often those incidents were weather-correlated, and average outage
   duration.

These three sub-scores are combined with configurable weights
(`WEIGHT_SENSOR_HEALTH`, `WEIGHT_WEATHER_RISK`, `WEIGHT_HISTORICAL_RISK` in
`src/backend/app/config.py`) into the composite risk score. That score is
then combined with the asset's **grid impact** — customers served and a
1–10 criticality rating — into a final `grid_impact_severity`, which is what
every ranking, maintenance plan, and crew plan is sorted by.

Keeping "how likely is this to fail" (composite risk) and "how bad would it
be if it did" (grid impact severity) as two separate, inspectable numbers —
rather than one opaque score — is a deliberate design decision: it lets a
grid engineer or judge see *why* an asset was prioritised, not just that it
was.

## What makes it different from naive alternatives

A naive system would either (a) only look at sensor data and miss a healthy
transformer about to be hit by a storm, or (b) only look at weather and miss
a transformer that is already failing on a calm day. Grid Guardian's
weighted fusion means an asset can rank as CRITICAL for either reason, and
the sub-scores in the API response make clear which one is driving it.

## Key design decisions

- **Explainability over a single black-box score.** Every ranked asset
  carries its sensor sub-scores, weather score, and historical score, not
  just the final number.
- **Two-stage planning.** Risk ranking → maintenance plan (what to do) is
  kept separate from risk ranking → crew plan (who should move where), so
  each can be reasoned about and tested independently.
- **Bob as a live client, not a code generator.** The MCP server
  (`src/backend/app/mcp_server/server.py`) calls the exact same
  `risk_engine`, `maintenance_planner`, and `crew_planner` modules used by
  the REST API and the dashboard — so a question answered through Bob and a
  number shown on the dashboard can never silently disagree.

## What the user experience looks like

A grid operations planner opens the dashboard and sees, in order: a bar
chart of every asset ranked by grid impact severity with colour-coded risk
tiers, a sortable risk table, a prioritised maintenance plan with a
recommended action and time window per asset, and a crew pre-positioning
plan showing which crew should move where and how many hours ahead of the
forecasted weather window. The same planner (or a judge) can instead ask
IBM Bob directly — "which assets are at critical risk right now?" or
"where should we send crews before the storm?" — and get the same,
live-computed answer.
