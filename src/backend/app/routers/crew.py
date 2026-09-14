from fastapi import APIRouter
from app.services.crew_planner import generate_crew_plan

router = APIRouter(prefix="/api/crew", tags=["crew"])


@router.get("/plan")
def crew_plan():
    return generate_crew_plan()
