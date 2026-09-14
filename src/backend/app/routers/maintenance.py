from fastapi import APIRouter
from app.services.maintenance_planner import generate_maintenance_plan

router = APIRouter(prefix="/api/maintenance", tags=["maintenance"])


@router.get("/plan")
def maintenance_plan():
    return generate_maintenance_plan()
