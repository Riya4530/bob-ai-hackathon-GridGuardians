"""
Grid Guardian Live Data Loader

Data sources:
- Assets: static grid asset registry
- Sensors: simulated live IoT telemetry
- Weather: live Open-Meteo forecast with fallback data
- Historical incidents: historical reference records
- Crews: static crew availability
"""

import json
import random
import time
from typing import Any

import httpx

from app.config import DATA_DIR


# ============================================================
# JSON LOADER
# ============================================================

def _load_json(filename: str) -> Any:
    path = DATA_DIR / filename

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# ============================================================
# STATIC ASSET DATA
# ============================================================

_assets_cache = None


def get_assets() -> list[dict]:
    """
    Load the monitored grid assets.

    Assets are intentionally static because the prototype represents
    a known utility asset registry.
    """
    global _assets_cache

    if _assets_cache is None:
        _assets_cache = _load_json("assets.json")

    return _assets_cache


# ============================================================
# SIMULATED LIVE SENSOR DATA
# ============================================================

def get_sensor_readings() -> dict:
    """
    Generate simulated live IoT sensor telemetry.

    The sensor_readings.json file contains the baseline condition
    of every asset. Small variations are added on every request
    to simulate continuously changing sensor readings.
    """

    base_readings = _load_json("sensor_readings.json")

    live_readings = {}

    for asset_id, reading in base_readings.items():

        # Transformer temperature
        temperature = (
            reading["temperature_c"]
            + random.uniform(-2.0, 2.0)
        )

        # Mechanical vibration
        vibration = (
            reading["vibration_mm_s"]
            + random.uniform(-0.25, 0.25)
        )

        # Partial discharge
        partial_discharge = (
            reading["partial_discharge_pc"]
            + random.uniform(-25.0, 25.0)
        )

        # Oil quality index
        oil_quality = (
            reading["oil_quality_index"]
            + random.uniform(-0.03, 0.03)
        )

        live_readings[asset_id] = {
            "temperature_c": round(
                max(0, temperature),
                1
            ),

            "vibration_mm_s": round(
                max(0, vibration),
                2
            ),

            "partial_discharge_pc": round(
                max(0, partial_discharge),
                1
            ),

            "oil_quality_index": round(
                min(1.0, max(0.0, oil_quality)),
                3
            ),
        }

    return live_readings


# ============================================================
# HISTORICAL INCIDENT DATA
# ============================================================

_historical_incidents_cache = None


def get_historical_incidents() -> list[dict]:
    """
    Load historical outage/incident records.

    Historical records are intentionally static because they
    represent past events rather than live telemetry.
    """

    global _historical_incidents_cache

    if _historical_incidents_cache is None:
        _historical_incidents_cache = _load_json(
            "historical_incidents.json"
        )

    return _historical_incidents_cache


# ============================================================
# LIVE WEATHER DATA
# ============================================================

_weather_cache: dict = {}
_weather_cache_time = 0.0

# Weather API is refreshed every 5 minutes.
# Dashboard itself refreshes every 10 seconds.
WEATHER_CACHE_SECONDS = 300


def _get_live_weather() -> dict:
    """
    Fetch live weather information from Open-Meteo.

    Each region gets its latitude and longitude from assets.json.

    The weather result is cached for 5 minutes to avoid making
    unnecessary external API requests every few seconds.
    """

    global _weather_cache
    global _weather_cache_time

    current_time = time.time()

    # Return cached weather if it is still fresh.
    if (
        _weather_cache
        and current_time - _weather_cache_time
        < WEATHER_CACHE_SECONDS
    ):
        return _weather_cache

    assets = get_assets()

    # Build one geographic location per region.
    regions = {}

    for asset in assets:

        region = asset["region"]

        if region not in regions:

            regions[region] = {
                "lat": asset["lat"],
                "lon": asset["lon"],
            }

    live_weather = {}

    try:

        for region, location in regions.items():

            url = "https://api.open-meteo.com/v1/forecast"

            params = {
                "latitude": location["lat"],
                "longitude": location["lon"],

                "current": (
                    "temperature_2m,"
                    "wind_speed_10m,"
                    "weather_code"
                ),

                "hourly": (
                    "precipitation_probability,"
                    "wind_speed_10m,"
                    "weather_code"
                ),

                "forecast_hours": 24,

                "timezone": "Asia/Kolkata",

                "wind_speed_unit": "kmh",
            }

            response = httpx.get(
                url,
                params=params,
                timeout=8.0,
            )

            response.raise_for_status()

            data = response.json()

            current = data.get(
                "current",
                {}
            )

            hourly = data.get(
                "hourly",
                {}
            )

            # ----------------------------------------------------
            # Wind
            # ----------------------------------------------------

            wind_values = [
                float(value)
                for value in hourly.get(
                    "wind_speed_10m",
                    []
                )
                if value is not None
            ]

            current_wind = float(
                current.get(
                    "wind_speed_10m",
                    0
                )
            )

            max_wind = max(
                wind_values,
                default=current_wind
            )

            # ----------------------------------------------------
            # Precipitation probability
            # ----------------------------------------------------

            precipitation_values = [
                float(value)
                for value in hourly.get(
                    "precipitation_probability",
                    []
                )
                if value is not None
            ]

            max_precipitation = max(
                precipitation_values,
                default=0
            )

            # Convert 0-100 percentage to 0-1
            precipitation_probability = (
                max_precipitation / 100
            )

            # ----------------------------------------------------
            # Storm detection
            # ----------------------------------------------------

            weather_codes = [
                int(value)
                for value in hourly.get(
                    "weather_code",
                    []
                )
                if value is not None
            ]

            # WMO weather codes 95-99 indicate thunderstorms.
            storm_alert = any(
                code >= 95
                for code in weather_codes
            )

            # ----------------------------------------------------
            # Current temperature
            # ----------------------------------------------------

            temperature = float(
                current.get(
                    "temperature_2m",
                    0
                )
            )

            live_weather[region] = {

                "wind_speed_kmh": round(
                    max_wind,
                    1
                ),

                "precip_probability": round(
                    precipitation_probability,
                    2
                ),

                "storm_alert": storm_alert,

                "temperature_c": round(
                    temperature,
                    1
                ),

                "forecast_window_hours": 24,

                "source": "Open-Meteo",

                "live": True,
            }

        # Save successful live result.
        _weather_cache = live_weather
        _weather_cache_time = current_time

        return live_weather

    except Exception as exc:

        print(
            "Live weather API unavailable."
        )

        print(
            f"Using fallback weather data: {exc}"
        )

        # Fallback keeps the dashboard functional if the
        # internet/API temporarily becomes unavailable.
        fallback = _load_json(
            "weather_forecast.json"
        )

        for region in fallback:

            fallback[region]["source"] = (
                "Local fallback dataset"
            )

            fallback[region]["live"] = False

        return fallback


def get_weather_forecast() -> dict:
    """
    Public weather function used by the existing router
    and risk engine.
    """

    return _get_live_weather()


# ============================================================
# CREW DATA
# ============================================================

_crews_cache = None


def get_crews() -> list[dict]:
    """
    Load available maintenance crews.
    """

    global _crews_cache

    if _crews_cache is None:
        _crews_cache = _load_json(
            "crews.json"
        )

    return _crews_cache


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_asset_by_id(
    asset_id: str
) -> dict | None:

    return next(
        (
            asset
            for asset in get_assets()
            if asset["id"] == asset_id
        ),
        None
    )


def get_incident_history_for_region(
    region: str
) -> dict | None:

    return next(
        (
            incident
            for incident in get_historical_incidents()
            if incident["region"] == region
        ),
        None
    )


def get_weather_for_region(
    region: str
) -> dict | None:

    return get_weather_forecast().get(
        region
    )