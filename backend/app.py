"""
app.py — ElectroFix Flask Application Entry Point
===================================================
LOCAL  : python app.py  →  runs on http://localhost:5000
PROD   : gunicorn app:app --bind 0.0.0.0:$PORT  (Railway Procfile handles this)
"""

import os
from dotenv import load_dotenv

# Load .env file (LOCAL only — in production, Railway sets env vars directly)
load_dotenv()

from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from config import Config
from routes.customer_routes import customer_bp
from routes.admin_routes import admin_bp


# ── App Setup ─────────────────────────────────────────────────────────────────

# Resolve the frontend directory relative to this file (works on any machine)
FRONTEND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'frontend')

app = Flask(__name__)
app.config.from_object(Config)

# Explicit session cookie settings (must be set on the app, not just the class)
app.config['SECRET_KEY']              = Config.SECRET_KEY
app.config['SESSION_COOKIE_HTTPONLY'] = Config.SESSION_COOKIE_HTTPONLY
app.config['SESSION_COOKIE_SAMESITE'] = Config.SESSION_COOKIE_SAMESITE
# LOCAL  : SESSION_COOKIE_SECURE=False (no HTTPS on localhost)
# PROD   : SESSION_COOKIE_SECURE=True  (set SESSION_COOKIE_SECURE=True in Railway)
app.config['SESSION_COOKIE_SECURE']   = Config.SESSION_COOKIE_SECURE

# ── CORS ──────────────────────────────────────────────────────────────────────
# LOCAL  : allows localhost:5000 (default in Config)
# PROD   : set CORS_ORIGINS=https://your-app.up.railway.app in Railway env vars
allowed_origins = [
    o.strip()
    for o in Config.CORS_ORIGINS.split(',')
    if o.strip()
]
CORS(app, resources={r'/api/*': {'origins': allowed_origins}}, supports_credentials=True)

# ── Blueprints ─────────────────────────────────────────────────────────────────

app.register_blueprint(customer_bp, url_prefix='/api')
app.register_blueprint(admin_bp,    url_prefix='/api/admin')

# ── Serve Frontend Static Files ────────────────────────────────────────────────

@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'service': 'electrofix-backend'})

@app.route('/')
def index():
    return send_from_directory(FRONTEND_DIR, 'index.html')

@app.route('/<path:path>')
def serve_frontend(path):
    """Serve any file from the frontend directory; fall back to index.html."""
    file_path = os.path.join(FRONTEND_DIR, path)
    if os.path.isfile(file_path):
        return send_from_directory(FRONTEND_DIR, path)
    return send_from_directory(FRONTEND_DIR, 'index.html')


# ── Entry Point ────────────────────────────────────────────────────────────────
# LOCAL  : run with  python app.py
# PROD   : gunicorn reads app:app — this block is NOT executed in production

if __name__ == '__main__':
    print('=' * 55)
    print('  ElectroFix Repair Management System')
    print(f'  http://localhost:{Config.PORT}')
    print(f'  Admin: http://localhost:{Config.PORT}/admin/login.html')
    print('=' * 55)
    app.run(host='0.0.0.0', debug=Config.DEBUG, port=Config.PORT)
