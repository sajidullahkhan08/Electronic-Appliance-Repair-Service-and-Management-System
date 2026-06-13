/* config.js — shared frontend API base configuration */

function getApiBaseUrl() {
  const configured = (
    window.ELECTROFIX_API_BASE_URL ||
    window.__API_BASE_URL ||
    ""
  ).trim();
  if (configured) return configured.replace(/\/$/, "");
  return "/api";
}

function apiUrl(path = "") {
  const base = getApiBaseUrl();
  const normalizedPath = path.startsWith("/") ? path : `/${path}`;
  return `${base}${normalizedPath}`;
}

window.getApiBaseUrl = getApiBaseUrl;
window.apiUrl = apiUrl;
