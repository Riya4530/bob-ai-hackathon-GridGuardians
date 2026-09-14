# ⚡ Grid Guardian — Power Outage Prediction & Equipment Failure Advisor

> **Predict. Prioritize. Prevent.**

Grid Guardian is an AI-powered decision-support prototype for predicting power-grid equipment failure and outage risk. It combines asset-health sensor data, weather conditions, and historical outage incidents to identify high-risk equipment, prioritize maintenance, and recommend crew pre-positioning.

---

## 👥 Team

| **Field**     | **Value**                                                     |
| ------------- | ------------------------------------------------------------- |
| **Team Name** | GridGuardians                                                 |
| **Track**     | U1 — Power Outage Prediction & Grid Equipment Failure Advisor |
| **Team Lead** | Riya Patel                                                    |
| **Members**   | Om Patel, Om Pandya, and Parthavi Patel                       |

---

## 🎯 Problem Statement

Power transformers and substations can fail because of equipment degradation, abnormal sensor readings, severe weather, and recurring historical failure patterns. These failures can cause large-scale power outages, affecting thousands of customers and creating significant operational and financial losses for utilities.

Grid operators need a way to identify the most vulnerable assets before failure occurs and decide where maintenance teams and emergency crews should be positioned.

---

## 💡 Solution

**Grid Guardian** combines three major sources of information: asset-health sensor readings, weather conditions/forecasts, and historical incident data.

Its risk engine calculates equipment risk and grid-impact severity, ranks assets from highest to lowest priority, generates recommended maintenance actions, and creates a crew pre-positioning plan for high-risk regions.

The prototype uses simulated IoT sensor data and live weather retrieval with a fallback forecast dataset, making the dashboard suitable for demonstrating how the system can operate in a real-time environment.

---

## ✨ Key Features

* **Asset Health Monitoring:** Evaluates transformer and substation health using temperature, vibration, partial discharge, and oil-quality readings.

* **Weather Risk Analysis:** Incorporates wind speed, precipitation probability, storm alerts, and forecast conditions into the risk assessment.

* **Historical Incident Analysis:** Uses previous outage/failure frequency and weather-correlated incidents to identify historically vulnerable regions.

* **AI-Assisted Risk Ranking:** Combines sensor health, weather risk, historical risk, asset criticality, and customer impact to rank grid assets.

* **Prioritised Maintenance Plan:** Automatically generates recommended actions for high-risk equipment.

* **Crew Pre-Positioning:** Recommends where available response crews should be positioned before a predicted outage.

* **Live Dashboard:** Risk Overview, Maintenance Plan, and Crew Pre-Positioning views automatically refresh every 10 seconds.

* **Geographic Asset Data:** Uses real Gujarat city locations including Vadodara, Ahmedabad, Surat, Rajkot, and Anand for the prototype.

* **MCP Integration:** Includes an MCP server layer for exposing Grid Guardian capabilities to AI-assisted workflows.

---

## 🛠️ Tech Stack

| **Category**                | **Technologies**                      |
| --------------------------- | ------------------------------------- |
| **Languages**               | Python, JavaScript, HTML, CSS, JSON   |
| **Backend Framework**       | FastAPI                               |
| **Frontend**                | HTML, CSS, JavaScript                 |
| **AI Development**          | IBM Bob                               |
| **AI Integration**          | MCP (Model Context Protocol)          |
| **Weather Data**            | Open-Meteo API                        |
| **Data Storage**            | JSON-based prototype datasets         |
| **Testing**                 | Pytest                                |
| **Version Control**         | Git, GitHub                           |
| **Development Environment** | IBM Bob / VS Code-compatible workflow |

---

## 📁 Repository Structure

```text
├── src/
│   ├── backend/
│   │   ├── app/
│   │   │   ├── data/
│   │   │   │   ├── assets.json
│   │   │   │   ├── crews.json
│   │   │   │   ├── historical_incidents.json
│   │   │   │   ├── sensor_readings.json
│   │   │   │   └── weather_forecast.json
│   │   │   │
│   │   │   ├── mcp_server/
│   │   │   │   └── server.py
│   │   │   │
│   │   │   ├── routers/
│   │   │   │   ├── assets.py
│   │   │   │   ├── crew.py
│   │   │   │   ├── maintenance.py
│   │   │   │   ├── risk.py
│   │   │   │   └── weather.py
│   │   │   │
│   │   │   ├── services/
│   │   │   │   ├── crew_planner.py
│   │   │   │   ├── maintenance_planner.py
│   │   │   │   └── risk_engine.py
│   │   │   │
│   │   │   ├── config.py
│   │   │   ├── data_loader.py
│   │   │   └── models.py
│   │   │
│   │   ├── tests/
│   │   │   ├── test_crew_planner.py
│   │   │   ├── test_maintenance_planner.py
│   │   │   └── test_risk_engine.py
│   │   │
│   │   ├── main.py
│   │   └── requirements.txt
│   │
│   └── frontend/
│       ├── index.html
│       ├── style.css
│       └── app.js
│
├── docs/
│   ├── problem-statement.md
│   ├── solution-overview.md
│   ├── architecture.md
│   └── setup-guide.md
│
├── demo/
│   ├── screenshots/
│   ├── demo-video-link.txt
│   └── live-demo-url.txt
│
├── presentation/
│
├── submission.yaml
├── README.md
└── .gitignore
```

---

## ⚡ How to Run

### 1. Clone the repository

```bash
git clone https://github.com/Riya4530/bob-ai-hackathon-GridGuardians.git
cd bob-ai-hackathon-GridGuardians
```

### 2. Go to the backend

On Windows PowerShell:

```powershell
cd "src/backend"
```

### 3. Install Python dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Run the tests

```powershell
python -m pytest -v
```

The project includes automated tests covering the risk engine, maintenance planner, and crew planner.

### 5. Start the FastAPI backend

```powershell
python -m uvicorn main:app --host 127.0.0.1 --port 8001
```

### 6. Open the dashboard

Open the following URL in your browser:

```text
http://127.0.0.1:8001
```

The Grid Guardian dashboard will load the frontend and connect to the FastAPI backend.

---

## 🔌 API Endpoints

The main prototype APIs include:

```text
GET /api/assets
GET /api/risk/ranking
GET /api/maintenance/plan
GET /api/crew/plan
```

These APIs provide asset information, risk ranking, maintenance recommendations, and crew pre-positioning recommendations.

---

## 🌦️ Weather Data

Grid Guardian supports weather data retrieval using geographic coordinates.

The backend can retrieve weather information using the Open-Meteo service and uses the local forecast dataset as a fallback when live weather retrieval is unavailable.

The prototype monitors regions including:

* Vadodara
* Ahmedabad
* Surat
* Rajkot
* Anand

---

## 📡 Data Flow

```text
Asset Sensor Data
       │
       ▼
Asset Health Analysis
       │
       ├──────────────┐
       ▼              ▼
Weather Data    Historical Incidents
       │              │
       └──────┬───────┘
              ▼
         Risk Engine
              │
              ▼
      Grid Impact Severity
              │
       ┌──────┼─────────┐
       ▼      ▼         ▼
    Ranking Maintenance Crew Plan
                     Plan
       │      │         │
       └──────┴─────────┘
              ▼
       Grid Guardian Dashboard
```

---

## 🧠 Risk Assessment

The risk engine considers multiple factors:

```text
Sensor Health
     +
Weather Risk
     +
Historical Risk
     +
Asset Criticality
     +
Customer Impact
     ↓
Composite Risk
     ↓
Grid Impact Severity
     ↓
Risk Tier
```

Assets are classified into risk tiers such as:

```text
LOW
MODERATE
HIGH
CRITICAL
```

Higher-impact assets are placed higher in the ranking so grid operators can focus their attention on the most important equipment first.

---

## 🖥️ Demo

| **Artifact**        | **Link**                       |
| ------------------- | ------------------------------ |
| 📹 **Demo Video**   | See `demo/demo-video-link.txt` |
| 🌐 **Live Demo**    | See `demo/live-demo-url.txt`   |
| 🖼️ **Screenshots** | See `demo/screenshots/`        |
| 📊 **Presentation** | See `presentation/`            |

---

## 🎬 Demonstration Flow

The recommended demo flow is:

### 1. Risk Overview

Show the live dashboard and explain:

* Current asset risk
* Grid impact severity
* Risk ranking
* Critical assets
* Auto-refresh

### 2. Maintenance Plan

Open the **Maintenance Plan** tab and show how the highest-risk assets receive prioritised maintenance recommendations.

### 3. Crew Pre-Positioning

Open the **Crew Pre-Positioning** tab and show how available response crews are assigned to high-risk regions before an expected outage.

### 4. Live Data

Allow the dashboard to refresh and demonstrate that the backend continuously recalculates the displayed risk information.

---

## ⚠️ Known Limitations

* The prototype uses simulated asset sensor and historical incident datasets rather than utility-owned production data.
* Weather data can use live Open-Meteo retrieval, with a local JSON fallback for demonstration reliability.
* The prototype is designed as a decision-support system and does not directly control physical grid equipment.
* Crew planning is a prototype recommendation system and does not connect to real utility workforce-management systems.
* The current data storage uses JSON files rather than a production database.
* The risk engine is a prototype scoring model and would require validation against real utility failure datasets before production deployment.
* The dashboard is primarily designed and tested for a modern desktop browser.

---

## 🔐 Safety & Security

Grid Guardian is designed as a monitoring and decision-support prototype.

It does not directly issue commands to substations, transformers, circuit breakers, or other physical grid-control equipment.

Production deployment would require:

* Authentication and authorization
* Secure API communication
* Protected sensor ingestion
* Audit logging
* Production database infrastructure
* Model validation
* Utility-specific safety controls
* Human approval before operational actions

---

## 🏅 What We're Most Proud Of

Our strongest achievement is connecting the complete decision-making workflow into one working prototype:

```text
Monitor
   ↓
Analyse
   ↓
Predict
   ↓
Prioritize
   ↓
Maintain
   ↓
Pre-position crews
```

Instead of only displaying sensor information, **Grid Guardian turns multiple data sources into actionable operational recommendations**.

The project demonstrates how AI-assisted development with **IBM Bob and MCP** can be used to rapidly build a working power-grid intelligence prototype covering risk assessment, maintenance prioritization, and emergency crew planning.

---

## 🚀 Future Improvements

Future versions of Grid Guardian could include:

* Real utility IoT sensor streaming
* Time-series machine-learning failure prediction
* GIS-based grid visualization
* Real-time weather alerts
* Transformer digital twins
* Historical outage database
* Automatic crew travel-time calculation
* SMS/email emergency alerts
* Cloud deployment
* Role-based operator access
* Explainable AI recommendations
* Integration with utility SCADA/EMS systems

---

## 📌 Project

**Grid Guardian — Power Outage Prediction & Equipment Failure Advisor**

**Tagline:** *Predict. Prioritize. Prevent.*

**Track:** U1

**Team:** GridGuardians
