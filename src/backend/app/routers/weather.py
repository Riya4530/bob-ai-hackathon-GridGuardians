from fastapi import APIRouter
from app.data_loader import get_weather_forecast

router = APIRouter(prefix="/api/weather", tags=["weather"])


@router.get("/forecast")
def weather_forecast():
    return get_weather_forecast()
