"""
db.py — Shared database connection helper.
"""

import pymysql
from config import Config


def get_db():
    """Return a new PyMySQL connection using DictCursor."""
    conn = pymysql.connect(
        host=Config.MYSQL_HOST,
        port=Config.MYSQL_PORT,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DB,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    return conn
