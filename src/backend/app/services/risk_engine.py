"""
Core risk engine.

This is the technical heart of the solution: it fuses three independent
signal sources into one ranked, explainable risk score per asset:

  1. Sensor health   - live temperature / vibration / partial discharge /
                        oil quality readings, normalised against
                        engineering warn/critical thresholds.
  2. Weather risk     - forecasted wind speed, precipitation probability
                        and storm alerts for the asset's region.
  3. Historical risk  - the region's base outage rate and how often past
                        incidents were weather-correlated.

The three sub-scores are combined with configurable weights (see
app/config.py) into a composite_risk_score (0-100), which is then
combined with each asset's grid impact (customers served x criticality)
to produce a grid_impact_severity used for final ranking. Combining
severity *after* risk keeps "how likely" and "how bad" separately
inspectable - useful for judges/utility engineers who want to see the
reasoning, not just a black-box number.
"""
from app.config import SENSOR_THRESHOLDS, WEIGHT_SENSOR_HEALTH, WEIGHT_WEATHER_RISK, WEIGHT_HISTORICAL_RISK
from app.data_loader import (
    get_assets,
    get_sensor_readings,
    get_incident_history_for_region,
    get_weather_for_region,
)


def _normalise(value: float, warn: float, critical: float, lower_is_worse: bool = False) -> float:
    """Map a raw sensor reading to a 0-100 'bad-ness' score using linear
    interpolation between the warn and critical engineering thresholds."""
    if lower_is_worse:
        if value >= warn:
            return 0.0
        if value <= critical:
            return 100.0
        span = warn - critical
        return round((warn - value) / span * 100, 1)
    else:
        if value <= warn:
            return 0.0
        if value >= critical:
            return 100.0
        span = critical - warn
        return round((value - warn) / span * 100, 1)


def compute_sensor_health_score(asset_id: str) -> dict:
    reading = get_sensor_readings()[asset_id]
    scores = {
        "temperature_c": _normalise(reading["temperature_c"], **_threshold_kwargs("temperature_c")),
        "vibration_mm_s": _normalise(reading["vibration_mm_s"], **_threshold_kwargs("vibration_mm_s")),
        "partial_discharge_pc": _normalise(reading["partial_discharge_pc"], **_threshold_kwargs("partial_discharge_pc")),
        "oil_quality_index": _normalise(reading["oil_quality_index"], **_threshold_kwargs("oil_quality_index")),
    }
    # Equal-weighted mean of the four sensor sub-scores.
    health_score = round(sum(scores.values()) / len(scores), 1)
    return {"reading": reading, "sub_scores": scores, "sensor_health_score": health_score}


def _threshold_kwargs(sensor_name: str) -> dict:
    t = SENSOR_THRESHOLDS[sensor_name]
    lower_is_worse = sensor_name == "oil_quality_index"
    return {"warn": t["warn"], "critical": t["critical"], "lower_is_worse": lower_is_worse}


def compute_weather_risk_score(region: str) -> float:
    weather = get_weather_for_region(region)
    if not weather:
        return 0.0
    wind_score = min(weather["wind_speed_kmh"] / 100 * 100, 100)
    precip_score = weather["precip_probability"] * 100
    storm_bonus = 25 if weather["storm_alert"] else 0
    score = min(wind_score * 0.4 + precip_score * 0.4 + storm_bonus * 0.2 + storm_bonus, 100)
    return round(min(score, 100), 1)


def compute_historical_risk_score(region: str) -> float:
    hist = get_incident_history_for_region(region)
    if not hist:
        return 0.0
    incident_score = min(hist["incidents_last_5y"] / 10 * 100, 100)
    correlation_ratio = (hist["weather_correlated"] / hist["incidents_last_5y"]) if hist["incidents_last_5y"] else 0
    severity_score = min(hist["avg_outage_hours"] / 12 * 100, 100)
    score = incident_score * 0.4 + correlation_ratio * 100 * 0.3 + severity_score * 0.3
    return round(min(score, 100), 1)


def compute_grid_impact_severity(customers_served: int, criticality: int, composite_risk_score: float) -> float:
    """Blend of 'how many people lose power' and 'how critical the asset
    is to the grid' with the likelihood of failure, so the final ranking
    reflects real-world consequence, not just failure probability."""
    impact_weight = (customers_served / 65000 * 0.6 + criticality / 10 * 0.4) * 100
    severity = impact_weight * 0.5 + composite_risk_score * 0.5
    return round(min(severity, 100), 1)


def _risk_tier(score: float) -> str:
    if score >= 75:
        return "CRITICAL"
    if score >= 55:
        return "HIGH"
    if score >= 30:
        return "MODERATE"
    return "LOW"


def assess_asset(asset: dict) -> dict:
    sensor = compute_sensor_health_score(asset["id"])
    weather_score = compute_weather_risk_score(asset["region"])
    historical_score = compute_historical_risk_score(asset["region"])

    composite = round(
        sensor["sensor_health_score"] * WEIGHT_SENSOR_HEALTH
        + weather_score * WEIGHT_WEATHER_RISK
        + historical_score * WEIGHT_HISTORICAL_RISK,
        1,
    )
    severity = compute_grid_impact_severity(asset["customers_served"], asset["criticality"], composite)

    return {
        "asset_id": asset["id"],
        "name": asset["name"],
        "region": asset["region"],
        "type": asset["type"],
        "criticality": asset["criticality"],
        "customers_served": asset["customers_served"],
        "sensor_health_score": sensor["sensor_health_score"],
        "sensor_sub_scores": sensor["sub_scores"],
        "weather_risk_score": weather_score,
        "historical_risk_score": historical_score,
        "composite_risk_score": composite,
        "grid_impact_severity": severity,
        "risk_tier": _risk_tier(composite),
    }


def get_ranked_risk_assessment() -> list[dict]:
    """Returns every asset's risk assessment, ranked by grid_impact_severity
    (descending) - the number that matters most for prioritising
    maintenance and crew pre-positioning."""
    assessments = [assess_asset(a) for a in get_assets()]
    assessments.sort(key=lambda a: a["grid_impact_severity"], reverse=True)
    return assessments
