/* tracking.js — Repair status tracking page logic */

const trackForm = document.getElementById("track-form");
const trackInput = document.getElementById("tracking-id-input");
const contactForm = document.getElementById("contact-form");
const contactInput = document.getElementById("contact-input");
const resultBox = document.getElementById("track-result");
const loadingBox = document.getElementById("track-loading");

// ── Status definitions per service type ────────────────────
const SHOP_STATUSES = [
  "Pending",
  "Under Inspection",
  "Repairing",
  "Completed",
  "Ready for Pickup",
];
const HOME_STATUSES = [
  "Pending",
  "Scheduled",
  "Technician Dispatched",
  "Repairing",
  "Completed",
];

const STATUS_ICONS = {
  Pending: "⏳",
  "Under Inspection": "🔍",
  Repairing: "🔧",
  Completed: "✅",
  "Ready for Pickup": "📦",
  Scheduled: "📅",
  "Technician Dispatched": "🚗",
};

// Pre-fill from URL param ?id=EFxxxxxx
const urlParam = new URLSearchParams(window.location.search).get("id");
if (urlParam && trackInput) {
  trackInput.value = urlParam.toUpperCase();
  doTrack(urlParam);
}

// ── Track by ID ─────────────────────────────────────────────
if (trackForm) {
  trackForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const id = trackInput.value.trim().toUpperCase();
    if (!id) return;
    doTrack(id);
  });
}

// ── Track by Name / Phone ───────────────────────────────────
if (contactForm) {
  contactForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const q = contactInput.value.trim();
    if (!q || q.length < 3) {
      resultBox.innerHTML = `<div class="card" style="text-align:center;padding:28px;"><p>Please enter at least 3 characters.</p></div>`;
      return;
    }
    showLoading();
    try {
      const res = await fetch(
        `${window.apiUrl ? window.apiUrl("/track-by-contact") : "/api/track-by-contact"}?query=${encodeURIComponent(q)}`,
        { credentials: "include" },
      );
      const json = await res.json();
      hideLoading();
      if (!json.success) {
        resultBox.innerHTML = notFoundCard(json.error);
        return;
      }
      // Multiple results
      resultBox.innerHTML = json.data.map((d) => buildResultCard(d)).join("");
    } catch {
      hideLoading();
      resultBox.innerHTML = serverErrorCard();
    }
  });
}

// ── Fetch single request by tracking ID ─────────────────────
async function doTrack(id) {
  showLoading();
  resultBox.innerHTML = "";
  try {
    const res = await fetch(
      `${window.apiUrl ? window.apiUrl("/track/") : "/api/track/"}${encodeURIComponent(id)}`,
      { credentials: "include" },
    );
    const json = await res.json();
    hideLoading();
    if (!json.success) {
      resultBox.innerHTML = notFoundCard(
        json.error || "No record found for this Tracking ID.",
      );
      return;
    }
    resultBox.innerHTML = buildResultCard(json.data);
  } catch {
    hideLoading();
    resultBox.innerHTML = serverErrorCard();
  }
}

// ── Build result card HTML ───────────────────────────────────
function buildResultCard(d) {
  const isHome = d.service_type === "Home Service";
  const STATUSES = isHome ? HOME_STATUSES : SHOP_STATUSES;
  const currentIndex = STATUSES.indexOf(d.status);
  const statusClass = d.status.toLowerCase().replace(/ /g, "-");

  const timelineHTML = STATUSES.map((s, i) => {
    const done = i < currentIndex;
    const active = i === currentIndex;
    const dotCls = done ? "done" : active ? "active" : "";
    const icon = STATUS_ICONS[s] || "○";
    return `
      <div class="timeline-item">
        <div class="timeline-left">
          <div class="timeline-dot ${dotCls}">${done ? "✅" : active ? icon : "○"}</div>
          ${i < STATUSES.length - 1 ? '<div class="timeline-line"></div>' : ""}
        </div>
        <div class="timeline-content">
          <h4 style="color:${active ? "var(--blue-light)" : done ? "var(--green)" : "var(--text-3)"};">${s}</h4>
          ${active ? `<p>Current status — updated ${d.updated_at}</p>` : ""}
        </div>
      </div>`;
  }).join("");

  return `
    <div class="card" style="margin-bottom:20px;">
      <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:12px;margin-bottom:20px;">
        <div>
          <p style="font-size:0.78rem;color:var(--text-2);margin-bottom:4px;">TRACKING ID</p>
          <div style="font-size:1.4rem;font-weight:800;color:var(--blue-light);letter-spacing:0.1em;">${d.tracking_id}</div>
        </div>
        <span class="status-badge status-${statusClass}">${d.status}</span>
      </div>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:16px;">
        <div><p style="font-size:0.75rem;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;color:var(--text-2);">Customer</p><p style="color:var(--text-1);margin-top:2px;">${d.customer_name}</p></div>
        <div><p style="font-size:0.75rem;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;color:var(--text-2);">Appliance</p><p style="color:var(--text-1);margin-top:2px;">${d.appliance_type}${d.appliance_brand ? " — " + d.appliance_brand : ""}</p></div>
        <div><p style="font-size:0.75rem;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;color:var(--text-2);">Service</p><p style="color:var(--text-1);margin-top:2px;">${d.service_type}</p></div>
        <div><p style="font-size:0.75rem;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;color:var(--text-2);">Submitted</p><p style="color:var(--text-1);margin-top:2px;">${d.request_date}</p></div>
      </div>
      ${d.problem_description ? `<div style="margin-top:16px;padding:14px;background:rgba(255,255,255,0.03);border-radius:10px;"><p style="font-size:0.75rem;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;color:var(--text-2);margin-bottom:6px;">Problem Description</p><p style="color:var(--text-1);">${d.problem_description}</p></div>` : ""}
      ${d.notes ? `<div style="margin-top:10px;padding:14px;background:rgba(59,130,246,0.06);border:1px solid var(--border-blue);border-radius:10px;"><p style="font-size:0.75rem;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;color:var(--blue-light);margin-bottom:6px;">Technician Notes</p><p style="color:var(--text-1);">${d.notes}</p></div>` : ""}
    </div>
    <div class="card" style="margin-bottom:24px;">
      <h3 style="margin-bottom:24px;">Repair Progress ${isHome ? '<span style="font-size:0.78rem;color:var(--gold);margin-left:8px;">(Home Service)</span>' : ""}</h3>
      <div class="timeline">${timelineHTML}</div>
    </div>`;
}

function showLoading() {
  if (loadingBox) loadingBox.style.display = "block";
  if (resultBox) resultBox.innerHTML = "";
}
function hideLoading() {
  if (loadingBox) loadingBox.style.display = "none";
}
function notFoundCard(msg) {
  return `<div class="card" style="text-align:center;padding:40px;"><div style="font-size:2.5rem;margin-bottom:16px;">❌</div><h3 style="margin-bottom:8px;">Not Found</h3><p>${msg}</p></div>`;
}
function serverErrorCard() {
  return `<div class="card" style="text-align:center;padding:40px;"><p>Could not connect to server. Please try again.</p></div>`;
}
