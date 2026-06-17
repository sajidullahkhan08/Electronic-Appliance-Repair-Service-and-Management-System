"""
db.py — Shared database connection helper.
=========================================
LOCAL  : Connects to XAMPP MySQL on localhost:3306.
PROD   : Connects to Railway MySQL plugin using injected env vars.
         No code change needed — config.py handles both via os.environ.
"""

import pymysql
from config import Config


def get_connection(database=None):
    """
    Return a raw PyMySQL connection.
    Pass database=None to connect without selecting a DB (used by init_db.py).
    """
    conn_kwargs = dict(
        host=Config.MYSQL_HOST,
        port=Config.MYSQL_PORT,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor,
        # PROD note: Railway MySQL does not require SSL by default.
        # If you enable SSL in Railway, add:
        #   ssl={'ca': '/path/to/ca-cert.pem'}
    )
    if database:
        conn_kwargs['database'] = database
    return pymysql.connect(**conn_kwargs)


def get_db():
    """Return a connection to the configured application database."""
    return get_connection(database=Config.MYSQL_DB)
