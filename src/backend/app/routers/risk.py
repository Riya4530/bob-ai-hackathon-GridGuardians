from fastapi import APIRouter
from app.services.risk_engine import get_ranked_risk_assessment

router = APIRouter(prefix="/api/risk", tags=["risk"])


@router.get("/ranking")
def risk_ranking():
    return get_ranked_risk_assessment()
