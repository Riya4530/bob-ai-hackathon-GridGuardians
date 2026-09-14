"""
Generates a crew pre-positioning plan: which crew should move toward
which at-risk region, and how far ahead of the forecasted weather
window they should be in place.

Strategy: for each region with at least one HIGH/CRITICAL asset, prefer
the crew already based in that region (fastest response, no travel
risk). If the local crew is unavailable, borrow the nearest available
crew with a compatible specialty. This mirrors how utility dispatch
centers actually reason about pre-positioning ahead of storms.
"""
from app.data_loader import get_crews, get_weather_for_region
from app.services.risk_engine import get_ranked_risk_assessment

SPECIALTY_BY_ASSET_TYPE = {
    "power_transformer": "transformer_repair",
    "substation": "substation_maintenance",
    "distribution_transformer": "distribution_repair",
}


def _best_available_crew(preferred_specialty: str, exclude_ids: set[str]) -> dict | None:
    crews = [c for c in get_crews() if c["available"] and c["crew_id"] not in exclude_ids]
    # Prefer exact specialty match, then emergency_response as a fallback
    # (emergency crews are cross-trained for exactly this scenario).
    specialty_match = [c for c in crews if c["specialty"] == preferred_specialty]
    if specialty_match:
        return specialty_match[0]
    emergency = [c for c in crews if c["specialty"] == "emergency_response"]
    if emergency:
        return emergency[0]
    return crews[0] if crews else None


def generate_crew_plan() -> list[dict]:
    ranked = get_ranked_risk_assessment()
    at_risk = [a for a in ranked if a["risk_tier"] in ("HIGH", "CRITICAL")]

    crews_by_region = {c["base_region"]: c for c in get_crews()}
    assigned_crew_ids: set[str] = set()
    plan = []

    for asset in at_risk:
        region = asset["region"]
        preferred_specialty = SPECIALTY_BY_ASSET_TYPE.get(asset["type"], "emergency_response")
        weather = get_weather_for_region(region) or {}

        local_crew = crews_by_region.get(region)
        if local_crew and local_crew["available"] and local_crew["crew_id"] not in assigned_crew_ids:
            crew = local_crew
            reason = f"Home crew for {region}; already positioned closest to {asset['name']}."
        else:
            crew = _best_available_crew(preferred_specialty, assigned_crew_ids)
            reason = (
                f"Home crew for {region} unavailable; nearest compatible crew "
                f"({preferred_specialty}) pre-positioned instead."
            )

        if crew is None:
            continue

        assigned_crew_ids.add(crew["crew_id"])
        storm_alert = weather.get("storm_alert", False)
        pre_position_hours = 12 if storm_alert else 24
        if asset["risk_tier"] == "CRITICAL":
            pre_position_hours = min(pre_position_hours, 8)

        plan.append(
            {
                "crew_id": crew["crew_id"],
                "assigned_region": region,
                "specialty": crew["specialty"],
                "size": crew["size"],
                "target_asset_id": asset["asset_id"],
                "target_asset_name": asset["name"],
                "reason": reason,
                "pre_position_before_hours": pre_position_hours,
            }
        )

    return plan
