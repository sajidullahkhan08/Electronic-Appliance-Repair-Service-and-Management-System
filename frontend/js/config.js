/* config.js — Frontend API base URL
 *
 * Since Flask serves BOTH the frontend (HTML/CSS/JS) and the backend (API),
 * they live on the exact same domain and port — locally and on Railway.
 *
 * LOCAL  : http://localhost:5000  →  API is at /api/...
 * PROD   : https://your-app.up.railway.app  →  API is at /api/...
 *
 * We ALWAYS use a relative path "/api" — no hardcoded URLs needed.
 */

function getApiBaseUrl() {
  return '/api';
}

function apiUrl(path = '') {
  const normalizedPath = path.startsWith('/') ? path : `/${path}`;
  return `/api${normalizedPath}`;
}

window.getApiBaseUrl = getApiBaseUrl;
window.apiUrl = apiUrl;
