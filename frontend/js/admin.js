/* admin.js — Admin panel shared logic */

const API = `${window.getApiBaseUrl ? window.getApiBaseUrl() : "/api"}/admin`;

// ── Auth guard ───────────────────────────────────────────────
async function requireAuth() {
  try {
    const res = await fetch(`${API}/check-auth`, { credentials: "include" });
    const json = await res.json();
    if (!json.authenticated) {
      window.location.href = "/admin/login.html";
    } else {
      const badge = document.getElementById("admin-username");
      if (badge) badge.textContent = json.phone || 'Admin';
    }
  } catch {
    window.location.href = "/admin/login.html";
  }
}

// ── Logout ───────────────────────────────────────────────────
async function doLogout() {
  await fetch(`${API}/logout`, { method: "POST", credentials: "include" });
  window.location.href = "/admin/login.html";
}

// ── Sidebar toggle (mobile) ─────────────────────────────────
const sidebarToggle = document.getElementById("sidebar-toggle");
const sidebar = document.getElementById("sidebar");
if (sidebarToggle && sidebar) {
  sidebarToggle.addEventListener("click", () =>
    sidebar.classList.toggle("open"),
  );
}

// ── Login form ───────────────────────────────────────────────
const loginForm = document.getElementById("login-form");
if (loginForm) {
  loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const btn   = loginForm.querySelector("button[type=submit]");
    const errEl = document.getElementById("login-error");
    btn.disabled = true;
    btn.textContent = "Logging in…";
    if (errEl) errEl.style.display = "none";

    const data = {
      phone:    document.getElementById("phone").value.trim(),
      password: document.getElementById("password").value,
    };
    try {
      const res = await fetch(`${API}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
        credentials: "include",
      });
      const json = await res.json();
      if (json.success) {
        window.location.href = "/admin/dashboard.html";
      } else {
        if (errEl) {
          errEl.textContent = json.error || "Invalid credentials.";
          errEl.style.display = "block";
        }
      }
    } catch {
      if (errEl) {
        errEl.textContent = "Server unreachable.";
        errEl.style.display = "block";
      }
    } finally {
      btn.disabled = false;
      btn.textContent = "Log In";
    }
  });
}

// ── Dashboard stats ─────────────────────────────────────────
async function loadStats() {
  const res = await fetch(`${API}/stats`, { credentials: "include" });
  const json = await res.json();
  if (!json.success) return;
  const d = json.data;
  setEl("stat-total", d.total);
  setEl("stat-pending", d.pending);
  setEl("stat-completed", d.completed);
  setEl("stat-home", d.home_services);
  setEl("stat-progress", d.in_progress);
  setEl("stat-customers", d.customers);
}

// ── Load all requests ────────────────────────────────────────
async function loadRequests(filter) {
  const url = filter
    ? `${API}/requests?service_type=${encodeURIComponent(filter)}`
    : `${API}/requests`;
  const res = await fetch(url, { credentials: "include" });
  const json = await res.json();
  return json.success ? json.data : [];
}

// ── Load customers ───────────────────────────────────────────
async function loadCustomers() {
  const res = await fetch(`${API}/customers`, { credentials: "include" });
  const json = await res.json();
  return json.success ? json.data : [];
}

// ── Status update ────────────────────────────────────────────
async function updateStatus(requestId, status, notes = "") {
  const res = await fetch(`${API}/requests/${requestId}/status`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ status, notes }),
    credentials: "include",
  });
  const json = await res.json();
  return json.success;
}

// ── Status badge HTML ────────────────────────────────────────
function statusBadge(status) {
  const map = {
    Pending: "pending",
    "Under Inspection": "under-inspection",
    Repairing: "repairing",
    Completed: "completed",
    "Ready for Pickup": "ready",
  };
  return `<span class="status-badge status-${map[status] || "pending"}">${status}</span>`;
}

// ── Search filter ────────────────────────────────────────────
function filterTable(inputId, tableBodyId) {
  const input = document.getElementById(inputId);
  const tbody = document.getElementById(tableBodyId);
  if (!input || !tbody) return;
  input.addEventListener("input", () => {
    const q = input.value.toLowerCase();
    tbody.querySelectorAll("tr").forEach((row) => {
      row.style.display = row.textContent.toLowerCase().includes(q)
        ? ""
        : "none";
    });
  });
}

// ── Helpers ──────────────────────────────────────────────────
function setEl(id, val) {
  const el = document.getElementById(id);
  if (el) el.textContent = val ?? "—";
}

// ── Change password (OTP protected) ─────────────────────────
async function changePassword(otp, newPassword, confirmPassword) {
  const res = await fetch(`${API}/change-password`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ otp, new_password: newPassword, confirm_password: confirmPassword }),
    credentials: 'include',
  });
  return await res.json();
}

// ── Change phone number (OTP protected) ──────────────────────
async function changePhone(otp, newPhone) {
  const res = await fetch(`${API}/change-phone`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ otp, new_phone: newPhone }),
    credentials: 'include',
  });
  return await res.json();
}

// ── Send OTP ──────────────────────────────────────────────────
async function sendOtp(purpose) {
  const res = await fetch(`${API}/send-otp`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ purpose }),
    credentials: 'include',
  });
  return await res.json();
}

// expose
window.requireAuth     = requireAuth;
window.doLogout        = doLogout;
window.loadStats       = loadStats;
window.loadRequests    = loadRequests;
window.loadCustomers   = loadCustomers;
window.updateStatus    = updateStatus;
window.statusBadge     = statusBadge;
window.filterTable     = filterTable;
window.setEl           = setEl;
window.changePassword  = changePassword;
window.changePhone     = changePhone;
window.sendOtp         = sendOtp;
