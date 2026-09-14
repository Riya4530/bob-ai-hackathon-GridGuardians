"""
Entry point for the Grid Guardian backend.

Run with:  uvicorn main:app --reload --port 8000
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.config import APP_NAME
from app.routers import assets, risk, weather, maintenance, crew

app = FastAPI(
    title=APP_NAME,
    description=(
        "Fuses asset sensor health, weather forecasts, and historical "
        "incident data to predict outage-prone equipment, rank assets by "
        "grid impact severity, and generate a prioritised maintenance and "
        "crew pre-positioning plan."
    ),
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(assets.router)
app.include_router(risk.router)
app.include_router(weather.router)
app.include_router(maintenance.router)
app.include_router(crew.router)


@app.get("/api/health")
def health_check():
    return {"status": "ok", "service": APP_NAME}


# Serve the static dashboard frontend at "/", so a judge can open one URL
# and see both the running app and (via /docs) the live API.
frontend_dir = Path(__file__).resolve().parent.parent / "frontend"
if frontend_dir.exists():
    app.mount("/", StaticFiles(directory=str(frontend_dir), html=True), name="frontend")
