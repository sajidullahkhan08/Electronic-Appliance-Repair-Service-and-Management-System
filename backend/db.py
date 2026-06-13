"""
db.py — Shared database connection helper.
"""

import pymysql
from config import Config

### For production (with SSL)
def _ssl_config():
    ssl_mode = (Config.MYSQL_SSL_MODE or '').upper()
    if ssl_mode in ('REQUIRED', 'VERIFY_CA', 'VERIFY_IDENTITY'):
        return {
            'ca': Config.MYSQL_SSL_CA or None,
            'check_hostname': bool(Config.MYSQL_SSL_CA),
        }
    return None


def get_connection(database=None):
    """Return a new PyMySQL connection using DictCursor and cloud-friendly SSL settings."""
    conn_kwargs = dict(
        host=Config.MYSQL_HOST,
        port=Config.MYSQL_PORT,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor,
    )
    if database:
        conn_kwargs['database'] = database

    ssl_config = _ssl_config()
    if ssl_config is not None:
        conn_kwargs['ssl'] = ssl_config

    return pymysql.connect(**conn_kwargs)


def get_db():
    """Return a new PyMySQL connection to the configured database."""
    return get_connection(database=Config.MYSQL_DB)
