"""Pydantic response models shared across routers and the MCP server."""
from pydantic import BaseModel


class SensorHealth(BaseModel):
    temperature_c: float
    vibration_mm_s: float
    partial_discharge_pc: float
    oil_quality_index: float
    sensor_health_score: float  # 0 (healthy) - 100 (critical)


class RiskAssessment(BaseModel):
    asset_id: str
    name: str
    region: str
    type: str
    criticality: int
    customers_served: int
    sensor_health_score: float
    weather_risk_score: float
    historical_risk_score: float
    composite_risk_score: float
    grid_impact_severity: float
    risk_tier: str  # LOW / MODERATE / HIGH / CRITICAL


class MaintenanceTask(BaseModel):
    priority_rank: int
    asset_id: str
    name: str
    region: str
    composite_risk_score: float
    grid_impact_severity: float
    recommended_action: str
    recommended_window_hours: int
    justification: str


class CrewAssignment(BaseModel):
    crew_id: str
    assigned_region: str
    specialty: str
    size: int
    target_asset_id: str
    target_asset_name: str
    reason: str
    pre_position_before_hours: int
