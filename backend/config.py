"""
config.py — ElectroFix Configuration
======================================
Reads ALL values from environment variables so the same code runs
both locally (XAMPP / .env file) and in the Railway cloud.

LOCAL  — copy .env.example to .env and fill in your XAMPP values.
PROD   — Railway injects MYSQLHOST, MYSQLPORT, MYSQLUSER, etc. automatically
         when you add a MySQL plugin to your Railway project.
"""

import os


class Config:

    # ── Flask ──────────────────────────────────────────────────────────────────
    # LOCAL  : leave default or put SECRET_KEY=xxx in .env
    # PROD   : set SECRET_KEY as an env var in Railway dashboard
    SECRET_KEY = os.environ.get('SECRET_KEY', 'electrofix-dev-secret-key')

    # ── Server port ────────────────────────────────────────────────────────────
    # LOCAL  : runs on 5000 by default
    # PROD   : Railway sets PORT automatically — gunicorn reads it from the Procfile
    PORT = int(os.environ.get('PORT', 5000))

    # ── Debug ──────────────────────────────────────────────────────────────────
    # LOCAL  : set DEBUG=True in .env to get auto-reload
    # PROD   : must be False — Railway env var DEBUG is not set so it defaults False
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

    # ── MySQL ──────────────────────────────────────────────────────────────────
    # LOCAL  : XAMPP MySQL defaults (root, no password, localhost:3306)
    #          Override by adding to .env:  MYSQLHOST=localhost  etc.
    # PROD   : Railway MySQL plugin injects these vars automatically
    MYSQL_HOST     = os.environ.get('MYSQL_HOST',     'localhost')
    MYSQL_PORT     = int(os.environ.get('MYSQL_PORT', 3306))
    MYSQL_USER     = os.environ.get('MYSQL_USER',     'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '')
    MYSQL_DB       = os.environ.get('MYSQL_DB', 'electrofix_db')

    # ── Session Cookies ────────────────────────────────────────────────────────
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    # LOCAL  : False  — no HTTPS on localhost, so Secure must be off
    # PROD   : True   — Railway serves over HTTPS, so cookies must be Secure
    SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'False').lower() == 'true'

    # Railway runs over HTTPS; enable secure cookies by default there.
    if os.environ.get('RAILWAY_SERVICE_ID'):
        SESSION_COOKIE_SECURE = True


    # ── CORS Allowed Origins ───────────────────────────────────────────────────
    # LOCAL  : localhost:5000 (Flask serves both frontend and API on same port)
    # PROD   : set CORS_ORIGINS=https://your-app.up.railway.app in Railway env vars
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'http://localhost:5000,http://127.0.0.1:5000')

    # ── Twilio SMS (for OTP 2FA) ───────────────────────────────────────────────
    # LOCAL  : leave empty → OTP is printed to the Flask console instead of SMS
    # PROD   : set all three in Railway dashboard environment variables
    # Get free credentials at: https://www.twilio.com/try-twilio
    TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', '')
    TWILIO_AUTH_TOKEN  = os.environ.get('TWILIO_AUTH_TOKEN',  '')
    TWILIO_FROM_NUMBER = os.environ.get('TWILIO_FROM_NUMBER', '')  # e.g. +15556667777
