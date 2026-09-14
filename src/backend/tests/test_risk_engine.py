from app.services.risk_engine import (
    compute_sensor_health_score,
    compute_weather_risk_score,
    compute_historical_risk_score,
    get_ranked_risk_assessment,
    assess_asset,
)
from app.data_loader import get_asset_by_id


def test_sensor_health_score_is_bounded():
    result = compute_sensor_health_score("TX-101")
    assert 0 <= result["sensor_health_score"] <= 100


def test_worst_asset_scores_higher_than_healthiest():
    """SS-305 has the worst raw sensor readings in the fixture data;
    TX-204 has the best. The engine must rank SS-305 as riskier."""
    worst = compute_sensor_health_score("SS-305")["sensor_health_score"]
    best = compute_sensor_health_score("TX-204")["sensor_health_score"]
    assert worst > best


def test_weather_risk_reflects_storm_alert(monkeypatch):
    from app.services import risk_engine

    calm_weather = {
        "wind_speed_kmh": 40,
        "precip_probability": 0.40,
        "storm_alert": False,
    }

    stormy_weather = {
        "wind_speed_kmh": 40,
        "precip_probability": 0.40,
        "storm_alert": True,
    }

    def fake_weather(region):
        if region == "stormy":
            return stormy_weather
        return calm_weather

    monkeypatch.setattr(
        risk_engine,
        "get_weather_for_region",
        fake_weather,
    )

    calm = risk_engine.compute_weather_risk_score("calm")
    stormy = risk_engine.compute_weather_risk_score("stormy")

    assert stormy > calm


def test_historical_risk_reflects_incident_frequency():
    low = compute_historical_risk_score("Rajkot")
    high = compute_historical_risk_score("Surat")
    assert high > low


def test_ranked_assessment_is_sorted_descending():
    ranked = get_ranked_risk_assessment()
    scores = [a["grid_impact_severity"] for a in ranked]
    assert scores == sorted(scores, reverse=True)


def test_ranked_assessment_covers_every_asset():
    ranked = get_ranked_risk_assessment()
    assert len(ranked) == 8
    assert {a["asset_id"] for a in ranked} == {
        "TX-101",
        "TX-102",
        "TX-203",
        "TX-204",
        "SS-305",
        "TX-306",
        "TX-407",
        "SS-508",
    }


def test_risk_tier_boundaries():
    asset = get_asset_by_id("SS-305")
    assessment = assess_asset(asset)
    assert assessment["risk_tier"] in {"LOW", "MODERATE", "HIGH", "CRITICAL"}