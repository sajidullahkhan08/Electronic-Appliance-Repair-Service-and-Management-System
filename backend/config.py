"""
config.py — ElectroFix Flask Configuration
Reads from environment variables so the same code works
both locally (XAMPP) and on Railway cloud deployment.
"""

import os


class Config:
    # Flask secret key — MUST be set as an env var in Railway
    SECRET_KEY = os.environ.get('SECRET_KEY', 'electrofix-dev-key-change-in-production')

    # MySQL — Railway injects these automatically when you add a MySQL plugin
    MYSQL_HOST     = os.environ.get('MYSQLHOST',     'localhost')
    MYSQL_PORT     = int(os.environ.get('MYSQLPORT', 3306))
    MYSQL_USER     = os.environ.get('MYSQLUSER',     'root')
    MYSQL_PASSWORD = os.environ.get('MYSQLPASSWORD', '')
    MYSQL_DB       = os.environ.get('MYSQLDATABASE', 'electrofix_db')

    # Session cookie settings from .env file
    SESSION_COOKIE_HTTPONLY = os.environ.get('SESSION_COOKIE_HTTPONLY', 'True').lower() == 'true'
    SESSION_COOKIE_SAMESITE = os.environ.get('SESSION_COOKIE_SAMESITE', 'Lax')
    SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'False').lower() == 'true'
    PORT = os.environ.get('PORT')

    # Debug mode — disable in production
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
