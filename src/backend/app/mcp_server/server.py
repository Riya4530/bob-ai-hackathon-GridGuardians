"""
MCP server for IBM Bob integration.

This is what makes Bob *load-bearing* rather than just "the tool we used
to write the code": Bob (or any other MCP client) can call these tools at
runtime to query the SAME live risk engine, maintenance planner, and crew
planner that power the dashboard - not a static copy of the logic.

Run standalone for local testing:
    python -m app.mcp_server.server

Configure in Bob (or Claude Desktop / any MCP client) by pointing it at
this script via stdio transport. See docs/setup-guide.md for the exact
config JSON.
"""
import json

from mcp.server.fastmcp import FastMCP

from app.services.risk_engine import get_ranked_risk_assessment, assess_asset
from app.services.maintenance_planner import generate_maintenance_plan
from app.services.crew_planner import generate_crew_plan
from app.data_loader import get_asset_by_id, get_assets

mcp = FastMCP("grid-guardian")


@mcp.tool()
def get_risk_ranking() -> str:
    """Return every monitored grid asset ranked by grid impact severity,
    with the underlying sensor/weather/historical sub-scores that explain
    why each asset is ranked where it is."""
    return json.dumps(get_ranked_risk_assessment(), indent=2)


@mcp.tool()
def get_asset_risk(asset_id: str) -> str:
    """Return a detailed risk assessment for a single asset by its ID
    (e.g. 'TX-101', 'SS-305'). Use get_risk_ranking first to see valid IDs."""
    asset = get_asset_by_id(asset_id)
    if not asset:
        return json.dumps({"error": f"Asset '{asset_id}' not found"})
    return json.dumps(assess_asset(asset), indent=2)


@mcp.tool()
def get_maintenance_plan() -> str:
    """Return the full prioritised maintenance plan: which asset to service,
    what action to take, and how urgent it is, ranked by priority."""
    return json.dumps(generate_maintenance_plan(), indent=2)


@mcp.tool()
def get_crew_prepositioning_plan() -> str:
    """Return the crew pre-positioning plan for the current forecast
    window: which crew should move to which region, and how many hours
    before the forecasted weather event they should be in place."""
    return json.dumps(generate_crew_plan(), indent=2)


@mcp.tool()
def list_monitored_assets() -> str:
    """List all grid assets currently being monitored, with their region,
    type, and number of customers served."""
    assets = get_assets()
    summary = [
        {
            "id": a["id"],
            "name": a["name"],
            "region": a["region"],
            "type": a["type"],
            "customers_served": a["customers_served"],
        }
        for a in assets
    ]
    return json.dumps(summary, indent=2)


if __name__ == "__main__":
    mcp.run(transport="stdio")
