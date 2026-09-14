# Problem Statement

## The problem

Power transformers and substations fail without enough warning, and when
they do, the cost is immediate and severe: outages at this scale cost
utilities upward of $1M per hour and can leave hundreds of thousands of
customers without power, sometimes for days.

Most utilities still schedule maintenance on a fixed calendar (e.g. "inspect
every transformer every 18 months") rather than in response to actual asset
condition. Meanwhile, many substations already carry sensors that measure
temperature, vibration, partial discharge, and oil quality — signals that
show degradation weeks before failure. Separately, weather forecasting is
mature and cheap to access. The gap is not a lack of data; it is that the
three data sources that matter — sensor health, weather risk, and historical
incident patterns — are never combined into one number a maintenance planner
or dispatcher can act on before the failure happens.

## Who is affected

- **Grid operations / maintenance planners**, who must decide which of
  dozens or hundreds of assets to prioritise with a limited crew budget.
- **Dispatch coordinators**, who need to pre-position repair crews ahead of
  a storm rather than reactively after an outage is reported.
- **End customers**, who experience the outage itself — longer for
  higher-criticality assets serving more people.

## Why existing approaches fall short

- **Calendar-based maintenance** treats a transformer installed in 1998 the
  same as one installed in 2019, regardless of what its sensors are
  currently reporting.
- **Sensor dashboards** (where they exist) show raw readings per-asset but
  don't rank assets against each other by consequence, and don't factor in
  the weather forecast that could turn a slowly-developing weakness into an
  immediate failure.
- **Weather alerting systems** flag storms at the regional level but have no
  visibility into which specific assets in that region are already
  compromised and therefore most likely to fail under stress.

## Why this matters now

Grid infrastructure is aging in most regions at the same time that extreme
weather events are becoming more frequent, and utility crews are a fixed,
scarce resource. The utilities that can fuse condition data with forecast
data — and act on it hours or days ahead, not after the outage — are the
ones that keep the lights on and keep repair costs from compounding into
emergency callouts.
