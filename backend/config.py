import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'electrofix-super-secret-key-2024')

    # MySQL Configuration — XAMPP defaults
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_PORT = int(os.environ.get('MYSQL_PORT', 3306))
    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '')
    MYSQL_DB = os.environ.get('MYSQL_DB', 'electrofix_db')

    DEBUG = True
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour
