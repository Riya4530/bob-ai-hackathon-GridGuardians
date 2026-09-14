"""
Central configuration for the Grid Guardian backend.
All values are overridable via environment variables (see src/.env.example).
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

# Risk engine weighting (must sum to 1.0). Tunable via env for experimentation
# without touching code, e.g. during judge Q&A.
WEIGHT_SENSOR_HEALTH = float(os.getenv("WEIGHT_SENSOR_HEALTH", "0.5"))
WEIGHT_WEATHER_RISK = float(os.getenv("WEIGHT_WEATHER_RISK", "0.3"))
WEIGHT_HISTORICAL_RISK = float(os.getenv("WEIGHT_HISTORICAL_RISK", "0.2"))

# Sensor thresholds used to normalise raw readings into a 0-100 "bad-ness" score.
SENSOR_THRESHOLDS = {
    "temperature_c": {"warn": 65, "critical": 85},
    "vibration_mm_s": {"warn": 2.5, "critical": 5.5},
    "partial_discharge_pc": {"warn": 300, "critical": 800},
    "oil_quality_index": {"warn": 0.7, "critical": 0.45},  # lower is worse
}

APP_NAME = os.getenv("APP_NAME", "Grid Guardian - Outage Prediction & Equipment Failure Advisor")
API_PORT = int(os.getenv("API_PORT", "8000"))
