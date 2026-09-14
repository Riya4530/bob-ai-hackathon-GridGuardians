
const API_BASE = "http://127.0.0.1:8001";

// ============================================================
// DASHBOARD SETTINGS
// ============================================================

// Dashboard refresh interval.
// 10 seconds makes the simulated IoT sensor stream visibly live.
const REFRESH_INTERVAL = 10000;

let refreshTimer = null;
let isRefreshing = false;


// ============================================================
// TAB SWITCHING
// ============================================================

document.querySelectorAll(".tab-btn").forEach((btn) => {
  btn.addEventListener("click", () => {

    document
      .querySelectorAll(".tab-btn")
      .forEach((b) => {
        b.classList.remove("active");
      });

    document
      .querySelectorAll(".tab-panel")
      .forEach((p) => {
        p.classList.remove("active");
      });

    btn.classList.add("active");

    const targetPanel = document.getElementById(
      btn.dataset.tab
    );

    if (targetPanel) {
      targetPanel.classList.add("active");
    }
  });
});


// ============================================================
// API HELPER
// ============================================================

async function fetchJSON(path) {

  const url = API_BASE + path;

  try {

    const res = await fetch(
      url,
      {
        method: "GET",
        cache: "no-store",
        headers: {
          "Accept": "application/json"
        }
      }
    );

    if (!res.ok) {
      throw new Error(
        `Request to ${path} failed with HTTP ${res.status}`
      );
    }

    return await res.json();

  }
  catch (err) {

    console.error(
      `API request failed: ${url}`,
      err
    );

    if (
      err instanceof TypeError
    ) {
      throw new Error(
        `Cannot connect to backend at ${API_BASE}. ` +
        `Make sure FastAPI is running on port 8001 ` +
        `and CORS is enabled.`
      );
    }

    throw err;
  }
}


// ============================================================
// RISK TABLE
// ============================================================

function renderRiskTable(ranking) {

  const container =
    document.getElementById("riskTableWrap");

  if (!container) {
    return;
  }

  if (!Array.isArray(ranking) || ranking.length === 0) {

    container.innerHTML = `
      <div class="card">
        <p>No risk ranking data available.</p>
      </div>
    `;

    return;
  }

  const rows = ranking
    .map(
      (a) => `
        <tr>

          <td>
            ${a.asset_id ?? "N/A"}
          </td>

          <td>
            ${a.name ?? "N/A"}
          </td>

          <td>
            ${a.region ?? "N/A"}
          </td>

          <td>
            ${a.grid_impact_severity ?? 0}
          </td>

          <td>
            <span class="badge ${a.risk_tier ?? "LOW"}">
              ${a.risk_tier ?? "LOW"}
            </span>
          </td>

        </tr>
      `
    )
    .join("");

  container.innerHTML = `

    <table>

      <thead>

        <tr>
          <th>Asset</th>
          <th>Name</th>
          <th>Region</th>
          <th>Severity</th>
          <th>Tier</th>
        </tr>

      </thead>

      <tbody>
        ${rows}
      </tbody>

    </table>
  `;
}


// ============================================================
// RISK CHART
// ============================================================

// Uses HTML/CSS instead of Chart.js.
// This avoids external CDN dependency.

function renderRiskChart(ranking) {

  const container =
    document.getElementById("riskChart");

  if (!container) {
    return;
  }

  if (!Array.isArray(ranking)) {
    return;
  }

  const chartHTML = ranking
    .map((a) => {

      let barClass = "low";

      if (a.risk_tier === "CRITICAL") {
        barClass = "critical";
      }
      else if (a.risk_tier === "HIGH") {
        barClass = "high";
      }
      else if (a.risk_tier === "MODERATE") {
        barClass = "moderate";
      }

      const severity = Math.max(
        0,
        Math.min(
          100,
          Number(
            a.grid_impact_severity
          ) || 0
        )
      );

      return `

        <div class="risk-bar-row">

          <div class="risk-bar-label">

            <span>
              ${a.asset_id ?? "N/A"}
            </span>

            <strong>
              ${severity.toFixed(1)}
            </strong>

          </div>

          <div class="risk-bar-track">

            <div
              class="risk-bar ${barClass}"
              style="width: ${severity}%"
            ></div>

          </div>

        </div>

      `;
    })
    .join("");

  container.innerHTML = `

    <div class="risk-chart">

      <div class="risk-chart-scale">

        <span>0</span>
        <span>25</span>
        <span>50</span>
        <span>75</span>
        <span>100</span>

      </div>

      ${chartHTML}

    </div>

  `;
}


// ============================================================
// MAINTENANCE PLAN
// ============================================================

function renderMaintenancePlan(plan) {

  const container =
    document.getElementById("maintenanceList");

  if (!container) {
    return;
  }

  if (!Array.isArray(plan) || plan.length === 0) {

    container.innerHTML = `
      <div class="plan-item">
        No maintenance recommendations available.
      </div>
    `;

    return;
  }

  container.innerHTML = plan
    .map(
      (t) => `

        <div class="plan-item">

          <div class="plan-title">

            #${t.priority_rank ?? "—"}
            —
            ${t.name ?? "Unknown Asset"}
            (${t.asset_id ?? "N/A"})

          </div>

          <div class="plan-meta">

            ${t.region ?? "Unknown region"}
            · severity
            ${t.grid_impact_severity ?? 0}
            · risk score
            ${t.composite_risk_score ?? 0}

          </div>

          <div class="plan-action">

            ${t.recommended_action ?? "No action available"}

          </div>

        </div>

      `
    )
    .join("");
}


// ============================================================
// CREW PRE-POSITIONING PLAN
// ============================================================

function renderCrewPlan(plan) {

  const container =
    document.getElementById("crewList");

  if (!container) {
    return;
  }

  if (!Array.isArray(plan) || plan.length === 0) {

    container.innerHTML = `
      <div class="plan-item">
        No crew assignments available.
      </div>
    `;

    return;
  }

  container.innerHTML = plan
    .map(
      (c) => `

        <div class="plan-item">

          <div class="plan-title">

            ${c.crew_id ?? "Unknown Crew"}

            (${c.size ?? 0} crew,
            ${c.specialty ?? "general"})

            →

            ${c.assigned_region ?? "Unassigned"}

          </div>

          <div class="plan-meta">

            Target:
            ${c.target_asset_name ?? "N/A"}

            · pre-position within
            ${c.pre_position_before_hours ?? "N/A"}h

          </div>

          <div class="plan-action">

            ${c.reason ?? "No reason provided"}

          </div>

        </div>

      `
    )
    .join("");
}


// ============================================================
// CONNECTION STATUS
// ============================================================

function showConnectionStatus(message) {

  let status =
    document.getElementById("backendStatus");

  if (!status) {

    status = document.createElement("div");

    status.id = "backendStatus";

    status.style.padding = "10px";
    status.style.margin = "10px 0";
    status.style.borderRadius = "8px";
    status.style.fontSize = "14px";

    const main =
      document.querySelector("main");

    if (main) {
      main.prepend(status);
    }
  }

  status.textContent = message;
}


function hideConnectionStatus() {

  const status =
    document.getElementById("backendStatus");

  if (status) {
    status.remove();
  }
}


// ============================================================
// DASHBOARD REFRESH
// ============================================================

async function init() {

  // Prevent two refresh cycles from running simultaneously.
  if (isRefreshing) {
    return;
  }

  isRefreshing = true;

  try {

    showConnectionStatus(
      "Connecting to Grid Guardian backend..."
    );


    // --------------------------------------------------------
    // 1. LIVE RISK RANKING
    // --------------------------------------------------------

    const ranking =
      await fetchJSON(
        "/api/risk/ranking"
      );

    renderRiskTable(
      ranking
    );

    renderRiskChart(
      ranking
    );


    // --------------------------------------------------------
    // 2. LIVE MAINTENANCE PLAN
    // --------------------------------------------------------

    const maintenance =
      await fetchJSON(
        "/api/maintenance/plan"
      );

    renderMaintenancePlan(
      maintenance
    );


    // --------------------------------------------------------
    // 3. LIVE CREW PLAN
    // --------------------------------------------------------

    const crew =
      await fetchJSON(
        "/api/crew/plan"
      );

    renderCrewPlan(
      crew
    );


    // --------------------------------------------------------
    // SUCCESS
    // --------------------------------------------------------

    hideConnectionStatus();

    console.log(
      "Grid Guardian data refreshed:",
      new Date().toLocaleTimeString()
    );

  }

  catch (err) {

    console.error(
      "Dashboard error:",
      err
    );

    showConnectionStatus(
      `Backend connection error: ${err.message}`
    );

  }

  finally {

    isRefreshing = false;

  }
}


// ============================================================
// INITIAL LOAD
// ============================================================

init();


// ============================================================
// AUTOMATIC LIVE REFRESH
// ============================================================

// Refresh dashboard every 10 seconds.
//
// Sensor readings change on every backend request.
// Weather is fetched from Open-Meteo and cached for 5 minutes.

refreshTimer = setInterval(
  () => {

    init();

  },
  REFRESH_INTERVAL
);
