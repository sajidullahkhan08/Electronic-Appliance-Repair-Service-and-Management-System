"""
app.py — ElectroFix Flask Application Entry Point
Run: python app.py
"""

import os

from dotenv import load_dotenv

load_dotenv()

from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from config import Config
from routes.customer_routes import customer_bp
from routes.admin_routes import admin_bp

# ── App Setup ─────────────────────────────────────────────────────────────────

FRONTEND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'frontend')

app = Flask(__name__)
app.config.from_object(Config)
app.config['SESSION_COOKIE_SAMESITE'] = Config.SESSION_COOKIE_SAMESITE
app.config['SESSION_COOKIE_SECURE'] = Config.SESSION_COOKIE_SECURE
app.config['PORT'] = Config.PORT

allowed_origins = [origin.strip() for origin in os.getenv('CORS_ORIGINS', 'http://localhost:3000,http://localhost:5000').split(',') if origin.strip()]
CORS(app, resources={r"/api/*": {"origins": allowed_origins}}, supports_credentials=True)

# ── Blueprints ─────────────────────────────────────────────────────────────────

app.register_blueprint(customer_bp, url_prefix='/api')
app.register_blueprint(admin_bp, url_prefix='/api/admin')

# ── Serve Frontend ─────────────────────────────────────────────────────────────

@app.route('/health')
def health():
    return jsonify({"status": "ok", "service": "electrofix-backend"})

@app.route('/')
def index():
    return send_from_directory(FRONTEND_DIR, 'index.html')

@app.route('/<path:path>')
def serve_frontend(path):
    """Serve any file from the frontend directory."""
    file_path = os.path.join(FRONTEND_DIR, path)
    if os.path.isfile(file_path):
        return send_from_directory(FRONTEND_DIR, path)
    # SPA fallback — serve index for unknown routes
    return send_from_directory(FRONTEND_DIR, 'index.html')

# ── Run ────────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    print("=" * 55)
    print("  ElectroFix Repair Management System")
    print("  http://localhost:" + str(Config.PORT))
    print("  Admin Panel: http://localhost:" + str(Config.PORT) + "/admin/login.html")
    print("=" * 55)
    app.run(host='0.0.0.0', debug=Config.DEBUG, port=Config.PORT)
