# Setup Guide

This guide assumes a clean machine with no prior setup. Follow it exactly
to run Grid Guardian locally.

## Prerequisites

| Tool | Version | Check with |
|---|---|---|
| Python | 3.10+ | `python3 --version` |
| pip | any recent | `pip --version` |
| A terminal | — | — |
| (Optional) IBM Bob | latest | for MCP integration testing |

No database, no API keys, and no external accounts are required — all
sensor, weather, incident, and crew data is provided as JSON fixtures under
`src/backend/app/data/` so the project runs fully offline.

## Environment variables

Copy the example file and adjust if desired (defaults work out of the box):

```bash
cp src/.env.example src/backend/.env
```

| Variable | Description | Default |
|---|---|---|
| `APP_NAME` | Display name shown in API docs / MCP identity | `Grid Guardian - Outage Prediction & Equipment Failure Advisor` |
| `API_PORT` | Port the backend binds to | `8000` |
| `WEIGHT_SENSOR_HEALTH` | Weight of the sensor sub-score in the composite risk score | `0.5` |
| `WEIGHT_WEATHER_RISK` | Weight of the weather sub-score | `0.3` |
| `WEIGHT_HISTORICAL_RISK` | Weight of the historical incident sub-score | `0.2` |

## Install

```bash
cd src/backend
pip install -r requirements.txt
```

## Run

```bash
# from src/backend/
uvicorn main:app --reload --port 8000
```

Then open **http://localhost:8000/** in a browser — this serves the
dashboard directly. Interactive API docs are at
**http://localhost:8000/docs**.

## Verify it's working

```bash
curl http://localhost:8000/api/health
# {"status":"ok","service":"Grid Guardian - Outage Prediction & Equipment Failure Advisor"}

curl http://localhost:8000/api/risk/ranking
# returns every asset ranked by grid_impact_severity, highest first
```

Run the test suite:

```bash
# from src/backend/
pytest tests/ -v
# 11 passed
```

## Running the MCP server (IBM Bob integration)

The MCP server exposes the same risk/maintenance/crew logic as callable
tools over stdio.

```bash
# from src/backend/
python -m app.mcp_server.server
```

To connect it to IBM Bob (or any MCP-compatible client), add an entry like
this to Bob's MCP configuration:

```json
{
  "mcpServers": {
    "grid-guardian": {
      "command": "python",
      "args": ["-m", "app.mcp_server.server"],
      "cwd": "/absolute/path/to/src/backend"
    }
  }
}
```

Once connected, you can ask Bob things like:

- "List the monitored grid assets."
- "What's the current risk ranking?"
- "Give me the maintenance plan for the highest-risk asset."
- "Where should crews be pre-positioned right now?"

Bob will call `list_monitored_assets`, `get_risk_ranking`,
`get_maintenance_plan`, and `get_crew_prepositioning_plan` respectively —
against the exact same logic the dashboard uses.

## Troubleshooting

| Problem | Fix |
|---|---|
| `ModuleNotFoundError: No module named 'app'` | Run commands from inside `src/backend/`, not the repo root |
| `ModuleNotFoundError: No module named 'mcp.server.fastmcp'` | You have `mcp` 2.x installed; this project targets the 1.x `FastMCP` API — run `pip install "mcp==1.2.0"` |
| Port 8000 already in use | Run with `--port 8001` and adjust any URLs accordingly |
| Dashboard loads but shows no data | Confirm the backend is running and reachable at the same origin the browser is using; check the browser console for the failed fetch URL |
| `pip install` fails to uninstall an existing `mcp` package | Add `--ignore-installed` to the pip install command |
