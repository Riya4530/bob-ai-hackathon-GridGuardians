"""
Turns the ranked risk assessment into a concrete, prioritised
maintenance plan: what to do, on which asset, and how urgently.
"""
from app.services.risk_engine import get_ranked_risk_assessment


def _recommend_action(assessment: dict) -> tuple[str, int]:
    """Returns (recommended_action, recommended_window_hours)."""
    tier = assessment["risk_tier"]
    sub = assessment["sensor_sub_scores"]
    worst_sensor = max(sub, key=sub.get)

    action_map = {
        "temperature_c": "Inspect cooling system and check for overload conditions",
        "vibration_mm_s": "Inspect mechanical mounts and core bolting for looseness",
        "partial_discharge_pc": "Schedule insulation test; partial discharge signature detected",
        "oil_quality_index": "Sample and test dielectric oil; consider oil filtration/replacement",
    }
    base_action = action_map.get(worst_sensor, "General inspection")

    if tier == "CRITICAL":
        return f"URGENT: {base_action}. Dispatch crew before next forecasted weather window.", 24
    if tier == "HIGH":
        return f"{base_action}. Schedule within this week.", 72
    if tier == "MODERATE":
        return f"{base_action}. Schedule within routine maintenance cycle.", 336
    return "No immediate action required; continue standard monitoring.", 2160


def generate_maintenance_plan() -> list[dict]:
    ranked = get_ranked_risk_assessment()
    plan = []
    for i, a in enumerate(ranked, start=1):
        action, window = _recommend_action(a)
        justification = (
            f"Sensor health {a['sensor_health_score']}/100, weather risk "
            f"{a['weather_risk_score']}/100, historical risk {a['historical_risk_score']}/100 "
            f"-> composite {a['composite_risk_score']}/100 ({a['risk_tier']}). "
            f"Serves {a['customers_served']:,} customers at criticality {a['criticality']}/10."
        )
        plan.append(
            {
                "priority_rank": i,
                "asset_id": a["asset_id"],
                "name": a["name"],
                "region": a["region"],
                "composite_risk_score": a["composite_risk_score"],
                "grid_impact_severity": a["grid_impact_severity"],
                "recommended_action": action,
                "recommended_window_hours": window,
                "justification": justification,
            }
        )
    return plan
