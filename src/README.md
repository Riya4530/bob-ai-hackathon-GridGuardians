# src/ layout

All source code lives here, split into `backend/` (FastAPI service + risk
engine + MCP server) and `frontend/` (static dashboard, served by the
backend at `/`).

```
src/
├── .env.example        # copy to backend/.env if you want to override defaults
├── backend/
│   ├── main.py          # FastAPI entrypoint - run with uvicorn
│   ├── requirements.txt
│   ├── app/
│   │   ├── config.py        # tunable weights & thresholds
│   │   ├── data_loader.py   # loads mock sensor/weather/incident/crew data
│   │   ├── models.py        # shared Pydantic response models
│   │   ├── services/
│   │   │   ├── risk_engine.py         # fuses sensor+weather+history -> risk score
│   │   │   ├── maintenance_planner.py # turns risk ranking into a work plan
│   │   │   └── crew_planner.py        # pre-positions crews ahead of forecasts
│   │   ├── routers/          # REST endpoints under /api/*
│   │   └── mcp_server/
│   │       └── server.py     # exposes the SAME services to IBM Bob via MCP
│   └── tests/                # pytest suite covering risk/maintenance/crew logic
└── frontend/
    ├── index.html   # dashboard shell (3 tabs: risk, maintenance, crew)
    ├── app.js       # fetches from /api/* and renders table/chart/plan lists
    └── style.css
```

See `docs/setup-guide.md` for exact install/run commands.
