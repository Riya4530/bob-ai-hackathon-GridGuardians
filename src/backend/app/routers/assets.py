from fastapi import APIRouter, HTTPException
from app.data_loader import get_assets, get_asset_by_id, get_sensor_readings

router = APIRouter(prefix="/api/assets", tags=["assets"])


@router.get("")
def list_assets():
    return get_assets()


@router.get("/{asset_id}")
def get_asset(asset_id: str):
    asset = get_asset_by_id(asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail=f"Asset '{asset_id}' not found")
    reading = get_sensor_readings().get(asset_id)
    return {**asset, "latest_sensor_reading": reading}
